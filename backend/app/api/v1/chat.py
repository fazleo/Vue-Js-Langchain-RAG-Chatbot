from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.rag.chain import build_rag_chain

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    chain = build_rag_chain()
    answer = chain.invoke(req.question)
    return ChatResponse(answer = answer)