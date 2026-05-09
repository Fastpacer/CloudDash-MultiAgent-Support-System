import os

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.utils.config_loader import settings


# ---------------------------------------------------
# HuggingFace Authentication
# ---------------------------------------------------

if settings.HF_TOKEN:
    os.environ["HF_TOKEN"] = settings.HF_TOKEN


# ---------------------------------------------------
# Embedding Model Configuration
# ---------------------------------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

print("Initializing embedding model...")


embedding_function = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
)


# ---------------------------------------------------
# Persistent Chroma Vector Store
# ---------------------------------------------------

vector_store = Chroma(
    collection_name="clouddash_kb",
    embedding_function=embedding_function,
    persist_directory=settings.VECTOR_DB_DIR,
)

print("Chroma vector store initialized successfully.")