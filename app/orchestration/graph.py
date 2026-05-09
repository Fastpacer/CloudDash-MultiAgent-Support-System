from langgraph.graph import (
    StateGraph,
    END,
)

from app.orchestration.state import (
    ConversationState,
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


# ---------------------------------------------------
# Agent Instances
# ---------------------------------------------------

triage_agent = TriageAgent()

technical_agent = TechnicalAgent()

billing_agent = BillingAgent()

escalation_agent = EscalationAgent()


# ---------------------------------------------------
# Nodes
# ---------------------------------------------------

def triage_node(
    state: ConversationState,
):

    return triage_agent.process(
        state
    )


def technical_node(
    state: ConversationState,
):

    return technical_agent.process(
        state
    )


def billing_node(
    state: ConversationState,
):

    return billing_agent.process(
        state
    )


def escalation_node(
    state: ConversationState,
):

    return escalation_agent.process(
        state
    )


# ---------------------------------------------------
# Conditional Routing
# ---------------------------------------------------

def route_after_triage(
    state: ConversationState,
):

    if state.current_agent == "technical_agent":

        return "technical"

    elif state.current_agent == "billing_agent":

        return "billing"

    else:

        return "escalation"


# ---------------------------------------------------
# Build Graph
# ---------------------------------------------------

workflow = StateGraph(
    ConversationState
)

workflow.add_node(
    "triage",
    triage_node,
)

workflow.add_node(
    "technical",
    technical_node,
)

workflow.add_node(
    "billing",
    billing_node,
)

workflow.add_node(
    "escalation",
    escalation_node,
)

workflow.set_entry_point(
    "triage"
)

workflow.add_conditional_edges(
    "triage",
    route_after_triage,
    {
        "technical": "technical",
        "billing": "billing",
        "escalation": "escalation",
    },
)

workflow.add_edge(
    "technical",
    END,
)

workflow.add_edge(
    "billing",
    END,
)

workflow.add_edge(
    "escalation",
    END,
)

graph = workflow.compile()