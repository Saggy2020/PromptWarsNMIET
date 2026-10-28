"""
Storage Service: Manages in-memory / persistent household entities,
inventory, meal plans, shopping lists, and demo data state.
"""

import uuid
from typing import Dict, List, Optional
from datetime import date, timedelta, datetime
from app.models.household import (
    Household, HouseholdMember, RoleEnum, AllergenEnum, MemberAllergy,
    SeverityEnum, MedicalConditionEnum
)
from app.models.inventory import InventoryItem, ItemCategory, ItemStatus, ExpirySource
from app.models.meal_plan import MealPlan, Recipe
from app.models.telemetry import ShoppingList, ShoppingItem, SustainabilityMetrics
from app.safety.shelf_life import lookup_shelf_life

class StorageService:
    def __init__(self):
        self.households: Dict[str, Household] = {}
        self.inventory: Dict[str, List[InventoryItem]] = {}
        self.meal_plans: Dict[str, List[MealPlan]] = {}
        self.shopping_lists: Dict[str, ShoppingList] = {}
        self.sustainability_metrics: Dict[str, SustainabilityMetrics] = {}
        
        # Seed default demo household
        self.seed_demo_data()

    def seed_demo_data(self) -> str:
        """
        Seeds standard realistic demo household ("The Sharma Household")
        with 3 members having distinct allergies/medical constraints and
        near-expiry pantry inventory items.
        """
        demo_household_id = "demo-household-sharma"
        
        aarav = HouseholdMember(
            id="member-aarav",
            name="Aarav Sharma",
            role=RoleEnum.OWNER,
            allergies=[
                MemberAllergy(allergen=AllergenEnum.PEANUTS, severity=SeverityEnum.SEVERE_ANAPHYLAXIS, notes="Anaphylactic to peanuts & groundnuts"),
                MemberAllergy(allergen=AllergenEnum.SHELLFISH, severity=SeverityEnum.SEVERE_ANAPHYLAXIS, notes="Prawns & crab")
            ],
            medical_conditions=[MedicalConditionEnum.HYPERTENSION],
            dietary_preferences=["low-sodium"],
            daily_calorie_target=2200,
            max_daily_sodium_mg=1500
        )
        
        maya = HouseholdMember(
            id="member-maya",
            name="Maya Sharma",
            role=RoleEnum.MEMBER,
            allergies=[
                MemberAllergy(allergen=AllergenEnum.WHEAT_GLUTEN, severity=SeverityEnum.SEVERE_ANAPHYLAXIS, notes="Celiac Disease")
            ],
            medical_conditions=[MedicalConditionEnum.CELIAC_DISEASE],
            dietary_preferences=["gluten-free"],
            daily_calorie_target=1800,
            max_daily_sodium_mg=2000
        )
        
        rohan = HouseholdMember(
            id="member-rohan",
            name="Rohan Sharma",
            role=RoleEnum.MEMBER,
            allergies=[
                MemberAllergy(allergen=AllergenEnum.DAIRY, severity=SeverityEnum.MILD_INTOLERANCE, notes="Lactose intolerant")
            ],
            medical_conditions=[],
            dietary_preferences=["vegetarian"],
            daily_calorie_target=2500,
            max_daily_sodium_mg=2300
        )

        household = Household(
            id=demo_household_id,
            name="The Sharma Household",
            currency="USD",
            created_at=datetime.utcnow(),
            members=[aarav, maya, rohan]
        )
        self.households[demo_household_id] = household

        # Seed Realistic Live Inventory
        today = date.today()
        seeded_items = [
            # Expiring soon (2 days) - High Waste Risk
            InventoryItem(
                id=str(uuid.uuid4()),
                household_id=demo_household_id,
                name="Fresh Baby Spinach",
                normalized_name="spinach",
                category=ItemCategory.PRODUCE,
                quantity=300.0,
                unit="g",
                purchase_date=today - timedelta(days=2),
                expiry_date=today + timedelta(days=2),
                days_to_expiry=2,
                expiry_source=ExpirySource.CURATED_TABLE,
                status=ItemStatus.IN_STOCK,
                estimated_cost=2.99,
                co2e_factor_kg=0.5
            ),
            # Expiring soon (3 days)
            InventoryItem(
                id=str(uuid.uuid4()),
                household_id=demo_household_id,
                name="Organic Firm Tofu",
                normalized_name="tofu",
                category=ItemCategory.PROTEIN,
                quantity=400.0,
                unit="g",
                purchase_date=today - timedelta(days=4),
                expiry_date=today + timedelta(days=3),
                days_to_expiry=3,
                expiry_source=ExpirySource.CURATED_TABLE,
                status=ItemStatus.IN_STOCK,
                estimated_cost=3.49,
                co2e_factor_kg=2.0
            ),
            # Expiring in 4 days
            InventoryItem(
                id=str(uuid.uuid4()),
                household_id=demo_household_id,
                name="Red Bell Pepper",
                normalized_name="bell pepper",
                category=ItemCategory.PRODUCE,
                quantity=2.0,
                unit="pcs",
                purchase_date=today - timedelta(days=3),
                expiry_date=today + timedelta(days=4),
                days_to_expiry=4,
                expiry_source=ExpirySource.CURATED_TABLE,
                status=ItemStatus.IN_STOCK,
                estimated_cost=2.50,
                co2e_factor_kg=0.8
            ),
            # Expiring in 5 days
            InventoryItem(
                id=str(uuid.uuid4()),
                household_id=demo_household_id,
                name="Button Mushrooms",
                normalized_name="mushrooms",
                category=ItemCategory.PRODUCE,
                quantity=250.0,
                unit="g",
                purchase_date=today - timedelta(days=1),
                expiry_date=today + timedelta(days=4),
                days_to_expiry=4,
                expiry_source=ExpirySource.CURATED_TABLE,
                status=ItemStatus.IN_STOCK,
                estimated_cost=2.70,
                co2e_factor_kg=1.3
            ),
            # Long shelf-life pantry staples
            InventoryItem(
                id=str(uuid.uuid4()),
                household_id=demo_household_id,
                name="Organic Brown Basmati Rice",
                normalized_name="brown rice",
                category=ItemCategory.PANTRY,
                quantity=1.5,
                unit="kg",
                purchase_date=today - timedelta(days=10),
                expiry_date=today + timedelta(days=180),
                days_to_expiry=180,
                expiry_source=ExpirySource.CURATED_TABLE,
                status=ItemStatus.IN_STOCK,
                estimated_cost=4.50,
                co2e_factor_kg=2.7
            )
        ]
        self.inventory[demo_household_id] = seeded_items

        # Seed initial sustainability metrics
        self.sustainability_metrics[demo_household_id] = SustainabilityMetrics(
            household_id=demo_household_id,
            total_waste_avoided_kg=4.2,
            total_co2e_avoided_kg=8.8,
            total_money_saved_usd=14.50,
            meals_planned_count=6,
            safety_vetoes_prevented=3,
            last_updated=datetime.utcnow()
        )

        return demo_household_id

    def get_household(self, household_id: str) -> Optional[Household]:
        return self.households.get(household_id)

    def get_inventory(self, household_id: str) -> List[InventoryItem]:
        # recalculate days_to_expiry on read
        items = self.inventory.get(household_id, [])
        today = date.today()
        for item in items:
            item.days_to_expiry = (item.expiry_date - today).days
        return items

    def add_inventory_items(self, household_id: str, items: List[InventoryItem]):
        if household_id not in self.inventory:
            self.inventory[household_id] = []
        self.inventory[household_id].extend(items)

    def update_item_status(self, household_id: str, item_id: str, status: ItemStatus) -> Optional[InventoryItem]:
        items = self.inventory.get(household_id, [])
        for item in items:
            if item.id == item_id:
                old_status = item.status
                item.status = status
                
                # If marked consumed, credit sustainability metrics
                if old_status == ItemStatus.IN_STOCK and status == ItemStatus.CONSUMED:
                    metrics = self.sustainability_metrics.get(household_id)
                    if metrics:
                        # Estimate weight in kg
                        mass_kg = item.quantity if item.unit == "kg" else (item.quantity / 1000.0 if item.unit == "g" else 0.25 * item.quantity)
                        metrics.total_waste_avoided_kg += round(mass_kg, 2)
                        metrics.total_co2e_avoided_kg += round(mass_kg * item.co2e_factor_kg, 2)
                        metrics.total_money_saved_usd += round(item.estimated_cost, 2)
                        metrics.last_updated = datetime.utcnow()
                return item
        return None

    def delete_item(self, household_id: str, item_id: str) -> bool:
        items = self.inventory.get(household_id, [])
        for i, it in enumerate(items):
            if it.id == item_id:
                items.pop(i)
                return True
        return False

    def get_metrics(self, household_id: str) -> SustainabilityMetrics:
        if household_id not in self.sustainability_metrics:
            self.sustainability_metrics[household_id] = SustainabilityMetrics(household_id=household_id)
        return self.sustainability_metrics[household_id]

    def delete_all_household_data(self, household_id: str):
        self.households.pop(household_id, None)
        self.inventory.pop(household_id, None)
        self.meal_plans.pop(household_id, None)
        self.shopping_lists.pop(household_id, None)
        self.sustainability_metrics.pop(household_id, None)

storage_service = StorageService()
