#!/bin/bash
# Script de démarrage avec migration automatique de la base de données

set -e

echo "🔄 Running database migrations..."

# Exécuter les migrations Alembic
alembic upgrade head

echo "✅ Database migrations completed"

echo "🚀 Starting application..."

# Démarrer l'application
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
