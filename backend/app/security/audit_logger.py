"""
Audit Logger and Telemetry Service.
Maintains an immutable memory/log audit trail of agent actions,
latency, tokens, estimated cost, and deterministic safety vetoes.
"""

import uuid
from typing import List, Optional
from datetime import datetime
from app.models.telemetry import AuditLogEntry, AgentName

# Cost constants (USD per 1M tokens) - based on current Vertex AI Gemini pricing
GEMINI_FLASH_INPUT_COST = 0.075 / 1_000_000
GEMINI_FLASH_OUTPUT_COST = 0.30 / 1_000_000
GEMINI_PRO_INPUT_COST = 1.25 / 1_000_000
GEMINI_PRO_OUTPUT_COST = 5.00 / 1_000_000

class AuditLogger:
    def __init__(self):
        self._logs: List[AuditLogEntry] = []

    def record_decision(
        self,
        household_id: str,
        agent_name: AgentName,
        action: str,
        input_summary: str,
        output_summary: str,
        correlation_id: Optional[str] = None,
        safety_veto_applied: bool = False,
        tokens_used: int = 0,
        latency_ms: float = 0.0,
        model_name: Optional[str] = None
    ) -> AuditLogEntry:
        cid = correlation_id or str(uuid.uuid4())
        
        # Calculate cost
        cost = 0.0
        if model_name and "pro" in model_name.lower():
            cost = tokens_used * GEMINI_PRO_INPUT_COST
        elif model_name:
            cost = tokens_used * GEMINI_FLASH_INPUT_COST

        entry = AuditLogEntry(
            id=str(uuid.uuid4()),
            correlation_id=cid,
            household_id=household_id,
            agent_name=agent_name,
            action=action,
            input_summary=input_summary[:200],
            output_summary=output_summary[:200],
            safety_veto_applied=safety_veto_applied,
            tokens_used=tokens_used,
            latency_ms=latency_ms,
            cost_usd=round(cost, 6),
            timestamp=datetime.utcnow()
        )
        self._logs.append(entry)
        return entry

    def get_logs_for_household(self, household_id: str, limit: int = 50) -> List[AuditLogEntry]:
        matched = [entry for entry in self._logs if entry.household_id == household_id]
        return sorted(matched, key=lambda x: x.timestamp, reverse=True)[:limit]

    def get_all_logs(self, limit: int = 100) -> List[AuditLogEntry]:
        return sorted(self._logs, key=lambda x: x.timestamp, reverse=True)[:limit]

audit_logger = AuditLogger()
