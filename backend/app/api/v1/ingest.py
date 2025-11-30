from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
import shutil
import os

from app.core.config import settings
from app.rag.loader import load_documents_from_path
from app.rag.splitter import split_documents
from app.rag.vectordb import get_vector_db

router = APIRouter()

@router.post("/upload")
async def upload_and_ingest(
    files: list[UploadFile] = File(...),
    collection_name: str = Form("default")
    ):
   
   
   """
    Upload multiple PDF files.
    For each file:
      - Save it to disk
      - Load PDF pages
      - Chunk
      - Insert into vector DB
    Returns total chunks added.
    """
   upload_dir = Path(settings.UPLOAD_DIR)
   upload_dir.mkdir(parents=True, exist_ok=True)

   all_chunks = []
   file_stats = []

   for file in files:
        file_path = f"{upload_dir}/{file.filename}"

        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"failed to save file, {file.filename}: {str(e)}"
            )

   docs =  load_documents_from_path(str(file_path))

   if not docs:
       raise HTTPException(
           status_code=400,
           detail="Could not read PDF File."
       )
   
   chunks = split_documents(docs)

   try:
       vectordb = get_vector_db(collection_name)
       vectordb.add_documents(chunks)
       vectordb.persist()
   except Exception as e:
       raise HTTPException(status_code=500, detail=f"Failed to index chunks: {str(e)}")

   return {
        "status": "success",
        "filepath": file_path,
        "chunks_added": len(chunks),
        "collection": collection_name
    }
    
         
   




    
