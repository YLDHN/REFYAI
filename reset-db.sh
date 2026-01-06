#!/bin/bash

echo "🔄 Réinitialisation de la base de données..."

cd /Users/yld/Documents/REFYAI/backend

# Activer l'environnement virtuel
source venv/bin/activate

# Sauvegarder l'ancienne base
if [ -f "refyai.db" ]; then
    echo "📦 Sauvegarde de l'ancienne base..."
    mv refyai.db refyai.db.backup.$(date +%Y%m%d_%H%M%S)
fi

# Créer la nouvelle base avec tous les champs
echo "🔨 Création de la nouvelle base de données..."
python -c "
import asyncio
from app.core.database import engine, Base
from app.models import user, project, document

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print('✅ Base de données créée avec tous les champs')

asyncio.run(init_db())
"

# Créer l'utilisateur demo
echo "👤 Création de l'utilisateur demo..."
python -c "
import asyncio
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash

async def create_demo_user():
    async with AsyncSessionLocal() as db:
        demo_user = User(
            email='demo@refyai.com',
            hashed_password=get_password_hash('demo123'),
            full_name='Demo User',
            is_active=True
        )
        db.add(demo_user)
        await db.commit()
        print('✅ Utilisateur demo créé (demo@refyai.com / demo123)')

asyncio.run(create_demo_user())
"

echo ""
echo "✨ Base de données réinitialisée avec succès !"
echo ""
echo "👤 Compte demo:"
echo "   Email:     demo@refyai.com"
echo "   Password:  demo123"
echo ""
