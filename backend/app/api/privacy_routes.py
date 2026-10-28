from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List
from app.services.storage_service import storage_service
from app.security.audit_logger import audit_logger

router = APIRouter(prefix="/api/privacy", tags=["Privacy & Auditing"])

@router.get("/export")
async def export_all_household_data(household_id: str = Query("demo-household-sharma")) -> Dict[str, Any]:
    household = storage_service.get_household(household_id)
    if not household:
        raise HTTPException(status_code=404, detail="Household not found")
        
    inventory = storage_service.get_inventory(household_id)
    plans = storage_service.meal_plans.get(household_id, [])
    shopping = storage_service.shopping_lists.get(household_id)
    metrics = storage_service.get_metrics(household_id)
    logs = audit_logger.get_logs_for_household(household_id)

    return {
        "export_timestamp": "2026-10-23T12:00:00Z",
        "household": household.dict(),
        "inventory": [i.dict() for i in inventory],
        "meal_plans": [p.dict() for p in plans],
        "shopping_list": shopping.dict() if shopping else None,
        "sustainability_metrics": metrics.dict(),
        "audit_logs": [l.dict() for l in logs]
    }

@router.delete("/delete-all")
async def delete_all_household_data(household_id: str = Query(...)) -> Dict[str, Any]:
    storage_service.delete_all_household_data(household_id)
    return {
        "status": "success",
        "message": f"All data for household {household_id} has been permanently deleted in accordance with Privacy by Design principles."
    }

@router.get("/audit-logs")
async def get_audit_logs(household_id: str = Query("demo-household-sharma")) -> List[Dict[str, Any]]:
    logs = audit_logger.get_logs_for_household(household_id)
    return [l.dict() for l in logs]
