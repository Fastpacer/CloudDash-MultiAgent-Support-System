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

        # ---------------------------------------------------
        # Advanced Triage Prompt
        # ---------------------------------------------------

        self.prompt = (
            ChatPromptTemplate
            .from_template(
                f"""
You are the CloudDash Workflow Triage Agent.

Your responsibilities:
1. Detect ALL relevant support domains
2. Decide which agents should participate
3. Create a focused task for EACH agent

AVAILABLE AGENTS:

technical_agent
- infrastructure
- APIs
- SSO
- dashboards
- monitoring
- sync failures

billing_agent
- subscriptions
- pricing
- invoices
- enterprise upgrades
- licensing

escalation_agent
- unclear requests
- unsupported workflows
- missing KB coverage

ROUTING KEYWORDS:

Technical:
{routing_rules["technical_keywords"]}

Billing:
{routing_rules["billing_keywords"]}

Escalation:
{routing_rules["escalation_keywords"]}

IMPORTANT:
- Multiple agents allowed
- Assign ONLY domain-specific tasks
- Avoid overlap between agents
- Keep tasks concise
- Do NOT let billing agents diagnose infrastructure
- Do NOT let technical agents discuss pricing

OUTPUT FORMAT EXACTLY:

AGENTS:
technical_agent,billing_agent

TASKS:
technical_agent: Diagnose dashboard latency issue
billing_agent: Evaluate enterprise upgrade implications

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

        raw_response = (
            response.content.strip()
        )

        logger.info(
            "triage_raw_response",
            response=raw_response,
        )

        # ---------------------------------------------------
        # Parse AGENTS Section
        # ---------------------------------------------------

        cleaned_routes = []

        agent_tasks = {}

        try:

            sections = (
                raw_response.split(
                    "TASKS:"
                )
            )

            agents_section = (
                sections[0]
            )

            tasks_section = (
                sections[1]
                if len(sections) > 1
                else ""
            )

            # -----------------------------------------------
            # Extract Agents
            # -----------------------------------------------

            if (
                "AGENTS:"
                in agents_section
            ):

                agent_text = (
                    agents_section
                    .replace(
                        "AGENTS:",
                        ""
                    )
                    .strip()
                )

                routes = [
                    route.strip()
                    for route in (
                        agent_text.split(",")
                    )
                    if route.strip()
                ]

            else:

                routes = []

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

            # -----------------------------------------------
            # Extract Agent Tasks
            # -----------------------------------------------

            task_lines = (
                tasks_section
                .strip()
                .splitlines()
            )

            for line in task_lines:

                if ":" not in line:

                    continue

                agent_name, task = (
                    line.split(
                        ":",
                        1,
                    )
                )

                agent_name = (
                    agent_name.strip()
                )

                task = (
                    task.strip()
                )

                if (
                    agent_name
                    in valid_agents
                ):

                    agent_tasks[
                        agent_name
                    ] = task

        except Exception as e:

            logger.warning(
                "triage_parsing_failed",
                error=str(e),
            )

        # ---------------------------------------------------
        # Fallback Routing
        # ---------------------------------------------------

        if not cleaned_routes:

            cleaned_routes = [
                "escalation_agent"
            ]

            agent_tasks[
                "escalation_agent"
            ] = (
                "Handle unsupported "
                "or ambiguous request."
            )

        # ---------------------------------------------------
        # Update State
        # ---------------------------------------------------

        state.pending_agents = (
            cleaned_routes
        )

        state.agent_tasks = (
            agent_tasks
        )

        state.current_agent = (
            cleaned_routes[0]
        )

        logger.info(
            "triage_completed",
            workflow=(
                cleaned_routes
            ),
            tasks=(
                agent_tasks
            ),
        )

        return state