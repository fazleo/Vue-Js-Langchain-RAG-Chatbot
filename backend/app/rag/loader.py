from app.core.logger import get_logger

logger = get_logger(__name__)

def load_documents_from_path(file_path: str, collection_name: str ='default'):
    from pathlib import Path
    from langchain_community.document_loaders import PDFMinerLoader
    ext = Path(file_path).suffix.lower()
    logger.info(f"Collection Name: {collection_name}")

    if ext == ".pdf":
        loader = PDFMinerLoader(file_path)
        docs = loader.load()
        

        for doc in docs:
            doc.metadata["collection_name"] = collection_name
            logger.info(doc.metadata)
        
        
        return docs
    
    print("Only PDF files are supported for now.")
    return []
    

    



