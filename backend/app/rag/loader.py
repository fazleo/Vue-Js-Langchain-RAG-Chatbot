
def load_documents_from_path(file_path: str):
    from pathlib import Path
    from langchain_community.document_loaders import PDFMinerLoader
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        loader = PDFMinerLoader(file_path)
        docs = loader.load()
        return docs
    
    print("Only PDF files are supported for now.")
    return []
    

    



