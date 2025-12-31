#!/bin/bash

# Script de création de la base de données

echo "🗄️  Initialisation de la base de données..."

# Se connecter au container PostgreSQL et créer les migrations
cd backend

# Activer l'environnement virtuel
source venv/bin/activate

# Exécuter les migrations Alembic
echo "📝 Application des migrations..."
alembic upgrade head

echo "✅ Base de données initialisée !"
