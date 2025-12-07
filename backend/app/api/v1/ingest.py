from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
import shutil
import os
import uuid

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
        if file.filename == "":
            raise HTTPException(
                status_code=400,
                detail="Empty filename not allowed"
            )
        
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail=f"Only PDF files are allowed. Rejected: {file.filename}"
            )
        
        # 2. Generate secure, unique filename
        original_name = Path(file.filename).name
        safe_filename = f"{uuid.uuid4()}_{original_name}"
        file_path = upload_dir / safe_filename

        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"failed to save file, {original_name}: {str(e)}"
            )

   
        docs =  load_documents_from_path(str(file_path), collection_name=collection_name)
    
        if not docs:
            raise HTTPException(
                status_code=400,
                detail="Could not read PDF File."
            )

        chunks = split_documents(docs)

        all_chunks.extend(chunks)

        file_stats.append({
            "file": original_name,
            "saved_as": safe_filename,
            "pages": len(docs),
            "chunks": len(chunks)
        })
        
    try:
        vectordb = get_vector_db(collection_name)
        vectordb.add_documents(chunks)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index chunks: {str(e)}")

    return {
        "status": "success",
        "filepath": file_path,
        "chunks_added": len(chunks),
        "collection": collection_name
    }
    
         
   




    
