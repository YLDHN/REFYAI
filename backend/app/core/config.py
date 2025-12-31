from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Projet
    PROJECT_NAME: str = "REFY AI API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Sécurité
    SECRET_KEY: str = "votre-cle-secrete-a-changer-en-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 jours
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "tauri://localhost",
        "https://refyai.vercel.app",
        "https://*.vercel.app",
    ]
    
    # Base de données
    DATABASE_URL: str = "postgresql+asyncpg://refyai:refyai@localhost:5432/refyai"
    
    # IA
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    
    # Stockage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50 MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
