"""
Script pour ajouter les colonnes manquantes à la table projects
"""
import asyncio
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

async def add_missing_columns():
    async with AsyncSessionLocal() as session:
        # Lire le fichier SQL
        with open('add_missing_columns.sql', 'r') as f:
            sql = f.read()
        
        # Exécuter
        await session.execute(text(sql))
        await session.commit()
        print("✅ Colonnes ajoutées avec succès!")

if __name__ == "__main__":
    asyncio.run(add_missing_columns())
