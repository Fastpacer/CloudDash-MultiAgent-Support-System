import streamlit as st

from uuid import uuid4

from app.memory.session_manager import (
    load_user_conversations,
)


# ---------------------------------------------------
# Initialize Session State
# ---------------------------------------------------

def initialize_session():

    # -----------------------------------------------
    # Authentication State
    # -----------------------------------------------

    if (
        "authenticated"
        not in st.session_state
    ):

        st.session_state.authenticated = (
            False
        )

    # -----------------------------------------------
    # Username
    # -----------------------------------------------

    if (
        "username"
        not in st.session_state
    ):

        st.session_state.username = (
            None
        )

    # -----------------------------------------------
    # User ID
    # -----------------------------------------------

    if (
        "user_id"
        not in st.session_state
    ):

        st.session_state.user_id = (
            None
        )

    # -----------------------------------------------
    # Active Conversation ID
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
    # Conversation History
    # -----------------------------------------------

    if (
        "conversation_history"
        not in st.session_state
    ):

        st.session_state.conversation_history = []

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


# ---------------------------------------------------
# Create New Conversation
# ---------------------------------------------------

def create_new_conversation():

    st.session_state.conversation_id = (
        str(uuid4())
    )

    st.session_state.chat_history = []


# ---------------------------------------------------
# Logout User
# ---------------------------------------------------

def logout_user():

    st.session_state.authenticated = (
        False
    )

    st.session_state.username = None

    st.session_state.user_id = None

    st.session_state.chat_history = []

    st.session_state.conversation_history = []

    st.session_state.conversation_id = (
        str(uuid4())
    )


# ---------------------------------------------------
# Load User Conversations To Session
# ---------------------------------------------------

def load_user_conversations_to_session(
    username: str,
):

    conversations = (
        load_user_conversations(
            username
        )
    )

    st.session_state.conversation_history = (
        conversations
    )