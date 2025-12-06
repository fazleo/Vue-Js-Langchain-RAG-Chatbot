from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GOOGLE_API_KEY:str
    GROQ_API_KEY: str
    CHROMA_DB_DIR: str = "./chroma_db"
    UPLOAD_DIR: str = "./uploads"
    DEBUG: bool = True


    class Config:
        env_file = ".env"

settings = Settings()

    