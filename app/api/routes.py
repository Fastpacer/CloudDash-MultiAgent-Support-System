from fastapi import APIRouter

from uuid import uuid4

from datetime import datetime

from app.orchestration.graph import (
    graph,
)

from app.orchestration.state import (
    ConversationState,
    ConversationMessage,
)

from app.api.schemas import (
    ConversationStartResponse,
    HealthResponse,
    MessageRequest,
    MessageResponse,
)

from app.guardrails.input_guard import (
    validate_input,
)

from app.memory.conversation_store import (
    save_message,
    load_conversation_history,
)

from app.memory.session_manager import (
    create_conversation_id,
)

from app.observability.metrics import (
    increment_metric,
)

from app.observability.tracing import (
    start_trace,
    end_trace,
)

from app.observability.logger import (
    logger,
)


router = APIRouter()


# ---------------------------------------------------
# Root Endpoint
# ---------------------------------------------------

@router.get(
    "/",
    tags=["Root"],
)
async def root():

    return {
        "message": (
            "CloudDash Multi-Agent "
            "Support System API"
        )
    }


# ---------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------

@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
)
async def health_check():

    return HealthResponse(
        status="healthy",
        version="1.0.0",
    )


# ---------------------------------------------------
# Conversation Initialization
# ---------------------------------------------------

@router.post(
    "/conversation/start",
    response_model=ConversationStartResponse,
    tags=["Conversation"],
)
async def start_conversation():

    conversation_id = (
        create_conversation_id()
    )

    trace_id = str(uuid4())

    return ConversationStartResponse(
        conversation_id=conversation_id,
        trace_id=trace_id,
        created_at=datetime.utcnow(),
    )


# ---------------------------------------------------
# Main Chat Endpoint
# ---------------------------------------------------

@router.post(
    "/chat",
    response_model=MessageResponse,
    tags=["Chat"],
)
async def chat_endpoint(
    request: MessageRequest,
):

    # ---------------------------------------------------
    # Request Metadata
    # ---------------------------------------------------

    trace_id = str(uuid4())

    trace_start = start_trace()

    increment_metric(
        "total_requests"
    )

    conversation_id = (
        request.conversation_id
    )

    logger.info(
        "chat_request_received",
        trace_id=trace_id,
        conversation_id=conversation_id,
    )

    # ---------------------------------------------------
    # Input Guardrails
    # ---------------------------------------------------

    is_valid, reason = validate_input(
        request.message
    )

    if not is_valid:

        increment_metric(
            "blocked_requests"
        )

        logger.warning(
            "guardrail_blocked_request",
            trace_id=trace_id,
            reason=reason,
        )

        return MessageResponse(
            response=(
                "Request blocked by "
                "security guardrails."
            ),
            active_agent="guardrails",
            citations=[],
            escalation_required=False,
            trace_id=trace_id,
            completed_agents=[],
            handover_count=0,
        )

    # ---------------------------------------------------
    # Load Conversation History
    # ---------------------------------------------------

    history = load_conversation_history(
        conversation_id
    )

    logger.info(
        "conversation_history_loaded",
        trace_id=trace_id,
        history_length=len(
            history
        ),
    )

    # ---------------------------------------------------
    # Initialize Conversation State
    # ---------------------------------------------------

    state = ConversationState(
        trace_id=trace_id,
        conversation_id=conversation_id,
        messages=history + [
            ConversationMessage(
                role="user",
                content=request.message,
            )
        ],
    )

    # ---------------------------------------------------
    # Execute Workflow
    # ---------------------------------------------------

    result = graph.invoke(
        state
    )

    # ---------------------------------------------------
    # Escalation Metrics
    # ---------------------------------------------------

    if result[
        "escalation_required"
    ]:

        increment_metric(
            "escalation_requests"
        )

    # ---------------------------------------------------
    # Persist Messages
    # ---------------------------------------------------

    for message in result[
        "messages"
    ]:

        save_message(
            conversation_id,
            message,
        )

    logger.info(
        "conversation_persisted",
        trace_id=trace_id,
        total_messages=len(
            result["messages"]
        ),
    )

    # ---------------------------------------------------
    # Final Assistant Response
    # ---------------------------------------------------

    final_message = (
        result["messages"][-1]
        .content
    )

    # ---------------------------------------------------
    # Trace Completion
    # ---------------------------------------------------

    duration = end_trace(
        trace_start
    )

    logger.info(
        "workflow_completed",
        trace_id=trace_id,
        duration_seconds=duration,
        active_agent=result[
            "current_agent"
        ],
        completed_agents=result[
            "completed_agents"
        ],
        handover_count=len(
            result[
                "handover_history"
            ]
        ),
    )

    # ---------------------------------------------------
    # Structured API Response
    # ---------------------------------------------------

    return MessageResponse(
        response=final_message,

        active_agent=result[
            "current_agent"
        ],

        citations=result[
            "retrieved_docs"
        ],

        escalation_required=result[
            "escalation_required"
        ],

        trace_id=trace_id,

        # -----------------------------------------------
        # Workflow Visibility
        # -----------------------------------------------

        completed_agents=result[
            "completed_agents"
        ],

        handover_count=len(
            result[
                "handover_history"
            ]
        ),
    )