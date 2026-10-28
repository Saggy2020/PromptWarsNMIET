from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List
from app.models.meal_plan import PlanGenerationRequest
from app.agents.meal_planner import meal_planner_agent
from app.services.storage_service import storage_service

router = APIRouter(prefix="/api/plan", tags=["Meal Planner"])

@router.post("/generate")
async def generate_meal_plan(payload: PlanGenerationRequest) -> Dict[str, Any]:
    plan_result = await meal_planner_agent.generate_plan(
        household_id=payload.household_id,
        days=payload.days
    )
    return plan_result

@router.get("/latest")
async def get_latest_plan(household_id: str = Query("demo-household-sharma")) -> Dict[str, Any]:
    plans = storage_service.meal_plans.get(household_id, [])
    if not plans:
        return {"has_plan": False, "recipes": []}
    latest = plans[-1]
    return {
        "has_plan": True,
        "plan_id": latest.id,
        "status": latest.status,
        "total_waste_rescued_kg": latest.total_waste_rescued_kg,
        "recipes": [r.dict() for r in latest.recipes]
    }
