#!/bin/bash

echo "🐍 Installation des dépendances backend..."

cd "$(dirname "$0")"

# Activer l'environnement virtuel
. venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Installation terminée !"
