#!/bin/bash
# Script pour lancer Prisma Studio

set -e

echo "🗄️  Lancement de Prisma Studio"
echo "=============================="

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Vérifier qu'on est dans le bon dossier
cd "$(dirname "$0")/frontend"

# Vérifier que Prisma est installé
if [ ! -d "node_modules/@prisma" ]; then
    echo "Installation de Prisma..."
    npm install
fi

# Vérifier que le client est généré
if [ ! -d "node_modules/.prisma/client" ]; then
    echo "Génération du client Prisma..."
    npx prisma generate
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║  🗄️  Prisma Studio                          ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║  Interface de gestion de la base de données ║${NC}"
echo -e "${GREEN}║  Remplace Adminer avec une interface moderne║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║  📊 URL: http://localhost:5555               ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║  ⏹️  Pour arrêter: Ctrl+C                    ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
echo ""

# Lancer Prisma Studio
npx prisma studio
