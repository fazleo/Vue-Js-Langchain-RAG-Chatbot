from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(
    docs, 
    chunk_size: int = 500, 
    chunk_overlap: int = 80
):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    chunks = splitter.split_documents(docs)
    return chunks
