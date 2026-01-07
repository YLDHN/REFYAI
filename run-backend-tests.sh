#!/bin/bash

# Script pour lancer tous les tests backend REFY AI
# Équivalent du run-visual-tests.sh mais pour le backend

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪  REFY AI - TESTS BACKEND"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Vérifier que nous sommes dans le bon répertoire
if [ ! -d "backend" ]; then
    echo -e "${RED}❌ Répertoire 'backend' introuvable. Êtes-vous à la racine du projet ?${NC}"
    exit 1
fi

# Vérifier que Python est disponible
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé ou introuvable${NC}"
    exit 1
fi

# Se déplacer dans le répertoire backend
cd backend

echo -e "${BLUE}📦 Vérification de l'environnement...${NC}"
echo ""

# Vérifier si les dépendances sont installées
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Aucun environnement virtuel détecté${NC}"
    echo -e "${YELLOW}   Tentative d'exécution avec Python système...${NC}"
    echo ""
fi

# Afficher le menu de sélection
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   SÉLECTION DES TESTS${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "  1) 📋 Logique métier pure"
echo "  2) ⏰ Moteur de phasage temporel"
echo "  3) 💰 Moteur financier (Waterfall/Promote)"
echo "  4) 📄 Conformité documentaire"
echo "  5) 🤖 IA prédictive (Mocks)"
echo "  6) 🌐 API bout en bout"
echo "  7) 📊 Exports (Excel/PDF)"
echo "  8) 🔒 Confidentialité (Privacy Shield)"
echo "  9) 🏥 Services administratifs"
echo " 10) 💼 Services CAPEX"
echo " 11) ⚡ Services critiques"
echo " 12) 💸 Finance avancée"
echo " 13) 🔌 Endpoints API"
echo ""
echo " 99) 🚀 LANCER TOUS LES TESTS"
echo "  0) ❌ Annuler"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════${NC}"
echo ""
read -p "Votre choix (0-13, 99): " choice

# Déterminer quelle commande pytest exécuter
case $choice in
    1)
        echo -e "\n${GREEN}🧪 Lancement: Logique métier pure${NC}\n"
        TEST_FILE="tests/test_01_business_logic.py"
        ;;
    2)
        echo -e "\n${GREEN}🧪 Lancement: Moteur de phasage temporel${NC}\n"
        TEST_FILE="tests/test_02_timeline_engine.py"
        ;;
    3)
        echo -e "\n${GREEN}🧪 Lancement: Moteur financier (Waterfall/Promote)${NC}\n"
        TEST_FILE="tests/test_03_waterfall_promote.py"
        ;;
    4)
        echo -e "\n${GREEN}🧪 Lancement: Conformité documentaire${NC}\n"
        TEST_FILE="tests/test_04_document_compliance.py"
        ;;
    5)
        echo -e "\n${GREEN}🧪 Lancement: IA prédictive (Mocks)${NC}\n"
        TEST_FILE="tests/test_05_ai_predictions_mock.py"
        ;;
    6)
        echo -e "\n${GREEN}🧪 Lancement: API bout en bout${NC}\n"
        TEST_FILE="tests/test_06_api_end_to_end.py"
        ;;
    7)
        echo -e "\n${GREEN}🧪 Lancement: Exports (Excel/PDF)${NC}\n"
        TEST_FILE="tests/test_07_exports_excel_pdf.py"
        ;;
    8)
        echo -e "\n${GREEN}🧪 Lancement: Confidentialité (Privacy Shield)${NC}\n"
        TEST_FILE="tests/test_08_privacy_shield.py"
        ;;
    9)
        echo -e "\n${GREEN}🧪 Lancement: Services administratifs${NC}\n"
        TEST_FILE="tests/test_administrative_delay_service.py"
        ;;
    10)
        echo -e "\n${GREEN}🧪 Lancement: Services CAPEX${NC}\n"
        TEST_FILE="tests/test_capex_service.py"
        ;;
    11)
        echo -e "\n${GREEN}🧪 Lancement: Services critiques${NC}\n"
        TEST_FILE="tests/test_critical_services.py"
        ;;
    12)
        echo -e "\n${GREEN}🧪 Lancement: Finance avancée${NC}\n"
        TEST_FILE="tests/test_financial_advanced.py"
        ;;
    13)
        echo -e "\n${GREEN}🧪 Lancement: Endpoints API${NC}\n"
        TEST_FILE="tests/test_api_endpoints.py"
        ;;
    99)
        echo -e "\n${GREEN}🚀 Lancement de TOUS les tests${NC}\n"
        TEST_FILE="tests/"
        ;;
    0)
        echo -e "\n${YELLOW}❌ Annulation${NC}\n"
        exit 0
        ;;
    *)
        echo -e "\n${RED}❌ Choix invalide${NC}\n"
        exit 1
        ;;
esac

# Lancer les tests avec pytest
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}   EXÉCUTION DES TESTS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Activer l'environnement virtuel si disponible
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Exécuter pytest avec les options de configuration
python3 -m pytest $TEST_FILE -v --tb=short --color=yes

# Capturer le code de sortie
EXIT_CODE=$?

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ TOUS LES TESTS SONT PASSÉS !${NC}"
else
    echo -e "${RED}❌ CERTAINS TESTS ONT ÉCHOUÉ (code: $EXIT_CODE)${NC}"
fi

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

exit $EXIT_CODE
