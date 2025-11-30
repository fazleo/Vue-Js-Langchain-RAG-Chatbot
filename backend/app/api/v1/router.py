from fastapi import APIRouter
from .chat import router as chat_router
from .ingest import router as ingest_router

router = APIRouter()
router.include_router(
    chat_router,
    prefix="/chat",
    tags=["chat"]
)

router.include_router(
    ingest_router,
    prefix="/ingest",
    tags=["ingest"]
)