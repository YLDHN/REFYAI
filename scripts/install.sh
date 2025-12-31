#!/bin/bash

# Script d'installation des dépendances

echo "📦 Installation des dépendances REFY AI..."

# Frontend
echo ""
echo "🎨 Installation des dépendances frontend..."
cd frontend
npm install
cd ..

# Backend
echo ""
echo "🐍 Installation des dépendances backend..."
cd backend

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

cd ..

echo ""
echo "✅ Installation terminée !"
echo ""
echo "🎯 Prochaines étapes:"
echo "   1. Configurer les fichiers .env (backend/.env et frontend/.env)"
echo "   2. Lancer le projet: ./scripts/start.sh"
