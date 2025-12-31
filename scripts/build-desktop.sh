#!/bin/bash

# Script de build de l'application desktop Tauri

echo "🖥️  Build de l'application desktop REFY AI..."

cd frontend

# Vérifier que Rust est installé
if ! command -v cargo &> /dev/null; then
    echo "❌ Rust n'est pas installé."
    echo "   Installez Rust depuis: https://rustup.rs/"
    exit 1
fi

# Installer les dépendances Tauri
echo "📦 Installation des dépendances Tauri..."
npm install

# Build de l'application
echo "🔨 Build en cours..."
npm run tauri build

echo ""
echo "✅ Build terminé !"
echo "📦 L'application se trouve dans: frontend/src-tauri/target/release/"
