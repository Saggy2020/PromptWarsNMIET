from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from app.models.inventory import InventoryItem, ItemStatus
from app.services.storage_service import storage_service
from app.agents.replanner import replanner_agent

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])

@router.get("")
async def get_inventory(household_id: str = Query(..., description="Household ID")) -> List[Dict[str, Any]]:
    items = storage_service.get_inventory(household_id)
    return [it.dict() for it in items]

@router.put("/{item_id}/status")
async def update_item_status(
    item_id: str,
    household_id: str = Query(..., description="Household ID"),
    new_status: ItemStatus = Query(..., description="New Status")
) -> Dict[str, Any]:
    updated_item = storage_service.update_item_status(household_id, item_id, new_status)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # If consumed or wasted, trigger re-planning agent in background
    replan_info = None
    if new_status in (ItemStatus.CONSUMED, ItemStatus.WASTED):
        replan_info = await replanner_agent.handle_inventory_change(
            household_id=household_id,
            change_type=new_status.value,
            item_name=updated_item.name
        )

    return {
        "status": "updated",
        "item": updated_item.dict(),
        "replan_info": replan_info
    }

@router.delete("/{item_id}")
async def delete_item(
    item_id: str,
    household_id: str = Query(..., description="Household ID")
) -> Dict[str, Any]:
    success = storage_service.delete_item(household_id, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "deleted", "item_id": item_id}
