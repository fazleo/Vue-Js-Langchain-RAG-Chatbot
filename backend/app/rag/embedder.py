from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from  app.core.config import settings

def get_embedder():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=settings.GEMINI_API_KEY
    )
