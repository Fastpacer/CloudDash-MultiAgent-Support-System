from app.handover.protocol import (
    HandoverPayload,
)

from app.observability.logger import logger


def log_handover_event(
    payload: HandoverPayload,
):

    logger.info(
        "agent_handover",
        source_agent=payload.source_agent,
        target_agent=payload.target_agent,
        reason=payload.handover_reason,
        priority=payload.priority,
    )