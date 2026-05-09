from app.agents.base_agent import BaseAgent

from app.orchestration.state import (
    ConversationState,
    ConversationMessage,
)

from app.observability.logger import logger


class EscalationAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            agent_name="escalation_agent"
        )

    def process(
        self,
        state: ConversationState,
    ) -> ConversationState:

        logger.info(
            "escalation_triggered",
            trace_id=state.trace_id,
        )

        escalation_message = """
Your issue requires escalation to a human support specialist.

A priority support ticket has been generated.

Our escalation team will review:
- account activity
- technical diagnostics
- relevant billing history

You will receive a follow-up shortly.
"""

        state.escalation_required = True

        state.messages.append(
            ConversationMessage(
                role="assistant",
                content=escalation_message,
            )
        )

        return state