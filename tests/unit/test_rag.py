from app.retrieval.retriever import (
    retrieve_documents,
)


def test_retrieval_returns_documents():

    results = retrieve_documents(
        query=(
            "CloudWatch metrics "
            "not syncing"
        ),
        top_k=3,
    )

    assert (
        len(results) > 0
    )


def test_retrieved_documents_have_metadata():

    results = retrieve_documents(
        query=(
            "refund policy"
        ),
        top_k=2,
    )

    first_doc = results[0]

    assert (
        "metadata"
        in first_doc
    )

    assert (
        "filename"
        in first_doc["metadata"]
    )