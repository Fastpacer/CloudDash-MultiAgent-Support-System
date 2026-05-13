import streamlit as st

from streamlit_app.components import (

    render_citations,

    render_trace_id,

    render_escalation_banner,

    render_workflow,

    render_agents_used,

    render_handover_count,

    render_agent_badge,

    render_workflow_metrics,

    render_response_divider,
)

from app.memory.conversation_store import (
    load_conversation_history,
)

from streamlit_app.session_manager import (
    create_new_conversation,
)


# ---------------------------------------------------
# Sidebar Conversation Manager
# ---------------------------------------------------

def render_conversation_sidebar():

    with st.sidebar:

        st.divider()

        st.subheader(
            "Conversations"
        )

        # -------------------------------------------
        # New Conversation
        # -------------------------------------------

        if st.button(
            "➕ New Conversation"
        ):

            create_new_conversation()

            st.rerun()

        st.divider()

        # -------------------------------------------
        # Previous Conversations
        # -------------------------------------------

        conversations = (
            st.session_state.get(
                "conversation_history",
                [],
            )
        )

        if not conversations:

            st.caption(
                "No previous conversations"
            )

        for conversation_id in conversations:

            button_label = (
                conversation_id[:12]
                + "..."
            )

            if st.button(
                button_label,
                key=conversation_id,
            ):

                history = (
                    load_conversation_history(
                        conversation_id
                    )
                )

                # -----------------------------------
                # Restore Conversation
                # -----------------------------------

                st.session_state.chat_history = []

                for message in history:

                    st.session_state.chat_history.append(
                        {
                            "role": (
                                message.role
                            ),

                            "content": (
                                message.content
                            ),

                            "trace_id": getattr(
                                message,
                                "trace_id",
                                "N/A",
                            ),

                            "citations": getattr(
                                message,
                                "citations",
                                [],
                            ),

                            "completed_agents": getattr(
                                message,
                                "completed_agents",
                                [],
                            ),

                            "handover_count": getattr(
                                message,
                                "handover_count",
                                0,
                            ),

                            "active_agent": getattr(
                                message,
                                "active_agent",
                                None,
                            ),

                            "total_agents": getattr(
                                message,
                                "total_agents",
                                0,
                            ),

                            "escalation_required": getattr(
                                message,
                                "escalation_required",
                                False,
                            ),
                        }
                    )

                st.session_state.conversation_id = (
                    conversation_id
                )

                st.rerun()


# ---------------------------------------------------
# Render Chat History
# ---------------------------------------------------

def render_chat_history():

    for chat in (
        st.session_state.chat_history
    ):

        with st.chat_message(
            chat["role"]
        ):

            # ---------------------------------------
            # Main Response
            # ---------------------------------------

            st.markdown(
                chat["content"]
            )

            # ---------------------------------------
            # Assistant Metadata
            # ---------------------------------------

            if (
                chat["role"]
                == "assistant"
            ):

                render_response_divider()

                # -----------------------------------
                # Workflow
                # -----------------------------------

                render_workflow(
                    chat.get(
                        "completed_agents",
                        [],
                    )
                )

                # -----------------------------------
                # Agents Used
                # -----------------------------------

                render_agents_used(
                    chat.get(
                        "completed_agents",
                        [],
                    )
                )

                # -----------------------------------
                # Workflow Metrics
                # -----------------------------------

                render_workflow_metrics(
                    total_agents=chat.get(
                        "total_agents",
                        0,
                    ),

                    total_handovers=chat.get(
                        "handover_count",
                        0,
                    ),
                )

                # -----------------------------------
                # Active Agent
                # -----------------------------------

                render_agent_badge(
                    chat.get(
                        "active_agent",
                        None,
                    )
                )

                # -----------------------------------
                # Citations
                # -----------------------------------

                render_citations(
                    chat.get(
                        "citations",
                        [],
                    )
                )

                # -----------------------------------
                # Handover Count
                # -----------------------------------

                render_handover_count(
                    chat.get(
                        "handover_count",
                        0,
                    )
                )

                # -----------------------------------
                # Trace ID
                # -----------------------------------

                render_trace_id(
                    chat.get(
                        "trace_id",
                        "N/A",
                    )
                )

                # -----------------------------------
                # Escalation
                # -----------------------------------

                if chat.get(
                    "escalation_required",
                    False,
                ):

                    render_escalation_banner()

                render_response_divider()