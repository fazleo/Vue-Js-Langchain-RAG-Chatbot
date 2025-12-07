from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.logger import get_logger

logger = get_logger(__name__)



def split_documents(
    docs, 
    chunk_size: int = 500, 
    chunk_overlap: int = 80,
):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    chunks = splitter.split_documents(docs)

    for chunk in chunks:
        logger.info(chunk.metadata)

    return chunks
