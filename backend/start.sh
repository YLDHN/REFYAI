#!/bin/bash

echo "🚀 Lancement du backend REFY AI..."

cd "$(dirname "$0")"

# Activer l'environnement virtuel
. venv/bin/activate

# Lancer le serveur
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
