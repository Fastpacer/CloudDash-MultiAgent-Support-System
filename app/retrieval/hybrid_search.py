from pathlib import Path

from rank_bm25 import BM25Okapi

from app.observability.logger import logger


KB_PATH = "knowledge_base"


class BM25Retriever:

    def __init__(self):

        self.documents = []
        self.metadata = []

        self._load_documents()

        tokenized_corpus = [
            doc.split()
            for doc in self.documents
        ]

        self.bm25 = BM25Okapi(
            tokenized_corpus
        )

        logger.info(
            "bm25_initialized",
            total_documents=len(self.documents),
        )

    def _load_documents(self):

        kb_directory = Path(KB_PATH)

        for file_path in kb_directory.rglob("*.md"):

            try:

                content = file_path.read_text(
                    encoding="utf-8"
                )

                self.documents.append(content)

                self.metadata.append(
                    {
                        "source": str(file_path),
                        "filename": file_path.name,
                        "category": file_path.parent.name,
                    }
                )

            except Exception as error:

                logger.error(
                    "bm25_document_load_failed",
                    file=str(file_path),
                    error=str(error),
                )

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
    ):

        tokenized_query = query.split()

        scores = self.bm25.get_scores(
            tokenized_query
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )[:top_k]

        results = []

        for index in ranked_indices:

            results.append(
                {
                    "content": self.documents[index],
                    "metadata": self.metadata[index],
                    "score": float(scores[index]),
                    "retrieval_type": "bm25",
                }
            )

        logger.info(
            "bm25_retrieval_completed",
            retrieved_documents=len(results),
        )

        return results


bm25_retriever = BM25Retriever()