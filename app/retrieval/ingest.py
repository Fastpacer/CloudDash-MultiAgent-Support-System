from pathlib import Path
 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.retrieval.vector_store import vector_store
from app.observability.logger import logger


KB_PATH = "knowledge_base"


def load_markdown_documents():

    documents = []

    kb_directory = Path(KB_PATH)

    for file_path in kb_directory.rglob("*.md"):

        try:

            content = file_path.read_text(
                encoding="utf-8"
            )

            category = file_path.parent.name

            document = Document(
                page_content=content,
                metadata={
                    "source": str(file_path),
                    "category": category,
                    "filename": file_path.name,
                },
            )

            documents.append(document)

        except Exception as error:

            logger.error(
                "document_loading_failed",
                file=str(file_path),
                error=str(error),
            )

    logger.info(
        "documents_loaded",
        total_documents=len(documents),
    )

    return documents


def chunk_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    chunks = text_splitter.split_documents(
        documents
    )

    logger.info(
        "documents_chunked",
        total_chunks=len(chunks),
    )

    return chunks


def ingest_documents():

    logger.info(
        "kb_ingestion_started"
    )

    documents = load_markdown_documents()

    chunks = chunk_documents(documents)

    vector_store.add_documents(chunks)

    logger.info(
        "kb_ingestion_completed",
        chunks_added=len(chunks),
    )


if __name__ == "__main__":

    ingest_documents()