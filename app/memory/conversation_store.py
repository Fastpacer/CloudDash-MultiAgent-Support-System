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
# Get User Conversation Directory
# ---------------------------------------------------

def get_user_conversation_dir(
    username: str,
):

    user_dir = (
        BASE_DIR
        / username
        / "conversations"
    )

    user_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return user_dir


# ---------------------------------------------------
# Get Conversation File Path
# ---------------------------------------------------

def get_conversation_path(
    username: str,
    conversation_id: str,
):

    user_dir = get_user_conversation_dir(
        username
    )

    return (
        user_dir
        / f"{conversation_id}.json"
    )


# ---------------------------------------------------
# Save Message
# ---------------------------------------------------

def save_message(
    username: str,
    conversation_id: str,
    message: ConversationMessage,
):

    path = get_conversation_path(
        username,
        conversation_id
    )

    existing_messages = (
        load_conversation_history(
            username,
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
    username: str,
    conversation_id: str,
):

    path = get_conversation_path(
        username,
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

def list_user_conversations(
    username: str,
):

    user_dir = get_user_conversation_dir(
        username
    )

    conversations = []

    for file in user_dir.glob(
        "*.json"
    ):

        conversations.append(
            file.stem
        )

    return conversations