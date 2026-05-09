from app.agents.registry import (
    agent_registry,
)

from app.orchestration.state import (
    ConversationState,
)

from app.observability.logger import logger


def route_conversation(
    state: ConversationState,
):

    logger.info(
        "routing_started",
        current_agent=state.current_agent,
    )

    agent = agent_registry.get(
        state.current_agent
    )

    if not agent:
        raise ValueError(
            f"Unknown agent: {state.current_agent}"
        )

    updated_state = agent.process(
        state
    )

    logger.info(
        "routing_completed",
        next_agent=updated_state.current_agent,
    )

    return updated_state