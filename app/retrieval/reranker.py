from sentence_transformers import CrossEncoder

from app.observability.logger import logger


RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


print("Initializing reranker model...")


reranker_model = CrossEncoder(
    RERANKER_MODEL
)


def rerank_documents(
    query: str,
    documents: list,
    top_k: int = 4,
):

    logger.info(
        "reranking_started",
        candidate_documents=len(documents),
    )

    pairs = [
        (query, doc["content"])
        for doc in documents
    ]

    scores = reranker_model.predict(
        pairs
    )

    reranked_results = []

    for doc, score in zip(documents, scores):

        doc["rerank_score"] = float(score)

        reranked_results.append(doc)

    reranked_results.sort(
        key=lambda item: item["rerank_score"],
        reverse=True,
    )

    logger.info(
        "reranking_completed",
        returned_documents=min(
            top_k,
            len(reranked_results),
        ),
    )

    return reranked_results[:top_k]