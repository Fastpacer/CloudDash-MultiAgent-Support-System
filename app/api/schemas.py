from pydantic import (
    BaseModel,
    Field,
)

from typing import (
    List,
)

from datetime import (
    datetime,
)


# ---------------------------------------------------
# Incoming Chat Request
# ---------------------------------------------------

class MessageRequest(
    BaseModel
):

    message: str

    conversation_id: str

    username: str


# ---------------------------------------------------
# Chat Response
# ---------------------------------------------------

class MessageResponse(
    BaseModel
):

    response: str

    active_agent: str

    citations: List[
        str
    ] = Field(
        default_factory=list
    )

    escalation_required: bool = (
        False
    )

    trace_id: str

    # -----------------------------------------------
    # Workflow Visibility
    # -----------------------------------------------

    completed_agents: List[
        str
    ] = Field(
        default_factory=list
    )

    handover_count: int = 0


# ---------------------------------------------------
# Conversation Initialization
# ---------------------------------------------------

class ConversationStartResponse(
    BaseModel
):

    conversation_id: str

    trace_id: str

    created_at: datetime


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------

class HealthResponse(
    BaseModel
):

    status: str

    version: str