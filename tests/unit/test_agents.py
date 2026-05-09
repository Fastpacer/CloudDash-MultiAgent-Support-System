from app.agents.triage_agent import (
    TriageAgent,
)

from app.orchestration.state import (
    ConversationState,
    ConversationMessage,
)


def test_billing_routing():

    agent = TriageAgent()

    state = ConversationState(
        trace_id="test-trace",
        conversation_id="test-convo",
        messages=[
            ConversationMessage(
                role="user",
                content=(
                    "I was charged twice "
                    "for my subscription."
                ),
            )
        ],
    )

    result = agent.process(
        state
    )

    assert (
        "billing_agent"
        in result.pending_agents
    )


def test_technical_routing():

    agent = TriageAgent()

    state = ConversationState(
        trace_id="test-trace",
        conversation_id="test-convo",
        messages=[
            ConversationMessage(
                role="user",
                content=(
                    "CloudWatch metrics "
                    "are not syncing."
                ),
            )
        ],
    )

    result = agent.process(
        state
    )

    assert (
        "technical_agent"
        in result.pending_agents
    )


def test_escalation_routing():

    agent = TriageAgent()

    state = ConversationState(
        trace_id="test-trace",
        conversation_id="test-convo",
        messages=[
            ConversationMessage(
                role="user",
                content=(
                    "I want legal action "
                    "against your company."
                ),
            )
        ],
    )

    result = agent.process(
        state
    )

    assert (
        "escalation_agent"
        in result.pending_agents
    )