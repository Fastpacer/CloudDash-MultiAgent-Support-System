from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime


class HandoverPayload(BaseModel):

    source_agent: str

    target_agent: str

    handover_reason: str

    conversation_summary: str

    extracted_entities: Dict[str, Any] = Field(
        default_factory=dict
    )

    conversation_history: List[Dict[str, str]] = Field(
        default_factory=list
    )

    priority: str = "normal"

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )