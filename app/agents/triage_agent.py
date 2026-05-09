from langchain_core.prompts import ChatPromptTemplate

from app.agents.base_agent import BaseAgent

from app.orchestration.state import (
    ConversationState,
)

from app.utils.llm_factory import get_llm
from app.observability.logger import logger


class TriageAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            agent_name="triage_agent"
        )

        self.llm = get_llm()

        self.prompt = ChatPromptTemplate.from_template(
            """
You are the CloudDash Triage Agent.

Classify the user request into EXACTLY ONE category.

Available categories:
- technical_agent
- billing_agent
- escalation_agent

Routing Rules:

Technical:
- alerts
- integrations
- APIs
- SSO
- dashboards
- sync failures
- infrastructure issues

Billing:
- invoices
- refunds
- pricing
- subscriptions
- upgrades
- payments
- duplicate charges

Escalation:
- legal threats
- production outages
- severe frustration
- data loss
- urgent manager requests

IMPORTANT:
Return ONLY the agent name.
Do not explain reasoning.

User Message:
{message}
"""
        )

    def process(
        self,
        state: ConversationState,
    ) -> ConversationState:

        latest_message = (
            state.messages[-1].content
        )

        logger.info(
            "triage_started",
            trace_id=state.trace_id,
        )

        chain = self.prompt | self.llm

        response = chain.invoke(
            {
                "message": latest_message
            }
        )

        detected_agent = (
            response.content
            .strip()
            .lower()
        )

        valid_agents = {
            "technical_agent",
            "billing_agent",
            "escalation_agent",
        }

        if detected_agent not in valid_agents:

            detected_agent = (
                "escalation_agent"
            )

        logger.info(
            "triage_completed",
            selected_agent=detected_agent,
        )

        state.current_agent = (
            detected_agent
        )

        return state