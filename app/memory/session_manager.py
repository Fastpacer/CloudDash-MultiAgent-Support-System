import json

from pathlib import Path
from uuid import uuid4


# ---------------------------------------------------
# Base User Storage
# ---------------------------------------------------

USERS_DIR = Path(
    "data/users"
)

USERS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------
# Create Conversation ID
# ---------------------------------------------------

def create_conversation_id():

    return str(uuid4())


# ---------------------------------------------------
# Create User ID
# ---------------------------------------------------

def create_user_id():

    return str(uuid4())


# ---------------------------------------------------
# Get User File Path
# ---------------------------------------------------

def get_user_path(
    username: str,
):

    return (
        USERS_DIR
        / f"{username}.json"
    )


# ---------------------------------------------------
# User Exists
# ---------------------------------------------------

def user_exists(
    username: str,
):

    return get_user_path(
        username
    ).exists()


# ---------------------------------------------------
# Register User
# ---------------------------------------------------

def register_user(
    username: str,
    password: str,
):

    path = get_user_path(
        username
    )

    if path.exists():

        return False

    user_data = {
        "user_id": (
            create_user_id()
        ),
        "username": username,
        "password": password,
        "conversations": [],
    }

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            user_data,
            file,
            indent=2,
        )

    return True


# ---------------------------------------------------
# Authenticate User
# ---------------------------------------------------

def authenticate_user(
    username: str,
    password: str,
):

    path = get_user_path(
        username
    )

    if not path.exists():

        return None

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        user_data = json.load(
            file
        )

    if (
        user_data["password"]
        != password
    ):

        return None

    return user_data


# ---------------------------------------------------
# Attach Conversation To User
# ---------------------------------------------------

def attach_conversation_to_user(
    username: str,
    conversation_id: str,
):

    path = get_user_path(
        username
    )

    if not path.exists():

        return

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        user_data = json.load(
            file
        )

    if (
        conversation_id
        not in user_data[
            "conversations"
        ]
    ):

        user_data[
            "conversations"
        ].append(
            conversation_id
        )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            user_data,
            file,
            indent=2,
        )


# ---------------------------------------------------
# Load User Conversations
# ---------------------------------------------------

def load_user_conversations(
    username: str,
):

    path = get_user_path(
        username
    )

    if not path.exists():

        return []

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        user_data = json.load(
            file
        )

    return user_data.get(
        "conversations",
        [],
    )