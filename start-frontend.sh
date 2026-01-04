#!/bin/bash
# Script pour lancer le Frontend

set -e

echo "🚀 Démarrage Frontend"
echo "===================="

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
    echo -e "${BLUE}🛑 Arrêt du frontend...${NC}"
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Frontend
echo -e "${BLUE}⚛️  Démarrage du Frontend...${NC}"
cd frontend

if [ ! -f ".env" ]; then
    cp .env.example .env
fi

if [ ! -d "node_modules" ]; then
    echo "Installation des dépendances..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!

cd ..

# Attendre que le frontend démarre
sleep 5

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║  ✅ Frontend démarré !                       ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║  🌐 Frontend: http://localhost:3000         ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║  ⏹️  Pour arrêter: Ctrl+C                    ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
echo ""

# Garder le script actif
wait
