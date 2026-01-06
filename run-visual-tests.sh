#!/bin/bash

# Script interactif pour lancer les tests Playwright visuels
# Permet de choisir un test spécifique ou de lancer tous les tests


# Vérifier que le backend est bien lancé
BACKEND_URL="http://localhost:8000/health"
echo ""
echo "🔎 Vérification du backend ($BACKEND_URL) ..."

if ! curl -s --fail "$BACKEND_URL" > /dev/null; then
  echo "⚠️  Le backend n'est pas accessible sur $BACKEND_URL."
  echo "⏳ Tentative de démarrage du backend..."
  if [ -f ./backend.sh ]; then
    ./backend.sh &
    sleep 5
  elif [ -f docker-compose.yml ]; then
    docker-compose up -d backend
    sleep 8
  else
    echo "❌ Impossible de trouver un script de démarrage du backend."
    exit 1
  fi
  # Revérifier après démarrage
  if ! curl -s --fail "$BACKEND_URL" > /dev/null; then
    echo "❌ Le backend ne répond toujours pas après tentative de démarrage."
    exit 1
  fi
  echo "✅ Backend démarré avec succès."
fi

cd frontend

echo ""
echo "🎬 ===================================="
echo "   TESTS VISUELS PLAYWRIGHT"
echo "   ===================================="
echo ""
echo "Choisissez un fichier de test:"
echo ""
echo "   1)  🎬 demo.spec.ts - Démonstration visuelle complète"
echo "   2)  🔐 auth.spec.ts - Tests d'authentification"
echo "   3)  🌐 api.spec.ts - Tests API Backend"
echo "   4)  💰 financial.spec.ts - Tests API Financial"
echo "   5)  💵 capex.spec.ts - Tests CAPEX"
echo "   6)  📄 documents.spec.ts - Tests Documents"
echo "   7)  📊 market.spec.ts - Tests Market"
echo "   8)  💸 interest-rate-admin.spec.ts - Tests Taux d'intérêt"
echo "   9)  📝 visual-form-test.spec.ts - Test formulaire visuel"
echo "   10) ⚠️  edge-cases.spec.ts - Tests cas limites"
echo "   11) 🚨 showstoppers.spec.ts - Tests critiques"
echo ""
echo "   99) 🚀 LANCER TOUS LES TESTS"
echo "   0)  ❌ Quitter"
echo ""
read -p "Votre choix: " choice

case $choice in
  1)
    echo ""
    echo "🎬 Lancement: Tests de démonstration..."
    echo ""
    npx playwright test demo.spec.ts --headed
    ;;
  2)
    echo ""
    echo "🔐 Lancement: Tests d'authentification..."
    echo ""
    npx playwright test auth.spec.ts --headed
    ;;
  3)
    echo ""
    echo "🌐 Lancement: Tests API Backend..."
    echo ""
    npx playwright test api.spec.ts --headed
    ;;
  4)
    echo ""
    echo "💰 Lancement: Tests API Financial..."
    echo ""
    npx playwright test financial.spec.ts --headed
    ;;
  5)
    echo ""
    echo "💵 Lancement: Tests CAPEX..."
    echo ""
    npx playwright test capex.spec.ts --headed
    ;;
  6)
    echo ""
    echo "📄 Lancement: Tests Documents..."
    echo ""
    npx playwright test documents.spec.ts --headed
    ;;
  7)
    echo ""
    echo "📊 Lancement: Tests Market..."
    echo ""
    npx playwright test market.spec.ts --headed
    ;;
  8)
    echo ""
    echo "💸 Lancement: Tests Taux d'intérêt..."
    echo ""
    npx playwright test interest-rate-admin.spec.ts --headed
    ;;
  9)
    echo ""
    echo "📝 Lancement: Test formulaire visuel..."
    echo ""
    npx playwright test visual-form-test.spec.ts --headed
    ;;
  10)
    echo ""
    echo "⚠️  Lancement: Tests cas limites..."
    echo ""
    npx playwright test edge-cases.spec.ts --headed
    ;;
  11)
    echo ""
    echo "🚨 Lancement: Tests critiques..."
    echo ""
    npx playwright test showstoppers.spec.ts --headed
    ;;
  99)
    echo ""
    echo "🚀 Lancement de TOUS les tests..."
    echo ""
    npx playwright test tests/e2e/ --headed
    ;;
  0)
    echo ""
    echo "👋 Au revoir!"
    echo ""
    exit 0
    ;;
  *)
    echo ""
    echo "❌ Choix invalide. Veuillez choisir un numéro valide."
    echo ""
    exit 1
    ;;
esac

echo ""
echo "✨ Tests terminés!"
echo ""
