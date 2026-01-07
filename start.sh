#!/bin/bash

set -e

echo "🚀 REFYAI - Démarrage complet du projet"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Fonction pour tuer un processus sur un port
kill_port() {
    local port=$1
    local pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "⚠️  Port $port occupé par PID $pid - Arrêt..."
        kill -9 $pid 2>/dev/null
        sleep 1
        echo "✅ Port $port libéré"
    fi
}

# 1. Vérifier et libérer les ports
echo "🔍 Étape 1/5: Vérification des ports..."
kill_port 8000  # Backend
kill_port 3000  # Frontend
echo "✅ Ports disponibles"
echo ""

# 2. Configuration Backend
echo "🐍 Étape 2/5: Configuration du Backend Python..."
cd /Users/yld/Documents/REFYAI/backend

# Créer l'environnement virtuel si nécessaire
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel avec Python 3.12..."
    /opt/homebrew/bin/python3.12 -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances si nécessaire
if [ ! -f "venv/.installed" ]; then
    echo "📥 Installation des dépendances Python..."
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt > /dev/null 2>&1
    touch venv/.installed
    echo "✅ Dépendances installées"
else
    echo "✅ Dépendances déjà installées"
fi
echo ""

# 3. Configuration de la base de données
echo "🗄️  Étape 3/5: Configuration de la base de données..."

# Créer le fichier .env si nécessaire
if [ ! -f ".env" ]; then
    echo "📝 Création du fichier .env..."
    cat > .env << EOF
DATABASE_URL=sqlite+aiosqlite:///./refyai.db
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF
    echo "✅ Fichier .env créé"
fi

# Créer la base de données si elle n'existe pas
if [ ! -f "refyai.db" ]; then
    echo "🔨 Création de la base de données..."
    python -c "
import asyncio
from app.core.database import engine, Base
from app.models import user, project, document

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('✅ Base de données créée')

asyncio.run(init_db())
"
else
    echo "✅ Base de données existe déjà"
fi

# Créer un utilisateur demo si nécessaire
echo "👤 Vérification utilisateur demo..."
python -c "
import asyncio
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy import select, func

async def create_demo_user():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(func.count(User.id)).filter(User.email == 'demo@refyai.com')
        )
        user_count = result.scalar()

        if user_count == 0:
            demo_user = User(
                email='demo@refyai.com',
                hashed_password=get_password_hash('demo123'),
                full_name='Demo User',
                is_active=True
            )
            db.add(demo_user)
            await db.commit()
            print('✅ Utilisateur demo créé (demo@refyai.com / demo123)')
        else:
            print('✅ Utilisateur demo existe déjà')

asyncio.run(create_demo_user())
" 2>/dev/null || echo "⚠️ Impossible de créer l'utilisateur demo (sera créé au premier lancement)"

echo ""

# 4. Démarrage du Backend
echo "🚀 Étape 4/5: Démarrage du Backend..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/refyai-backend.log 2>&1 &
BACKEND_PID=$!
echo "⏳ Attente du backend..."
sleep 3

# Vérifier que le backend répond
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend démarré sur http://localhost:8000 (PID: $BACKEND_PID)"
else
    echo "❌ Erreur: Le backend n'a pas démarré"
    echo "Logs: /tmp/refyai-backend.log"
    tail -n 20 /tmp/refyai-backend.log
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
echo ""

# 5. Démarrage du Frontend
echo "⚛️  Étape 5/5: Démarrage du Frontend..."
cd /Users/yld/Documents/REFYAI/frontend

# Installer les dépendances si nécessaire
if [ ! -d "node_modules" ]; then
    echo "📥 Installation des dépendances npm..."
    npm install > /dev/null 2>&1
    echo "✅ Dépendances installées"
else
    echo "✅ Dépendances déjà installées"
fi

# Démarrer le frontend
npm run dev > /tmp/refyai-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "⏳ Attente du frontend..."
sleep 8

# Vérifier que le frontend répond
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend démarré sur http://localhost:3000 (PID: $FRONTEND_PID)"
else
    echo "❌ Erreur: Le frontend n'a pas démarré"
    echo "Logs: /tmp/refyai-frontend.log"
    tail -n 20 /tmp/refyai-frontend.log
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ REFYAI démarré avec succès !"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Frontend:  http://localhost:3000"
echo "🔧 Backend:   http://localhost:8000"
echo "📚 API Docs:  http://localhost:8000/docs"
echo ""
echo "👤 Compte demo:"
echo "   Email:     demo@refyai.com"
echo "   Password:  demo123"
echo ""
echo "📝 Logs:"
echo "   Backend:   /tmp/refyai-backend.log"
echo "   Frontend:  /tmp/refyai-frontend.log"
echo ""
echo "🛑 Pour arrêter:"
echo "   Ctrl+C ou ./stop.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Fonction pour arrêter proprement
cleanup() {
    echo ""
    echo "🛑 Arrêt des services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    sleep 1
    kill_port 8000
    kill_port 3000
    echo "✅ Services arrêtés"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Garder le script actif
echo "⌛ Services en cours d'exécution... (Ctrl+C pour arrêter)"
wait
