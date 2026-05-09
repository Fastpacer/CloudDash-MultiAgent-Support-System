from typing import Tuple


BLOCKED_PHRASES = [
    "100% guaranteed",
    "definitely always works",
    "this can never fail",
]


def validate_output(
    response: str,
    citations,
) -> Tuple[bool, str]:

    lowered = response.lower()

    # ---------------------------------------------------
    # Unsupported Certainty Detection
    # ---------------------------------------------------

    for phrase in BLOCKED_PHRASES:

        if phrase in lowered:

            return (
                False,
                f"Unsafe certainty phrase detected: {phrase}",
            )

    # ---------------------------------------------------
    # Missing Citations
    # ---------------------------------------------------

    if not citations:

        return (
            False,
            "No citations attached to response",
        )

    return (
        True,
        "Output validation passed",
    )