from app.orchestration.graph import (
    graph,
)

from app.orchestration.state import (
    ConversationState,
    ConversationMessage,
)


def test_billing_workflow_execution():

    state = ConversationState(
        trace_id="handover-test",
        conversation_id="handover-convo",
        messages=[
            ConversationMessage(
                role="user",
                content=(
                    "Why was I charged "
                    "twice this month?"
                ),
            )
        ],
    )

    result = graph.invoke(
        state
    )

    assert (
        result["current_agent"]
        == "billing_agent"
    )

    assert (
        len(
            result["messages"]
        ) > 1
    )