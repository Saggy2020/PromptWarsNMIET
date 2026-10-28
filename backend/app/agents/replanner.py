"""
Re-Planning Agent: Triggers reactive meal plan recalculation
when inventory changes occur (items spoiled, used, or newly added).
"""

import time
import uuid
from typing import Dict, Any, List
from app.models.telemetry import AgentName
from app.security.audit_logger import audit_logger
from app.services.storage_service import storage_service
from app.agents.meal_planner import meal_planner_agent

class ReplannerAgent:
    def __init__(self):
        self.agent_name = AgentName.ORCHESTRATOR

    async def handle_inventory_change(
        self,
        household_id: str,
        change_type: str, # "consumed", "wasted", "added"
        item_name: str
    ) -> Dict[str, Any]:
        cid = str(uuid.uuid4())
        
        # Trigger re-plan
        plan_result = await meal_planner_agent.generate_plan(
            household_id=household_id,
            correlation_id=cid
        )
        
        summary = (
            f"Inventory delta detected: '{item_name}' was marked as {change_type}. "
            f"Re-plan completed: {len(plan_result.get('recipes', []))} safe recipes generated."
        )

        audit_logger.record_decision(
            household_id=household_id,
            agent_name=self.agent_name,
            action="replanner_executed",
            input_summary=f"Item: {item_name}, Delta: {change_type}",
            output_summary=summary,
            correlation_id=cid
        )

        return {
            "replan_triggered": True,
            "change_type": change_type,
            "item_name": item_name,
            "message": summary,
            "updated_plan": plan_result
        }

replanner_agent = ReplannerAgent()
