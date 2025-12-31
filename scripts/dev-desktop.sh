#!/bin/bash

# Script de lancement du mode développement Tauri

echo "🖥️  Lancement de l'application desktop en mode développement..."

cd frontend

# Vérifier que les dépendances sont installées
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances..."
    npm install
fi

# Lancer Tauri en mode dev
echo "🚀 Démarrage..."
npm run tauri dev
