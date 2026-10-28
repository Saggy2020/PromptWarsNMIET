from fastapi import APIRouter
from typing import Dict, Any
from pydantic import BaseModel
from app.agents.orchestrator import orchestrator_agent

router = APIRouter(prefix="/api/assistant", tags=["Assistant"])

class ChatRequest(BaseModel):
    household_id: str
    message: str

@router.post("/chat")
async def chat_with_assistant(payload: ChatRequest) -> Dict[str, Any]:
    return await orchestrator_agent.chat(
        household_id=payload.household_id,
        message=payload.message
    )
