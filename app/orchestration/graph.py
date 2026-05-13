from datetime import (
    datetime,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
)

from langgraph.graph import (
    StateGraph,
    END,
)

from app.orchestration.state import (
    ConversationState,
    HandoverEvent,
    ConversationMessage,
)

from app.agents.triage_agent import (
    TriageAgent,
)

from app.agents.technical_agent import (
    TechnicalAgent,
)

from app.agents.billing_agent import (
    BillingAgent,
)

from app.agents.escalation_agent import (
    EscalationAgent,
)

from app.utils.llm_factory import (
    get_llm,
)

from app.observability.logger import (
    logger,
)


# ---------------------------------------------------
# Agent Registry
# ---------------------------------------------------

triage_agent = TriageAgent()

technical_agent = (
    TechnicalAgent()
)

billing_agent = (
    BillingAgent()
)

escalation_agent = (
    EscalationAgent()
)

AGENT_REGISTRY = {

    "technical_agent": (
        technical_agent
    ),

    "billing_agent": (
        billing_agent
    ),

    "escalation_agent": (
        escalation_agent
    ),
}


# ---------------------------------------------------
# Synthesis LLM
# ---------------------------------------------------

synthesis_llm = get_llm()

synthesis_prompt = (
    ChatPromptTemplate.from_template(
        """
You are the CloudDash Workflow Synthesis Engine.

Your job is to combine multiple specialized
agent outputs into ONE unified enterprise
support response.

IMPORTANT:
- Remove redundancy
- Merge overlapping information
- Preserve technical accuracy
- Keep the response concise
- Produce ONE coherent answer
- Do NOT mention internal orchestration
- Do NOT label sections by agent names

The final answer should feel like:
ONE intelligent enterprise assistant.

Agent Outputs:
{agent_outputs}
"""
    )
)


# ---------------------------------------------------
# Triage Node
# ---------------------------------------------------

def triage_node(
    state: ConversationState,
):

    return triage_agent.process(
        state
    )


# ---------------------------------------------------
# Workflow Executor Node
# ---------------------------------------------------

def workflow_node(
    state: ConversationState,
):

    logger.info(
        "workflow_execution_started",
        workflow=(
            state.pending_agents
        ),
        trace_id=(
            state.trace_id
        ),
    )

    previous_agent = (
        "triage_agent"
    )

    aggregated_citations = (
        set()
    )

    escalation_required = (
        False
    )

    # -----------------------------------------------
    # Sequential Workflow Execution
    # -----------------------------------------------

    for agent_name in (
        state.pending_agents
    ):

        agent = (
            AGENT_REGISTRY.get(
                agent_name
            )
        )

        # -------------------------------------------
        # Missing Agent Fallback
        # -------------------------------------------

        if not agent:

            logger.warning(
                "unknown_agent_detected",
                target_agent=(
                    agent_name
                ),
            )

            continue

        # -------------------------------------------
        # Handover Tracking
        # -------------------------------------------

        handover_event = (
            HandoverEvent(
                source_agent=(
                    previous_agent
                ),

                target_agent=(
                    agent_name
                ),

                reason=(
                    "workflow_transition"
                ),

                context_snapshot=(
                    state.messages[-1]
                    .content[:500]
                ),
            )
        )

        state.handover_history.append(
            handover_event
        )

        logger.info(
            "handover_completed",
            source_agent=(
                previous_agent
            ),
            target_agent=(
                agent_name
            ),
            trace_id=(
                state.trace_id
            ),
        )

        # -------------------------------------------
        # Execute Agent
        # -------------------------------------------

        state.current_agent = (
            agent_name
        )

        state = agent.process(
            state
        )

        # -------------------------------------------
        # Track Workflow Completion
        # -------------------------------------------

        if (
            agent_name
            not in state.completed_agents
        ):

            state.completed_agents.append(
                agent_name
            )

        previous_agent = (
            agent_name
        )

    # -----------------------------------------------
    # Aggregate Citations
    # -----------------------------------------------

    for output in (
        state.agent_outputs
    ):

        for citation in (
            output.citations
        ):

            aggregated_citations.add(
                citation
            )

    # -----------------------------------------------
    # Escalation Detection
    # -----------------------------------------------

    if (
        "escalation_agent"
        in state.completed_agents
    ):

        escalation_required = (
            True
        )

    # -----------------------------------------------
    # Collect Agent Outputs
    # -----------------------------------------------

    raw_outputs = []

    for output in (
        state.agent_outputs
    ):

        formatted_output = (
            f"{output.agent_name}:\n"
            f"{output.response}"
        )

        raw_outputs.append(
            formatted_output
        )

    combined_outputs = (
        "\n\n".join(
            raw_outputs
        )
    )

    # -----------------------------------------------
    # LLM Synthesis Step
    # -----------------------------------------------

    synthesis_chain = (
        synthesis_prompt
        | synthesis_llm
    )

    synthesized_response = (
        synthesis_chain.invoke(
            {
                "agent_outputs": (
                    combined_outputs
                )
            }
        ).content.strip()
    )

    # -----------------------------------------------
    # Agents Invoked Section
    # -----------------------------------------------

    agents_section = (
        "\n\nAgents Invoked:\n"
    )

    for agent_name in (
        state.completed_agents
    ):

        cleaned_agent = (
            agent_name
            .replace(
                "_agent",
                ""
            )
            .replace(
                "_",
                " "
            )
            .title()
        )

        agents_section += (
            f"- {cleaned_agent}\n"
        )

    # -----------------------------------------------
    # Sources Section
    # -----------------------------------------------

    citations_section = (
        "\n\nSources:\n"
    )

    for citation in (
        aggregated_citations
    ):

        citations_section += (
            f"- {citation}\n"
        )

    # -----------------------------------------------
    # Final Combined Response
    # -----------------------------------------------

    final_response = (
        synthesized_response
        + agents_section
        + citations_section
    )

    # -----------------------------------------------
    # Final Assistant Message
    # -----------------------------------------------

    state.messages.append(
        ConversationMessage(
            role="assistant",
            content=final_response,
        )
    )

    # -----------------------------------------------
    # Workflow Metadata
    # -----------------------------------------------

    state.escalation_required = (
        escalation_required
    )

    state.workflow_completed_at = (
        datetime.utcnow()
    )

    state.total_handovers = len(
        state.handover_history
    )

    state.total_agents_invoked = len(
        state.completed_agents
    )

    logger.info(
        "workflow_synthesis_completed",
        agents_invoked=(
            state.completed_agents
        ),
        total_handovers=(
            state.total_handovers
        ),
        trace_id=(
            state.trace_id
        ),
    )

    return state


# ---------------------------------------------------
# Build Workflow Graph
# ---------------------------------------------------

workflow = StateGraph(
    ConversationState
)

workflow.add_node(
    "triage",
    triage_node,
)

workflow.add_node(
    "workflow_executor",
    workflow_node,
)

workflow.set_entry_point(
    "triage"
)

workflow.add_edge(
    "triage",
    "workflow_executor",
)

workflow.add_edge(
    "workflow_executor",
    END,
)

graph = workflow.compile()