from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any
from app.agents.procurement import procurement_agent
from app.services.storage_service import storage_service

router = APIRouter(prefix="/api/shopping", tags=["Procurement"])

@router.post("/generate")
async def generate_shopping_list(household_id: str = Query("demo-household-sharma")) -> Dict[str, Any]:
    return await procurement_agent.generate_shopping_list(household_id)

@router.get("")
async def get_shopping_list(household_id: str = Query("demo-household-sharma")) -> Dict[str, Any]:
    s_list = storage_service.shopping_lists.get(household_id)
    if not s_list:
        # Generate automatically if empty
        return await procurement_agent.generate_shopping_list(household_id)
    return s_list.dict()

@router.post("/approve")
async def approve_shopping_list(household_id: str = Query("demo-household-sharma")) -> Dict[str, Any]:
    s_list = storage_service.shopping_lists.get(household_id)
    if not s_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    s_list.approved_by_user = True
    return {"status": "approved", "message": "Shopping list approved for procurement."}
