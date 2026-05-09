import streamlit as st

from streamlit_app.components import (
    render_citations,
    render_trace_id,
    render_escalation_banner,
)


# ---------------------------------------------------
# Render Chat History
# ---------------------------------------------------

def render_chat_history():

    for chat in st.session_state.chat_history:

        with st.chat_message(
            chat["role"]
        ):

            st.markdown(
                chat["content"]
            )

            # ---------------------------------------
            # Citations
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