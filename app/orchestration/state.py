from typing import (
    List,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
)

from datetime import datetime


# ---------------------------------------------------
# Conversation Message
# ---------------------------------------------------

class ConversationMessage(
    BaseModel,
):

    role: str

    content: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )


# ---------------------------------------------------
# Handover Event
# ---------------------------------------------------

class HandoverEvent(
    BaseModel,
):

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )

    source_agent: str

    target_agent: str

    reason: str

    context_snapshot: str


# ---------------------------------------------------
# Conversation State
# ---------------------------------------------------

class ConversationState(
    BaseModel,
):

    trace_id: str

    conversation_id: str

    messages: List[
        ConversationMessage
    ] = Field(
        default_factory=list
    )

    # -----------------------------------------------
    # Agent Workflow
    # -----------------------------------------------

    current_agent: Optional[
        str
    ] = None

    pending_agents: List[
        str
    ] = Field(
        default_factory=list
    )

    completed_agents: List[
        str
    ] = Field(
        default_factory=list
    )

    # -----------------------------------------------
    # Retrieval
    # -----------------------------------------------

    retrieved_docs: List[
        str
    ] = Field(
        default_factory=list
    )

    # -----------------------------------------------
    # Escalation
    # -----------------------------------------------

    escalation_required: bool = (
        False
    )

    # -----------------------------------------------
    # Handover Tracking
    # -----------------------------------------------

    handover_history: List[
        HandoverEvent
    ] = Field(
        default_factory=list
    )

    # -----------------------------------------------
    # Extracted Entities
    # -----------------------------------------------

    extracted_entities: dict = (
        Field(default_factory=dict)
    )