from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime

class ItemCategory(str, Enum):
    PRODUCE = "produce"
    DAIRY = "dairy"
    PROTEIN = "protein"
    PANTRY = "pantry"
    BAKERY = "bakery"
    FROZEN = "frozen"
    BEVERAGES = "beverages"

class ItemStatus(str, Enum):
    IN_STOCK = "in_stock"
    CONSUMED = "consumed"
    WASTED = "wasted"

class ExpirySource(str, Enum):
    CURATED_TABLE = "curated_table"
    AI_ESTIMATE = "ai_estimate"
    MANUAL_ENTRY = "manual_entry"

class InventoryItem(BaseModel):
    id: str = Field(..., description="Unique item UUID")
    household_id: str
    name: str = Field(..., min_length=1, max_length=120)
    normalized_name: str
    category: ItemCategory
    quantity: float = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=20) # g, kg, ml, l, pcs, bunch
    purchase_date: date
    expiry_date: date
    days_to_expiry: int
    expiry_source: ExpirySource
    status: ItemStatus = ItemStatus.IN_STOCK
    estimated_cost: float = Field(default=0.0, ge=0)
    co2e_factor_kg: float = Field(default=1.0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class IntakeItemInput(BaseModel):
    name: str
    category: ItemCategory = ItemCategory.PRODUCE
    quantity: float = 1.0
    unit: str = "pcs"
    purchase_date: Optional[date] = None
    expiry_days_override: Optional[int] = None

class ReceiptIngestRequest(BaseModel):
    household_id: str
    raw_text: Optional[str] = None
    image_base64: Optional[str] = None
    mime_type: Optional[str] = "image/jpeg"
