from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Moteur de base de données asynchrone
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

# Session maker
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base pour les modèles
Base = declarative_base()

# Dépendance pour obtenir la session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
