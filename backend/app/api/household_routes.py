from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List
from app.models.household import Household, HouseholdMember
from app.services.storage_service import storage_service

router = APIRouter(prefix="/api/household", tags=["Household"])

@router.get("")
async def get_household(household_id: str = Query("demo-household-sharma")) -> Dict[str, Any]:
    household = storage_service.get_household(household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
    return household.dict()

@router.post("/member")
async def add_household_member(
    household_id: str,
    member: HouseholdMember
) -> Dict[str, Any]:
    household = storage_service.get_household(household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
    
    if len(household.members) >= 6:
        raise HTTPException(status_code=400, detail="Maximum 6 members allowed per household.")

    household.members.append(member)
    return {"status": "member_added", "member": member.dict()}
