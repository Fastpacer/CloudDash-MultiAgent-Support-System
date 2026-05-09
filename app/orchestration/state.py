from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


# ---------------------------------------------------
# Conversation Message
# ---------------------------------------------------

class ConversationMessage(BaseModel):

    role: str

    content: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )


# ---------------------------------------------------
# Conversation State
# ---------------------------------------------------

class ConversationState(BaseModel):

    # ---------------------------------------------------
    # Core Metadata
    # ---------------------------------------------------

    trace_id: str

    conversation_id: str

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    # ---------------------------------------------------
    # Active Agent
    # ---------------------------------------------------

    current_agent: str = "triage_agent"

    # ---------------------------------------------------
    # Messages
    # ---------------------------------------------------

    messages: List[ConversationMessage] = Field(
        default_factory=list
    )

    # ---------------------------------------------------
    # Retrieval Metadata
    # ---------------------------------------------------

    retrieved_docs: List[str] = Field(
        default_factory=list
    )

    # ---------------------------------------------------
    # NLP Metadata
    # ---------------------------------------------------

    extracted_entities: Dict[str, Any] = Field(
        default_factory=dict
    )

    current_intent: Optional[str] = None

    sentiment: Optional[str] = None

    # ---------------------------------------------------
    # Escalation
    # ---------------------------------------------------

    escalation_required: bool = False