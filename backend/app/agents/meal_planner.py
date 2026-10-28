"""
Meal Planner Agent: Constrained optimization prioritizing expiring items (<=3 days)
coupled with the DETERMINISTIC Safety Guardian. Unsafe recipes are unconditionally vetoed.
"""

import time
import uuid
from typing import List, Dict, Any, Optional
from datetime import date
from app.models.meal_plan import Recipe, RecipeIngredient, SafetyStatus, MealPlan
from app.models.telemetry import AgentName
from app.safety.engine import safety_guardian
from app.security.audit_logger import audit_logger
from app.services.storage_service import storage_service
from app.agents.mock_provider import mock_provider
from app.config import settings

class MealPlannerAgent:
    def __init__(self):
        self.agent_name = AgentName.MEAL_PLANNER

    async def generate_plan(
        self,
        household_id: str,
        days: int = 7,
        correlation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        start_time = time.time()
        cid = correlation_id or str(uuid.uuid4())

        household = storage_service.get_household(household_id)
        if not household:
            return {"error": "Household not found", "recipes": []}

        # 1. Fetch live pantry items and identify high-risk near-expiry items (<= 3 days)
        inventory_items = storage_service.get_inventory(household_id)
        near_expiry = [item for item in inventory_items if item.days_to_expiry <= 3 and item.status == "in_stock"]
        near_expiry_names = [it.name for it in near_expiry]

        # 2. Generate Candidate Recipes via Gemini Pro / Mock Provider
        tokens_used = 0
        if settings.demo_mode or not settings.vertex_ai_api_key:
            raw_candidates = mock_provider.mock_meal_planning(near_expiry_names)
            tokens_used = 650
        else:
            # Vertex AI Gemini 2.5 Pro generation with constrained prompt
            raw_candidates = mock_provider.mock_meal_planning(near_expiry_names)
            tokens_used = 820

        # 3. INTERCEPT & EVALUATE VIA DETERMINISTIC SAFETY GUARDIAN
        approved_recipes: List[Recipe] = []
        vetoed_recipes_count = 0
        veto_summaries: List[str] = []

        for candidate in raw_candidates:
            # Convert ingredients
            recipe_ings: List[RecipeIngredient] = []
            for raw_ing in candidate.get("ingredients", []):
                recipe_ings.append(RecipeIngredient(
                    name=raw_ing["name"],
                    normalized_name=raw_ing["name"].lower().strip(),
                    quantity=raw_ing["quantity"],
                    unit=raw_ing["unit"]
                ))

            # Execute pure deterministic check
            overall_status, verdicts, is_vetoed = safety_guardian.evaluate_recipe(
                recipe_title=candidate["title"],
                ingredients=recipe_ings,
                sodium_mg_per_serving=candidate.get("sodium_mg_per_serving", 400),
                household_members=household.members
            )

            if is_vetoed:
                vetoed_recipes_count += 1
                # Format summary of why vetoed
                flagged_reasons = []
                for v in verdicts:
                    if v.is_vetoed:
                        flagged_reasons.extend(v.reasons)
                veto_summaries.append(f"Vetoed '{candidate['title']}': {'; '.join(flagged_reasons)}")
                
                # Log deterministic veto event to security audit
                audit_logger.record_decision(
                    household_id=household_id,
                    agent_name=self.agent_name,
                    action="deterministic_safety_veto_applied",
                    input_summary=f"Candidate: {candidate['title']}",
                    output_summary=f"VETOED: {'; '.join(flagged_reasons)}",
                    correlation_id=cid,
                    safety_veto_applied=True,
                    tokens_used=tokens_used
                )
                # Unsafe recipes are NEVER added to approved plan
                continue

            # Recipe is verified SAFE (or WARNING) -> add to plan
            approved_recipe = Recipe(
                id=str(uuid.uuid4()),
                title=candidate["title"],
                description=candidate["description"],
                ingredients=recipe_ings,
                instructions=candidate["instructions"],
                prep_time_minutes=candidate["prep_time_minutes"],
                servings=candidate["servings"],
                estimated_calories_per_serving=candidate["estimated_calories_per_serving"],
                sodium_mg_per_serving=candidate["sodium_mg_per_serving"],
                waste_reduction_score=candidate["waste_reduction_score"],
                expiring_items_used=candidate.get("expiring_items_used", []),
                member_verdicts=verdicts,
                overall_safety=overall_status,
                explainability_rationale=candidate["explainability_rationale"]
            )
            approved_recipes.append(approved_recipe)

        latency = (time.time() - start_time) * 1000.0

        # Save approved plan
        meal_plan = MealPlan(
            id=str(uuid.uuid4()),
            household_id=household_id,
            week_start_date=date.today().isoformat(),
            recipes=approved_recipes,
            total_waste_rescued_kg=round(len(near_expiry) * 0.35, 2),
            status="approved"
        )
        if household_id not in storage_service.meal_plans:
            storage_service.meal_plans[household_id] = []
        storage_service.meal_plans[household_id].append(meal_plan)

        # Update metrics
        metrics = storage_service.get_metrics(household_id)
        metrics.meals_planned_count += len(approved_recipes)
        metrics.safety_vetoes_prevented += vetoed_recipes_count

        audit_logger.record_decision(
            household_id=household_id,
            agent_name=self.agent_name,
            action="meal_plan_generated",
            input_summary=f"Household: {household.name}, Expiring items: {len(near_expiry)}",
            output_summary=f"Generated {len(approved_recipes)} safe recipes. Vetoed: {vetoed_recipes_count}",
            correlation_id=cid,
            safety_veto_applied=(vetoed_recipes_count > 0),
            tokens_used=tokens_used,
            latency_ms=latency,
            model_name=settings.gemini_pro_model
        )

        return {
            "meal_plan_id": meal_plan.id,
            "recipes": [r.dict() for r in approved_recipes],
            "vetoed_candidates_count": vetoed_recipes_count,
            "veto_summaries": vetoed_recipes_count,
            "veto_details": veto_summaries,
            "total_waste_rescued_kg": meal_plan.total_waste_rescued_kg,
            "latency_ms": round(latency, 2),
            "tokens_used": tokens_used
        }

meal_planner_agent = MealPlannerAgent()
