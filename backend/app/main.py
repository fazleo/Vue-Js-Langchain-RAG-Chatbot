from fastapi import FastAPI
from app.api.v1.router import router as v1_router
from app.core.config import settings


app = FastAPI(
    title="RAG Chatbot Backend",
    debug=settings.DEBUG
)

app.include_router(v1_router, prefix="/api/v1")
@app.get("/")
def home():
    return {
        "status" : "running",
        "version" : "1.0"
    }