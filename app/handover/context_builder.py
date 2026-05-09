from app.handover.protocol import (
    HandoverPayload,
)

from app.orchestration.state import (
    ConversationState,
)


def build_handover_payload(
    state: ConversationState,
    source_agent: str,
    target_agent: str,
    reason: str,
):

    recent_messages = [
        {
            "role": msg.role,
            "content": msg.content,
        }
        for msg in state.messages[-6:]
    ]

    summary = "\n".join(
        [
            f"{msg.role}: {msg.content}"
            for msg in state.messages[-4:]
        ]
    )

    return HandoverPayload(
        source_agent=source_agent,
        target_agent=target_agent,
        handover_reason=reason,
        conversation_summary=summary,
        extracted_entities=state.extracted_entities,
        conversation_history=recent_messages,
        priority="high"
        if state.escalation_required
        else "normal",
    )