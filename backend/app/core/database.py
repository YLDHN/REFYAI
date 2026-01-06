from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import asyncio

# Moteur de base de données asynchrone avec pool optimisé
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    # Configuration du pool de connexions
    pool_size=20,                    # Connexions maintenues
    max_overflow=30,                 # Connexions supplémentaires possibles
    pool_timeout=settings.CONNECTION_TIMEOUT,
    pool_recycle=3600,              # Recycler connexions après 1h
    pool_pre_ping=True,             # Vérifier connexions avant utilisation
    # Gestion des erreurs
    connect_args={
        "server_settings": {
            "application_name": "refyai_backend"
        },
        "timeout": settings.CONNECTION_TIMEOUT,
        "command_timeout": settings.API_TIMEOUT,
    },
)

# Session maker avec auto-retry
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# Base pour les modèles
Base = declarative_base()

# Dépendance pour obtenir la session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
