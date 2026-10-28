from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.inventory import ItemCategory

class AgentName(str, Enum):
    ORCHESTRATOR = "orchestrator"
    VISION_INTAKE = "vision_intake"
    SAFETY_GUARDIAN = "safety_guardian"
    MEAL_PLANNER = "meal_planner"
    PROCUREMENT = "procurement"
    SUSTAINABILITY = "sustainability"

class AuditLogEntry(BaseModel):
    id: str
    correlation_id: str
    household_id: str
    agent_name: AgentName
    action: str
    input_summary: str
    output_summary: str
    safety_veto_applied: bool = False
    tokens_used: int = 0
    latency_ms: float = 0.0
    cost_usd: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SustainabilityMetrics(BaseModel):
    household_id: str
    total_waste_avoided_kg: float = 0.0
    total_co2e_avoided_kg: float = 0.0
    total_money_saved_usd: float = 0.0
    meals_planned_count: int = 0
    safety_vetoes_prevented: int = 0
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class ShoppingItem(BaseModel):
    id: str
    name: str
    category: ItemCategory = ItemCategory.PANTRY
    quantity: float
    unit: str
    estimated_cost: float = 0.0
    recipe_references: List[str] = Field(default_factory=list)
    is_purchased: bool = False
    safe_substitutes: List[str] = Field(default_factory=list)

class ShoppingList(BaseModel):
    id: str
    household_id: str
    items: List[ShoppingItem] = Field(default_factory=list)
    total_estimated_cost: float = 0.0
    requires_approval: bool = True
    approved_by_user: bool = False
    updated_at: datetime = Field(default_factory=datetime.utcnow)
