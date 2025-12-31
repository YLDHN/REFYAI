#!/bin/bash

# Script de démarrage du projet REFY AI

echo "🚀 Démarrage de REFY AI..."

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker Desktop."
    exit 1
fi

# Vérifier que Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé."
    exit 1
fi

# Créer le fichier .env s'il n'existe pas
if [ ! -f backend/.env ]; then
    echo "📝 Création du fichier .env..."
    cp backend/.env.example backend/.env
    echo "⚠️  N'oubliez pas de configurer votre clé OpenAI dans backend/.env"
fi

if [ ! -f frontend/.env ]; then
    echo "📝 Création du fichier .env frontend..."
    cp frontend/.env.example frontend/.env
fi

# Démarrer les services
echo "🐳 Démarrage des containers Docker..."
docker-compose up -d postgres

echo "⏳ Attente du démarrage de PostgreSQL..."
sleep 5

echo "✅ Services démarrés !"
echo ""
echo "📍 URLs disponibles:"
echo "   - API Backend: http://localhost:8000"
echo "   - Frontend: http://localhost:3000"
echo "   - PostgreSQL: localhost:5432"
echo ""
echo "📝 Commandes utiles:"
echo "   - Voir les logs: docker-compose logs -f"
echo "   - Arrêter: docker-compose down"
echo "   - Redémarrer: docker-compose restart"
echo ""
echo "🎯 Pour développer:"
echo "   Frontend: cd frontend && npm install && npm run dev"
echo "   Backend: cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload"
