from typing import Tuple


BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "system prompt",
    "reveal hidden prompt",
    "bypass security",
    "act as root",
    "jailbreak",
    "developer instructions",
]


def validate_input(
    user_input: str,
) -> Tuple[bool, str]:

    lowered = user_input.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in lowered:

            return (
                False,
                f"Blocked prompt injection pattern: {pattern}",
            )

    return (
        True,
        "Input validated successfully",
    )