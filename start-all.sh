#!/bin/bash
# Script pour tout lancer (Backend + Adminer + Frontend)

set -e

echo "🚀 Démarrage REFYAI - Tout en Un"
echo "================================="

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Vérifier qu'on est dans le bon dossier
cd "$(dirname "$0")"

# Fonction de nettoyage
cleanup() {
    echo ""
    echo -e "${BLUE}🛑 Arrêt de tous les services...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Vérifier PostgreSQL
if ! psql -lqt | cut -d \| -f 1 | grep -qw refyai 2>/dev/null; then
    echo -e "${RED}❌ Base de données 'refyai' non trouvée${NC}"
    echo "Création de la base..."
    createdb refyai || true
fi

# ==================== BACKEND ====================
echo -e "${BLUE}🐍 Démarrage du Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
else
    source venv/bin/activate
fi

# Migrations
alembic upgrade head 2>/dev/null || true

# Créer dossiers nécessaires
mkdir -p logs uploads

# Lancer le backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &> logs/backend.log &
BACKEND_PID=$!

cd ..

# Attendre que le backend soit prêt
sleep 3

# ==================== FRONTEND ====================
echo -e "${BLUE}⚛️  Démarrage du Frontend...${NC}"
cd frontend

if [ ! -f ".env" ]; then
    cp .env.example .env
fi

if [ ! -d "node_modules" ]; then
    echo "Installation des dépendances..."
    npm install
fi

npm run dev &> /tmp/refyai-frontend.log &
FRONTEND_PID=$!

cd ..

# Attendre que tout soit prêt
sleep 5

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║  🎉 REFYAI est en ligne !                   ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║  🌐 Frontend:  http://localhost:3000        ║${NC}"
echo -e "${GREEN}║  🔧 Backend:   http://localhost:8000        ║${NC}"
echo -e "${GREEN}║  📚 API Docs:  http://localhost:8000/docs   ║${NC}"
echo -e "${GREEN}║  🗄️  Prisma:    npm run prisma:studio      ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║  📋 Logs:                                    ║${NC}"
echo -e "${GREEN}║     Backend:  backend/logs/backend.log      ║${NC}"
echo -e "${GREEN}║     Frontend: /tmp/refyai-frontend.log      ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║  ⏹️  Pour arrêter: Ctrl+C                    ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
echo ""

# Garder le script actif
wait
