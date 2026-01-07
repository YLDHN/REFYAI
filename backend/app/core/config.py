from pydantic_settings import BaseSettings
from typing import List, Any
import json
from pydantic import field_validator

class Settings(BaseSettings):
    # Projet
    PROJECT_NAME: str = "REFY AI API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
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

    @field_validator('ALLOWED_ORIGINS', mode='before')
    def _parse_allowed_origins(cls, v: Any):
        """Accept JSON array or comma-separated string in env var for ALLOWED_ORIGINS."""
        if isinstance(v, str):
            s = v.strip()
            # Try JSON array first
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass

            # Fallback: comma separated
            return [p.strip() for p in s.split(',') if p.strip()]

        return v
    
    # Performance & Robustesse
    API_TIMEOUT: int = 60  # Timeout en secondes
    MAX_CONNECTIONS: int = 100  # Pool de connexions DB
    CONNECTION_TIMEOUT: int = 30  # Timeout connexion DB
    REQUEST_RATE_LIMIT: int = 100  # Requêtes max par minute par IP
    ENABLE_RETRY: bool = True  # Retry automatique sur erreurs temporaires
    
    # Base de données
    DATABASE_URL: str = "postgresql+asyncpg://refyai:refyai@localhost:5432/refyai"
    
    # Celery & Redis
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    REDIS_URL: str = "redis://localhost:6379/1"
    
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
