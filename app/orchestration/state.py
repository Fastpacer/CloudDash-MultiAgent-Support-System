from typing import (
    List,
    Optional,
    Dict,
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
# Agent Output
# ---------------------------------------------------

class AgentOutput(
    BaseModel,
):

    agent_name: str

    response: str

    citations: List[
        str
    ] = Field(
        default_factory=list
    )


# ---------------------------------------------------
# Conversation State
# ---------------------------------------------------

class ConversationState(
    BaseModel,
):

    # -----------------------------------------------
    # Core Identity
    # -----------------------------------------------

    trace_id: str

    conversation_id: str

    # -----------------------------------------------
    # Messages
    # -----------------------------------------------

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
    # Agent Task Delegation
    # -----------------------------------------------

    agent_tasks: Dict[
        str,
        str,
    ] = Field(
        default_factory=dict
    )

    # -----------------------------------------------
    # Agent Outputs
    # -----------------------------------------------

    agent_outputs: List[
        AgentOutput
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

    extracted_entities: Dict = (
        Field(default_factory=dict)
    )

    # -----------------------------------------------
    # Workflow Metadata
    # -----------------------------------------------

    workflow_started_at: datetime = (
        Field(
            default_factory=datetime.utcnow
        )
    )

    workflow_completed_at: Optional[
        datetime
    ] = None

    total_handovers: int = 0

    total_agents_invoked: int = 0