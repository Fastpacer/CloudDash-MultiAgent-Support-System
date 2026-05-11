import streamlit as st

from streamlit_app.components import (
    render_citations,
    render_trace_id,
    render_escalation_banner,
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

                render_citations(
                    chat.get(
                        "citations",
                        [],
                    )
                )

                render_trace_id(
                    chat.get(
                        "trace_id",
                        "N/A",
                    )
                )

                if chat.get(
                    "escalation_required",
                    False,
                ):

                    render_escalation_banner()