#!/bin/bash
# Script de test rapide de l'API REFYAI

echo "🧪 Test de l'API REFYAI"
echo "======================"
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Fonction de test
test_endpoint() {
    local name=$1
    local url=$2
    local method=${3:-GET}
    
    echo -n "Testing $name... "
    
    response=$(curl -s -w "%{http_code}" -o /tmp/test_response.json "$url" -X $method)
    http_code=${response: -3}
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
        echo -e "${GREEN}✓ OK ($http_code)${NC}"
        return 0
    else
        echo -e "${RED}✗ FAIL ($http_code)${NC}"
        cat /tmp/test_response.json 2>/dev/null
        return 1
    fi
}

# Tests
echo "1. Backend Health Check"
test_endpoint "Health" "http://localhost:8000/health"

echo ""
echo "2. API Root"
test_endpoint "Root" "http://localhost:8000/"

echo ""
echo "3. API Documentation"
test_endpoint "Docs" "http://localhost:8000/docs"

echo ""
echo "4. Frontend"
test_endpoint "Frontend" "http://localhost:3000"

echo ""
echo "5. Adminer"
test_endpoint "Adminer" "http://localhost:8080"

echo ""
echo "═══════════════════════════════════"
echo "📊 Métriques du serveur:"
echo "═══════════════════════════════════"
curl -s http://localhost:8000/health | python3 -m json.tool

echo ""
echo "✅ Tests terminés !"
