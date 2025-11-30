from langchain_chroma import Chroma
from app.rag.embedder import get_embedder
from app.core.config import settings

def get_vector_db(collection_name="default"):
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embedder(),
        persist_directory=settings.CHROMADB_DIR,  # Where to save data locally, remove if not necessary
    )