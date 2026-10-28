"""
Conversational Orchestrator Agent: Routes user intents, enforces human confirmation
action guardrails before executing mutations, and declines medical diagnoses.
"""

import time
import uuid
from typing import Dict, Any, List
from app.models.telemetry import AgentName
from app.security.audit_logger import audit_logger
from app.security.pii_redactor import pii_redactor
from app.security.injection_guard import injection_guard
from app.agents.meal_planner import meal_planner_agent
from app.agents.procurement import procurement_agent
from app.agents.sustainability import sustainability_agent
from app.services.storage_service import storage_service

class ConversationalOrchestrator:
    def __init__(self):
        self.agent_name = AgentName.ORCHESTRATOR

    async def chat(
        self,
        household_id: str,
        message: str,
        correlation_id: str = None
    ) -> Dict[str, Any]:
        cid = correlation_id or str(uuid.uuid4())
        
        # 1. PII Redaction
        sanitized_msg, _ = pii_redactor.redact(message)

        # 2. Injection Guard
        is_threat, patterns = injection_guard.check_adversarial_threat(sanitized_msg)
        if is_threat:
            audit_logger.record_decision(
                household_id=household_id,
                agent_name=self.agent_name,
                action="chat_injection_blocked",
                input_summary=sanitized_msg[:80],
                output_summary=f"Neutralized threat patterns: {patterns}",
                correlation_id=cid,
                safety_veto_applied=True
            )
            return {
                "response": "⚠️ Request declined: Adversarial prompt instruction detected and blocked.",
                "action_proposal": None,
                "safety_declined": True
            }

        # 3. Medical Diagnosis / Prescription Diet Intercept
        med_keywords = ["cure my diabetes", "diagnose", "cure hypertension", "prescribe diet", "treat my allergy"]
        if any(kw in sanitized_msg.lower() for kw in med_keywords):
            disclaimer = (
                "Notice: PantryPilot provides household food and inventory intelligence, not medical diagnosis "
                "or clinical nutrition prescriptions. Please consult your physician or registered dietitian for medical advice."
            )
            return {
                "response": disclaimer,
                "action_proposal": None,
                "is_medical_disclaimer": True
            }

        # 4. Intent Routing
        lower = sanitized_msg.lower()
        
        # Meal planning query
        if any(w in lower for w in ["cook", "dinner", "recipe", "meal", "expiring"]):
            plan_res = await meal_planner_agent.generate_plan(household_id, correlation_id=cid)
            recipes = plan_res.get("recipes", [])
            if recipes:
                first = recipes[0]
                resp = (
                    f"I recommend cooking **{first['title']}**! It rescues expiring ingredients "
                    f"({', '.join(first['expiring_items_used'])}) and is verified safe for all household members."
                )
            else:
                resp = "I checked our live pantry, but couldn't find recipes that satisfy all allergen and medical constraints."
                
            return {
                "response": resp,
                "action_proposal": {
                    "type": "CONFIRM_MEAL_PLAN",
                    "title": "Adopt Waste-Minimizing Meal Plan",
                    "details": f"Generated plan with {len(recipes)} verified safe recipes.",
                    "requires_user_approval": True
                }
            }

        # Deletion request -> Human in the Loop approval card
        elif "delete" in lower or "remove item" in lower or "clear inventory" in lower:
            return {
                "response": "I can remove items from your pantry, but requires your explicit confirmation.",
                "action_proposal": {
                    "type": "CONFIRM_DELETE_INVENTORY",
                    "title": "Confirm Pantry Item Deletion",
                    "details": "This will permanently remove the selected item from household inventory.",
                    "requires_user_approval": True
                }
            }

        # Impact / Sustainability inquiry
        elif any(w in lower for w in ["waste", "savings", "carbon", "co2", "saved"]):
            impact = sustainability_agent.get_household_impact(household_id)
            resp = (
                f"🌱 The Sharma Household has avoided **{impact['waste_avoided_kg']} kg** of food waste, "
                f"prevented **{impact['co2e_avoided_kg']} kg CO2e**, and saved **${impact['money_saved_usd']}**!"
            )
            return {
                "response": resp,
                "action_proposal": None
            }

        # General friendly assistant fallback
        return {
            "response": (
                "Hello! I am your PantryPilot food intelligence assistant. I can help plan meals using expiring groceries, "
                "verify recipes against household allergen constraints, or compile smart shopping lists. What would you like to do?"
            ),
            "action_proposal": None
        }

orchestrator_agent = ConversationalOrchestrator()
