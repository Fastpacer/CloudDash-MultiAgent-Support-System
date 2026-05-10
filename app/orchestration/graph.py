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

    # -----------------------------------------------
    # Aggregated Workflow Responses
    # -----------------------------------------------

    workflow_responses = []

    # -----------------------------------------------
    # Sequential Agent Execution
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
        # Handover Logging
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

        pre_message_count = len(
            state.messages
        )

        state = agent.process(
            state
        )

        # -------------------------------------------
        # Extract Newly Generated Messages
        # -------------------------------------------

        new_messages = (
            state.messages[
                pre_message_count:
            ]
        )

        for msg in new_messages:

            if msg.role == "assistant":

                formatted_response = (
                    f"\n\n"
                    f"=== "
                    f"{agent_name.upper()} "
                    f"===\n\n"
                    f"{msg.content}"
                )

                workflow_responses.append(
                    formatted_response
                )

        # -------------------------------------------
        # Completed Agent Tracking
        # -------------------------------------------

        state.completed_agents.append(
            agent_name
        )

        previous_agent = (
            agent_name
        )

    # -----------------------------------------------
    # Final Workflow Synthesis
    # -----------------------------------------------

    if workflow_responses:

        combined_response = (
            "\n".join(
                workflow_responses
            )
        )

        state.messages.append(
            ConversationMessage(
                role="assistant",
                content=combined_response,
            )
        )

    logger.info(
        "workflow_execution_completed",
        completed_agents=(
            state.completed_agents
        ),
        total_handovers=len(
            state.handover_history
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