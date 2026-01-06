#!/bin/bash
# 🚀 BACKEND - Démarrage complet (FastAPI + Celery + Redis)

set -e

echo "🚀 REFY AI - BACKEND"
echo "===================="

cd "$(dirname "$0")/backend"

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non installé"
    exit 1
fi

echo "✅ Python: $(python3 --version)"

# Installer dépendances si nécessaire
if [ ! -d "venv" ]; then
    echo "📦 Création environnement virtuel avec Python 3.12..."
    /opt/homebrew/bin/python3.12 -m venv venv
fi

source venv/bin/activate

echo "📦 Installation/Mise à jour dépendances..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Vérifier Redis
if ! command -v redis-server &> /dev/null; then
    echo "⚠️  Redis non installé. Installation..."
    brew install redis
fi

# Créer .env si absent
if [ ! -f .env ]; then
    cat > .env << 'EOF'
DATABASE_URL=postgresql://refyai:refyai@localhost/refyai
OPENAI_API_KEY=sk-your-key-here
CELERY_BROKER_URL=redis://localhost:6379/0
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=dev-secret-key-change-in-production
EOF
    echo "✅ Fichier .env créé"
fi

# Démarrer Redis en arrière-plan si pas actif
if ! pgrep -x "redis-server" > /dev/null; then
    echo "🔴 Démarrage Redis..."
    redis-server --daemonize yes
    sleep 2
fi

redis-cli ping > /dev/null && echo "✅ Redis actif"

# Démarrer Celery workers en arrière-plan
echo "⚙️  Démarrage Celery workers..."
celery -A celery_app worker --loglevel=info --detach --pidfile=/tmp/celery.pid --logfile=logs/celery.log

sleep 2
echo "✅ Celery workers actifs"

# Démarrer FastAPI
echo "🚀 Démarrage Backend FastAPI..."
echo ""
echo "📍 Backend: http://localhost:8000"
echo "📚 Swagger: http://localhost:8000/api/docs"
echo "📖 ReDoc: http://localhost:8000/api/redoc"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
