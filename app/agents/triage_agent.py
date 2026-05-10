from langchain_core.prompts import (
    ChatPromptTemplate,
)

from app.agents.base_agent import (
    BaseAgent,
)

from app.orchestration.state import (
    ConversationState,
)

from app.utils.llm_factory import (
    get_llm,
)

from app.observability.logger import (
    logger,
)

from app.config.config_loader import (
    ROUTING_CONFIG,
)


class TriageAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            agent_name="triage_agent"
        )

        self.llm = get_llm()

        routing_rules = (
            ROUTING_CONFIG[
                "routing"
            ]
        )

        self.prompt = (
            ChatPromptTemplate
            .from_template(
                f"""
You are the CloudDash Triage Agent.

Identify ALL relevant support domains.

ROUTING RULES:

Technical Keywords:
{routing_rules["technical_keywords"]}

Billing Keywords:
{routing_rules["billing_keywords"]}

Escalation Keywords:
{routing_rules["escalation_keywords"]}

IMPORTANT:
- Multiple intents allowed
- Return comma-separated agent names
- No explanations

VALID AGENTS:
technical_agent
billing_agent
escalation_agent

User Message:
{{message}}
"""
            )
        )

    def process(
        self,
        state: ConversationState,
    ) -> ConversationState:

        latest_message = (
            state.messages[-1]
            .content
        )

        logger.info(
            "triage_started",
            trace_id=(
                state.trace_id
            ),
        )

        chain = (
            self.prompt
            | self.llm
        )

        response = chain.invoke(
            {
                "message": (
                    latest_message
                )
            }
        )

        raw_routes = (
            response.content
            .strip()
            .lower()
        )

        routes = [
            route.strip()
            for route in (
                raw_routes.split(",")
            )
            if route.strip()
        ]

        valid_agents = {
            "technical_agent",
            "billing_agent",
            "escalation_agent",
        }

        cleaned_routes = [
            route
            for route in routes
            if route in valid_agents
        ]

        if not cleaned_routes:

            cleaned_routes = [
                "escalation_agent"
            ]

        state.pending_agents = (
            cleaned_routes
        )

        state.current_agent = (
            cleaned_routes[0]
        )

        logger.info(
            "triage_completed",
            workflow=(
                cleaned_routes
            ),
        )

        return state