from collections import defaultdict

from app.orchestration.state import (
    ConversationMessage,
)


# ---------------------------------------------------
# In-Memory Conversation Store
# ---------------------------------------------------

conversation_store = defaultdict(list)


def save_message(
    conversation_id: str,
    message: ConversationMessage,
):

    conversation_store[
        conversation_id
    ].append(message)


def load_conversation_history(
    conversation_id: str,
):

    return conversation_store.get(
        conversation_id,
        [],
    )