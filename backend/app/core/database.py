from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import asyncio

# Configuration dynamique selon le type de base de données
engine_kwargs = {
    "echo": settings.DEBUG,
    "future": True,
}

# Détection du type de base de données
db_url = str(settings.DATABASE_URL)

if "sqlite" in db_url:
    # Configuration SQLite
    engine_kwargs.update({
        "connect_args": {"check_same_thread": False}
    })
else:
    # Configuration PostgreSQL (Production)
    engine_kwargs.update({
        "pool_size": 20,
        "max_overflow": 30,
        "pool_timeout": settings.CONNECTION_TIMEOUT,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
        "connect_args": {
            "server_settings": {
                "application_name": "refyai_backend"
            },
            "timeout": settings.CONNECTION_TIMEOUT,
            "command_timeout": settings.API_TIMEOUT,
        }
    })

# Moteur de base de données asynchrone
engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)

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
