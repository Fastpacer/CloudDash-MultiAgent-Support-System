import json

from pathlib import Path

from app.orchestration.state import (
    ConversationMessage,
)


# ---------------------------------------------------
# Base Storage Directory
# ---------------------------------------------------

BASE_DIR = Path(
    "data/conversations"
)

BASE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------
# Get Conversation File Path
# ---------------------------------------------------

def get_conversation_path(
    conversation_id: str,
):

    return (
        BASE_DIR
        / f"{conversation_id}.json"
    )


# ---------------------------------------------------
# Save Message
# ---------------------------------------------------

def save_message(
    conversation_id: str,
    message: ConversationMessage,
):

    path = get_conversation_path(
        conversation_id
    )

    existing_messages = (
        load_conversation_history(
            conversation_id
        )
    )

    existing_messages.append(
        message
    )

    serialized_messages = []

    for msg in existing_messages:

        serialized_messages.append(
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": (
                    msg.timestamp.isoformat()
                ),
            }
        )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            serialized_messages,
            file,
            indent=2,
        )


# ---------------------------------------------------
# Load Conversation History
# ---------------------------------------------------

def load_conversation_history(
    conversation_id: str,
):

    path = get_conversation_path(
        conversation_id
    )

    if not path.exists():

        return []

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        raw_messages = json.load(
            file
        )

    messages = []

    for msg in raw_messages:

        messages.append(
            ConversationMessage(
                role=msg["role"],
                content=msg["content"],
            )
        )

    return messages


# ---------------------------------------------------
# List User Conversations
# ---------------------------------------------------

def list_conversations():

    conversations = []

    for file in BASE_DIR.glob(
        "*.json"
    ):

        conversations.append(
            file.stem
        )

    return conversations