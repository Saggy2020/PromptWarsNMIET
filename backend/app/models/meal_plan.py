from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class SafetyStatus(str, Enum):
    SAFE = "safe"
    WARNING = "warning"
    UNSAFE = "unsafe"

class MemberSafetyVerdict(BaseModel):
    member_id: str
    member_name: str
    status: SafetyStatus
    reasons: List[str] = Field(default_factory=list)
    flagged_ingredients: List[str] = Field(default_factory=list)
    synonym_matched: Optional[str] = None
    is_vetoed: bool = False

class RecipeIngredient(BaseModel):
    name: str
    normalized_name: str
    quantity: float
    unit: str
    in_inventory: bool = False
    inventory_item_id: Optional[str] = None
    synonyms: List[str] = Field(default_factory=list)

class Recipe(BaseModel):
    id: str
    title: str
    description: str
    ingredients: List[RecipeIngredient]
    instructions: List[str]
    prep_time_minutes: int = Field(default=20, ge=1)
    servings: int = Field(default=4, ge=1)
    estimated_calories_per_serving: int = 450
    sodium_mg_per_serving: int = 400
    waste_reduction_score: float = Field(default=50.0, ge=0.0, le=100.0)
    expiring_items_used: List[str] = Field(default_factory=list)
    member_verdicts: List[MemberSafetyVerdict] = Field(default_factory=list)
    overall_safety: SafetyStatus = SafetyStatus.SAFE
    explainability_rationale: str

class MealPlan(BaseModel):
    id: str
    household_id: str
    week_start_date: str
    recipes: List[Recipe] = Field(default_factory=list)
    total_waste_rescued_kg: float = 0.0
    status: str = "draft" # draft, approved, active
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PlanGenerationRequest(BaseModel):
    household_id: str
    days: int = 7
    prioritize_expiring_days: int = 3
    target_servings: int = 4
