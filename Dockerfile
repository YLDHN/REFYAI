# Dockerfile pour backend FastAPI REFY AI
FROM python:3.12-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système (si nécessaire pour psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code backend
COPY backend/ .

# Créer les dossiers nécessaires
RUN mkdir -p logs uploads

# Exposer le port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Commande de démarrage
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
