from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from app.models.inventory import ReceiptIngestRequest, InventoryItem, ItemStatus, ExpirySource
from app.agents.vision_intake import vision_intake_agent
from app.services.storage_service import storage_service
from datetime import date
import uuid

router = APIRouter(prefix="/api/intake", tags=["Intake"])

@router.post("/receipt")
async def ingest_receipt(payload: ReceiptIngestRequest) -> Dict[str, Any]:
    result = await vision_intake_agent.process_receipt(
        household_id=payload.household_id,
        raw_text=payload.raw_text,
        image_base64=payload.image_base64
    )
    return result

@router.post("/approve")
async def approve_and_commit_items(payload: Dict[str, Any]) -> Dict[str, Any]:
    household_id = payload.get("household_id")
    items_raw = payload.get("items", [])
    
    if not household_id:
        raise HTTPException(status_code=400, detail="household_id is required")

    committed_items: List[InventoryItem] = []
    for it in items_raw:
        item = InventoryItem(
            id=str(uuid.uuid4()),
            household_id=household_id,
            name=it["name"],
            normalized_name=it["name"].lower().strip(),
            category=it["category"],
            quantity=float(it["quantity"]),
            unit=it["unit"],
            purchase_date=date.fromisoformat(it.get("purchase_date", date.today().isoformat())),
            expiry_date=date.fromisoformat(it.get("expiry_date", date.today().isoformat())),
            days_to_expiry=int(it.get("days_to_expiry", 7)),
            expiry_source=ExpirySource(it.get("expiry_source", ExpirySource.CURATED_TABLE)),
            status=ItemStatus.IN_STOCK,
            estimated_cost=float(it.get("estimated_cost", 2.50)),
            co2e_factor_kg=float(it.get("co2e_factor_kg", 1.0))
        )
        committed_items.append(item)

    storage_service.add_inventory_items(household_id, committed_items)

    return {
        "status": "success",
        "committed_count": len(committed_items),
        "items": [it.dict() for it in committed_items]
    }
