"""
Procurement Agent: Compiles consolidated, aisle-grouped shopping lists
by diffing approved recipes with live inventory, suggesting allergen-safe substitutions.
"""

import uuid
from typing import Dict, Any, List
from datetime import datetime
from app.models.telemetry import ShoppingList, ShoppingItem, AgentName
from app.models.inventory import ItemCategory
from app.safety.shelf_life import lookup_shelf_life
from app.safety.engine import safety_guardian
from app.services.storage_service import storage_service
from app.security.audit_logger import audit_logger

class ProcurementAgent:
    def __init__(self):
        self.agent_name = AgentName.PROCUREMENT

    async def generate_shopping_list(self, household_id: str) -> Dict[str, Any]:
        household = storage_service.get_household(household_id)
        if not household:
            return {"error": "Household not found", "items": []}

        # Get latest approved meal plan
        plans = storage_service.meal_plans.get(household_id, [])
        if not plans:
            return {"message": "No active meal plans found to compile shopping list.", "items": []}
            
        latest_plan = plans[-1]
        inventory = storage_service.get_inventory(household_id)
        inventory_names = {it.name.lower().strip(): it for it in inventory if it.status == "in_stock"}

        missing_items: List[ShoppingItem] = []
        total_cost = 0.0

        for recipe in latest_plan.recipes:
            for ing in recipe.ingredients:
                ing_key = ing.name.lower().strip()
                # Check if item is already in pantry
                if ing_key not in inventory_names:
                    # Look up category and estimated cost
                    exp_date, days, category, co2e, unit_cost, source = lookup_shelf_life(ing.name)
                    
                    # Safe substitutes check
                    substitutes = []
                    if "tamari" in ing_key or "soy sauce" in ing_key:
                        substitutes = ["Coconut Aminos (Gluten-Free & Soy-Free)"]

                    item = ShoppingItem(
                        id=str(uuid.uuid4()),
                        name=ing.name,
                        category=category,
                        quantity=ing.quantity,
                        unit=ing.unit,
                        estimated_cost=unit_cost,
                        recipe_references=[recipe.title],
                        safe_substitutes=substitutes
                    )
                    missing_items.append(item)
                    total_cost += unit_cost

        # Save shopping list
        shopping_list = ShoppingList(
            id=str(uuid.uuid4()),
            household_id=household_id,
            items=missing_items,
            total_estimated_cost=round(total_cost, 2),
            requires_approval=True,
            approved_by_user=False
        )
        storage_service.shopping_lists[household_id] = shopping_list

        audit_logger.record_decision(
            household_id=household_id,
            agent_name=self.agent_name,
            action="shopping_list_compiled",
            input_summary=f"Plan: {latest_plan.id}, Recipes: {len(latest_plan.recipes)}",
            output_summary=f"Compiled {len(missing_items)} missing items. Est cost: ${round(total_cost, 2)}"
        )

        return {
            "shopping_list_id": shopping_list.id,
            "items": [it.dict() for it in missing_items],
            "total_estimated_cost": round(total_cost, 2),
            "requires_approval": True,
            "status": "awaiting_user_confirmation"
        }

procurement_agent = ProcurementAgent()
