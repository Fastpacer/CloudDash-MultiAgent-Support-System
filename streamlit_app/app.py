import streamlit as st

from app.orchestration.graph import (
    graph,
)

from app.orchestration.state import (
    ConversationState,
    ConversationMessage,
)

from streamlit_app.session_manager import (
    initialize_session,
)

from streamlit_app.components import (
    render_header,
    render_sidebar,
)

from streamlit_app.chat_ui import (
    render_chat_history,
)

from app.guardrails.input_guard import (
    validate_input,
)

from app.observability.logger import (
    logger,
)

from app.observability.metrics import (
    increment_metric,
)

from app.observability.tracing import (
    start_trace,
    end_trace,
)


# ---------------------------------------------------
# Streamlit Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title=(
        "CloudDash AI Support"
    ),
    page_icon="☁️",
    layout="wide",
)


# ---------------------------------------------------
# Initialize Session
# ---------------------------------------------------

initialize_session()


# ---------------------------------------------------
# Render UI
# ---------------------------------------------------

render_sidebar()

render_header()

render_chat_history()


# ---------------------------------------------------
# Chat Input
# ---------------------------------------------------

user_input = st.chat_input(
    "Describe your issue..."
)


# ---------------------------------------------------
# Process User Message
# ---------------------------------------------------

if user_input:

    trace_start = start_trace()

    increment_metric(
        "total_requests"
    )

    # -----------------------------------------------
    # Display User Message
    # -----------------------------------------------

    st.chat_message(
        "user"
    ).markdown(user_input)

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    # -----------------------------------------------
    # Input Guardrails
    # -----------------------------------------------

    is_valid, reason = validate_input(
        user_input
    )

    if not is_valid:

        increment_metric(
            "blocked_requests"
        )

        blocked_response = (
            "Request blocked by "
            "security guardrails."
        )

        st.chat_message(
            "assistant"
        ).markdown(blocked_response)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": blocked_response,
                "citations": [],
                "trace_id": "BLOCKED",
                "escalation_required": False,
            }
        )

        st.stop()

    # -----------------------------------------------
    # Conversation State
    # -----------------------------------------------

    conversation_state = (
        ConversationState(
            trace_id=(
                st.session_state
                .conversation_id
            ),
            conversation_id=(
                st.session_state
                .conversation_id
            ),
            messages=[
                ConversationMessage(
                    role="user",
                    content=user_input,
                )
            ],
        )
    )

    # -----------------------------------------------
    # Workflow Execution
    # -----------------------------------------------

    with st.spinner(
        "Analyzing request..."
    ):

        result = graph.invoke(
            conversation_state
        )

    # -----------------------------------------------
    # Escalation Metrics
    # -----------------------------------------------

    if result[
        "escalation_required"
    ]:

        increment_metric(
            "escalation_requests"
        )

    # -----------------------------------------------
    # Extract Final Response
    # -----------------------------------------------

    assistant_response = (
        result["messages"][-1]
        .content
    )

    citations = result.get(
        "retrieved_docs",
        [],
    )

    trace_id = result.get(
        "trace_id",
        "N/A",
    )

    escalation_required = (
        result.get(
            "escalation_required",
            False,
        )
    )

    # -----------------------------------------------
    # Render Assistant Response
    # -----------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            assistant_response
        )

        if citations:

            with st.expander(
                "Sources"
            ):

                for citation in citations:

                    st.markdown(
                        f"- {citation}"
                    )

        st.caption(
            f"Trace ID: {trace_id}"
        )

        if escalation_required:

            st.error(
                (
                    "⚠️ Escalation "
                    "Required"
                )
            )

    # -----------------------------------------------
    # Persist Chat History
    # -----------------------------------------------

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": assistant_response,
            "citations": citations,
            "trace_id": trace_id,
            "escalation_required": (
                escalation_required
            ),
        }
    )

    # -----------------------------------------------
    # Workflow Timing
    # -----------------------------------------------

    duration = end_trace(
        trace_start
    )

    logger.info(
        "streamlit_workflow_completed",
        duration_seconds=duration,
    )