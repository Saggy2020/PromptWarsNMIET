from fastapi import APIRouter, Query
from typing import Dict, Any
from app.agents.sustainability import sustainability_agent

router = APIRouter(prefix="/api/sustainability", tags=["Sustainability"])

@router.get("/metrics")
async def get_sustainability_metrics(household_id: str = Query("demo-household-sharma")) -> Dict[str, Any]:
    return sustainability_agent.get_household_impact(household_id)
