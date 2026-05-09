import streamlit as st
from uuid import uuid4


# ---------------------------------------------------
# Initialize Session State
# ---------------------------------------------------

def initialize_session():

    # -----------------------------------------------
    # Conversation ID
    # -----------------------------------------------

    if (
        "conversation_id"
        not in st.session_state
    ):

        st.session_state.conversation_id = (
            str(uuid4())
        )

    # -----------------------------------------------
    # Chat History
    # -----------------------------------------------

    if (
        "chat_history"
        not in st.session_state
    ):

        st.session_state.chat_history = []

    # -----------------------------------------------
    # Trace History
    # -----------------------------------------------

    if (
        "trace_history"
        not in st.session_state
    ):

        st.session_state.trace_history = []

    # -----------------------------------------------
    # Escalation State
    # -----------------------------------------------

    if (
        "escalation_triggered"
        not in st.session_state
    ):

        st.session_state.escalation_triggered = (
            False
        )