from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    # collection_name: str

class ChatResponse(BaseModel):
    answer: str

# class IngestResponse(BaseModel):
#     status: str
#     total_files: int
#     total_chunks: int
#     file
    