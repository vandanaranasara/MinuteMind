import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Meeting Minutes"
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    CORS_ORIGINS: List[str] = ["http://localhost:8501", "http://localhost:3000"]

settings = Settings()
