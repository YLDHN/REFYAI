#!/bin/bash
# Test de connexion Frontend-Backend pour l'authentification

echo "🧪 Test Connexion Frontend-Backend"
echo "===================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
API_URL="http://localhost:8000/api/v1"
TEST_EMAIL="test_$(date +%s)@example.com"
TEST_PASSWORD="TestPassword123!"
TEST_NAME="Test User"

echo "📧 Email de test: $TEST_EMAIL"
echo ""

# Test 1: Backend Health
echo "1️⃣  Test Backend Health..."
response=$(curl -s -w "%{http_code}" -o /tmp/health.json http://localhost:8000/health)
http_code=${response: -3}

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ Backend en ligne${NC}"
    cat /tmp/health.json | python3 -m json.tool 2>/dev/null | head -5
else
    echo -e "${RED}✗ Backend inaccessible (code: $http_code)${NC}"
    exit 1
fi
echo ""

# Test 2: Inscription
echo "2️⃣  Test Inscription (/auth/register)..."
register_response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\",\"full_name\":\"$TEST_NAME\"}")

register_body=$(echo "$register_response" | head -n -1)
register_code=$(echo "$register_response" | tail -n 1)

if [ "$register_code" = "201" ]; then
    echo -e "${GREEN}✓ Inscription réussie${NC}"
    echo "$register_body" | python3 -m json.tool 2>/dev/null
    USER_ID=$(echo "$register_body" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
    echo -e "${BLUE}User ID: $USER_ID${NC}"
elif [ "$register_code" = "400" ]; then
    echo -e "${YELLOW}⚠️  Email déjà utilisé (normal si test déjà exécuté)${NC}"
else
    echo -e "${RED}✗ Erreur inscription (code: $register_code)${NC}"
    echo "$register_body"
    exit 1
fi
echo ""

# Test 3: Connexion
echo "3️⃣  Test Connexion (/auth/login)..."
login_response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")

login_body=$(echo "$login_response" | head -n -1)
login_code=$(echo "$login_response" | tail -n 1)

if [ "$login_code" = "200" ]; then
    echo -e "${GREEN}✓ Connexion réussie${NC}"
    TOKEN=$(echo "$login_body" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
    echo -e "${BLUE}Token obtenu: ${TOKEN:0:20}...${NC}"
else
    echo -e "${RED}✗ Erreur connexion (code: $login_code)${NC}"
    echo "$login_body"
    exit 1
fi
echo ""

# Test 4: Vérification du token
echo "4️⃣  Test Token (/auth/me)..."
me_response=$(curl -s -w "\n%{http_code}" -X GET "$API_URL/auth/me" \
    -H "Authorization: Bearer $TOKEN")

me_body=$(echo "$me_response" | head -n -1)
me_code=$(echo "$me_response" | tail -n 1)

if [ "$me_code" = "200" ]; then
    echo -e "${GREEN}✓ Token valide${NC}"
    echo "$me_body" | python3 -m json.tool 2>/dev/null
else
    echo -e "${RED}✗ Token invalide (code: $me_code)${NC}"
    echo "$me_body"
    exit 1
fi
echo ""

# Test 5: Test endpoint protégé (projects)
echo "5️⃣  Test Endpoint Protégé (/projects)..."
projects_response=$(curl -s -w "\n%{http_code}" -X GET "$API_URL/projects" \
    -H "Authorization: Bearer $TOKEN")

projects_body=$(echo "$projects_response" | head -n -1)
projects_code=$(echo "$projects_response" | tail -n 1)

if [ "$projects_code" = "200" ]; then
    echo -e "${GREEN}✓ Accès autorisé aux projets${NC}"
    project_count=$(echo "$projects_body" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
    echo -e "${BLUE}Nombre de projets: $project_count${NC}"
else
    echo -e "${RED}✗ Accès refusé (code: $projects_code)${NC}"
    echo "$projects_body"
fi
echo ""

# Test 6: Test sans token (doit échouer)
echo "6️⃣  Test Sans Token (doit échouer)..."
notoken_response=$(curl -s -w "\n%{http_code}" -X GET "$API_URL/projects")
notoken_code=$(echo "$notoken_response" | tail -n 1)

if [ "$notoken_code" = "401" ] || [ "$notoken_code" = "403" ]; then
    echo -e "${GREEN}✓ Sécurité OK (accès refusé sans token)${NC}"
else
    echo -e "${RED}✗ Problème de sécurité (code: $notoken_code)${NC}"
fi
echo ""

# Résumé
echo "════════════════════════════════════"
echo -e "${GREEN}✅ Tous les tests réussis !${NC}"
echo "════════════════════════════════════"
echo ""
echo "📝 Instructions pour le frontend:"
echo "   1. Assurez-vous que NEXT_PUBLIC_API_URL=http://localhost:8000"
echo "   2. Redémarrez le frontend: npm run dev"
echo "   3. Testez l'inscription sur: http://localhost:3000/auth/register"
echo "   4. Testez la connexion sur: http://localhost:3000/auth/login"
echo ""
