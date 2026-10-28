from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel
from app.models.meal_plan import RecipeIngredient
from app.safety.engine import safety_guardian
from app.services.storage_service import storage_service

router = APIRouter(prefix="/api/safety", tags=["Safety Guardian"])

class SafetyCheckRequest(BaseModel):
    household_id: str
    recipe_title: str
    ingredients: List[str]
    sodium_mg: int = 400

@router.post("/veto-check")
async def evaluate_safety(payload: SafetyCheckRequest) -> Dict[str, Any]:
    household = storage_service.get_household(payload.household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")

    recipe_ings = [
        RecipeIngredient(
            name=name,
            normalized_name=name.lower().strip(),
            quantity=100.0,
            unit="g"
        )
        for name in payload.ingredients
    ]

    overall_status, verdicts, is_vetoed = safety_guardian.evaluate_recipe(
        recipe_title=payload.recipe_title,
        ingredients=recipe_ings,
        sodium_mg_per_serving=payload.sodium_mg,
        household_members=household.members
    )

    return {
        "recipe_title": payload.recipe_title,
        "is_vetoed": is_vetoed,
        "overall_status": overall_status.value,
        "member_verdicts": [v.dict() for v in verdicts]
    }
