def detect_possible_hallucination(
    response: str,
    citations,
):

    # ---------------------------------------------------
    # No KB Sources
    # ---------------------------------------------------

    if not citations:

        return True

    # ---------------------------------------------------
    # Grounded Uncertainty Handling
    # ---------------------------------------------------

    grounded_uncertainty_phrases = [
        "verified information unavailable",
        "kb does not provide",
        "unable to verify",
    ]

    lowered = response.lower()

    for phrase in grounded_uncertainty_phrases:

        if phrase in lowered:

            return False

    return False