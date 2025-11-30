from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GROQ_API_KEY: str
    CHROMA_DIR: str = "./chroma_db"
    UPLOAD_DIR: str = "./uploads"


    class Config:
        env_file = ".env"

settings = Settings()

    