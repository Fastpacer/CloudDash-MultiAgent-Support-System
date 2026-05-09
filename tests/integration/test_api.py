from fastapi.testclient import (
    TestClient,
)

from app.main import app


client = TestClient(
    app
)


def test_chat_endpoint():

    payload = {
        "message": (
            "My invoice amount "
            "looks incorrect."
        ),
        "conversation_id": (
            "integration-test"
        ),
    }

    response = client.post(
        "/chat",
        json=payload,
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert (
        "response"
        in data
    )

    assert (
        "active_agent"
        in data
    )

    assert (
        "trace_id"
        in data
    )