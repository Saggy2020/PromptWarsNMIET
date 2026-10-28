from fastapi import APIRouter
from typing import Dict, Any
from app.services.storage_service import storage_service

router = APIRouter(prefix="/api/demo", tags=["Demo Mode"])

@router.post("/seed")
async def seed_demo_household() -> Dict[str, Any]:
    household_id = storage_service.seed_demo_data()
    return {
        "status": "seeded",
        "household_id": household_id,
        "message": "Demo household 'The Sharma Household' successfully seeded with profiles, near-expiry items, and sustainability metrics."
    }
