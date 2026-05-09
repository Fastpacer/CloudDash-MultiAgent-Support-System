from app.retrieval.vector_store import vector_store
from app.retrieval.hybrid_search import bm25_retriever
from app.retrieval.reranker import rerank_documents
from app.retrieval.query_rewriter import rewrite_query

from app.observability.logger import logger


def dense_retrieve(
    query: str,
    top_k: int = 4,
):

    results = vector_store.similarity_search_with_score(
        query,
        k=top_k,
    )

    formatted_results = []

    for document, score in results:

        formatted_results.append(
            {
                "content": document.page_content,
                "metadata": document.metadata,
                "score": float(score),
                "retrieval_type": "dense",
            }
        )

    return formatted_results


def reciprocal_rank_fusion(
    dense_results,
    sparse_results,
    k: int = 60,
):

    fused_scores = {}

    all_results = dense_results + sparse_results

    for rank, result in enumerate(all_results):

        key = result["content"]

        if key not in fused_scores:

            fused_scores[key] = {
                "result": result,
                "score": 0,
            }

        fused_scores[key]["score"] += 1 / (
            rank + k
        )

    reranked = sorted(
        fused_scores.values(),
        key=lambda item: item["score"],
        reverse=True,
    )

    return [
        item["result"]
        for item in reranked
    ]


def retrieve_documents(
    query: str,
    top_k: int = 4,
):

    logger.info(
        "hybrid_retrieval_started",
        query=query,
    )

    # -----------------------------------
    # Query Rewriting
    # -----------------------------------

    rewritten_query = rewrite_query(
        query
    )

    logger.info(
        "query_rewritten",
        original_query=query,
        rewritten_query=rewritten_query,
    )

    # -----------------------------------
    # Dense Semantic Retrieval
    # -----------------------------------

    dense_results = dense_retrieve(
        query=rewritten_query,
        top_k=top_k,
    )

    # -----------------------------------
    # Sparse BM25 Retrieval
    # -----------------------------------

    sparse_results = bm25_retriever.retrieve(
        query=rewritten_query,
        top_k=top_k,
    )

    # -----------------------------------
    # Reciprocal Rank Fusion
    # -----------------------------------

    fused_results = reciprocal_rank_fusion(
        dense_results,
        sparse_results,
    )

    logger.info(
        "hybrid_retrieval_completed",
        dense_results=len(dense_results),
        sparse_results=len(sparse_results),
        fused_results=len(fused_results),
    )

    # -----------------------------------
    # Cross-Encoder Re-ranking
    # -----------------------------------

    reranked_results = rerank_documents(
        query=rewritten_query,
        documents=fused_results,
        top_k=top_k,
    )

    logger.info(
        "reranked_results_ready",
        final_results=len(reranked_results),
    )

    return reranked_results