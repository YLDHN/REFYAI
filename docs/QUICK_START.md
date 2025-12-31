# 🚀 QUICK START GUIDE - REFY AI

## ⚡ Démarrage Rapide

### 1. Premier lancement (Setup complet)

```bash
# Clone (si pas déjà fait)
git clone https://github.com/votre-repo/REFYAI.git
cd REFYAI

# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API

# Base de données
docker-compose up -d  # Lance PostgreSQL
alembic upgrade head  # Lance migrations

# Démarrer backend
uvicorn app.main:app --reload --port 8000

# Frontend Setup (nouveau terminal)
cd ../frontend
npm install
npm run dev
```

**URLs**:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Docs API: http://localhost:8000/docs

---

### 2. Lancement quotidien (déjà configuré)

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Base de données (si pas déjà lancée)
docker-compose up -d
```

---

## 🔧 Commandes Utiles

### Backend

```bash
# Activer venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows

# Installer dépendances
pip install -r requirements.txt

# Lancer serveur
uvicorn app.main:app --reload --port 8000

# Lancer avec logs détaillés
uvicorn app.main:app --reload --port 8000 --log-level debug

# Tests
pytest tests/ -v
pytest tests/test_capex_service.py -v
pytest tests/ --cov=app --cov-report=html

# Migrations DB
alembic revision --autogenerate -m "Description migration"
alembic upgrade head
alembic downgrade -1
alembic current
alembic history

# Linter
black app/
flake8 app/
mypy app/

# Docker
docker-compose up -d         # Lance containers
docker-compose down          # Arrête containers
docker-compose logs -f       # Logs en temps réel
docker-compose ps            # Status containers
```

---

### Frontend

```bash
# Installer dépendances
npm install

# Développement
npm run dev

# Build production
npm run build
npm run start

# Linter
npm run lint
npm run lint:fix

# Tests (quand créés)
npm run test
npm run test:watch
npm run test:e2e

# Nettoyage
rm -rf .next node_modules
npm install
```

---

### Base de Données

```bash
# Connexion psql
docker exec -it refyai-postgres psql -U refyai -d refyai

# Backup
docker exec refyai-postgres pg_dump -U refyai refyai > backup.sql

# Restore
docker exec -i refyai-postgres psql -U refyai refyai < backup.sql

# Reset complet
docker-compose down -v
docker-compose up -d
cd backend
alembic upgrade head
```

---

## 📝 Fichiers de Configuration

### Backend `.env`
```env
# Database
DATABASE_URL=postgresql+asyncpg://refyai:refyai@localhost:5432/refyai

# Security
SECRET_KEY=your-secret-key-change-in-production
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# OpenAI
OPENAI_API_KEY=sk-...

# DVF API (pas de clé requise)
DVF_API_URL=https://api.cquest.org/dvf

# Euribor API (pas de clé requise)
EURIBOR_API_URL=https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.RT.MM
EURIBOR_FALLBACK_RATE=3.45

# Uploads
UPLOAD_DIR=/tmp/refyai_uploads

# Environment
ENVIRONMENT=development
```

---

### Frontend `.env.local`
```env
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
```

---

## 🐛 Debugging

### Backend ne démarre pas

```bash
# Vérifier port libre
lsof -i :8000
kill -9 <PID>

# Vérifier venv activé
which python  # Doit pointer vers venv/bin/python

# Vérifier dépendances
pip list | grep fastapi
pip install --upgrade fastapi

# Logs détaillés
uvicorn app.main:app --reload --log-level debug
```

---

### Frontend ne démarre pas

```bash
# Vérifier port libre
lsof -i :3000
kill -9 <PID>

# Cache Next.js
rm -rf .next
npm run dev

# Dépendances
rm -rf node_modules package-lock.json
npm install
```

---

### Base de données ne se connecte pas

```bash
# Vérifier container actif
docker ps | grep postgres

# Redémarrer container
docker-compose restart postgres

# Logs PostgreSQL
docker-compose logs -f postgres

# Test connexion
docker exec -it refyai-postgres psql -U refyai -d refyai
```

---

### Migrations échouent

```bash
# Vérifier version actuelle
alembic current

# Rollback
alembic downgrade -1

# Recréer DB
docker-compose down -v
docker-compose up -d
alembic upgrade head

# Régénérer migration
alembic revision --autogenerate -m "New migration"
```

---

## 📊 Vérifications Santé

### Backend OK ✅
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}

curl http://localhost:8000/
# Response: {"message": "REFY AI API", "version": "1.0.0", "status": "running"}
```

---

### Frontend OK ✅
```bash
curl http://localhost:3000
# Response: HTML page

# Dans navigateur
open http://localhost:3000
```

---

### Base de Données OK ✅
```bash
docker exec refyai-postgres psql -U refyai -d refyai -c "SELECT COUNT(*) FROM projects;"
# Doit retourner nombre de projets
```

---

### APIs Externes OK ✅
```bash
# Test DVF API
curl "https://api.cquest.org/dvf?code_commune=75056&type_local=Appartement" | jq

# Test Euribor API
curl "https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.RT.MM.EURIBOR3MD_.HSTA?format=jsondata&lastNObservations=1" | jq
```

---

## 🧪 Tests Rapides

### Tester service CAPEX
```bash
# Démarrer backend
uvicorn app.main:app --reload --port 8000

# Nouveau terminal
curl -X POST "http://localhost:8000/api/v1/capex/estimate?item_key=facade_ravalement_simple&quantity=100&city_tier=1" | jq
```

---

### Tester service délais admin
```bash
curl -X POST "http://localhost:8000/api/v1/admin-delays/procedure" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Paris",
    "procedure_type": "permis_construire",
    "complexity": 1.5,
    "has_abf": true
  }' | jq
```

---

### Tester DVF API
```bash
curl "http://localhost:8000/api/v1/market/comparables/Paris?type_local=Appartement" | jq
```

---

### Tester questionnaire
```bash
curl "http://localhost:8000/api/v1/questionnaire/questions" | jq
```

---

## 📚 Documentation

### Swagger UI (Auto-générée)
```
http://localhost:8000/docs
```

### ReDoc (Alternative)
```
http://localhost:8000/redoc
```

### Documentation Markdown
- `docs/BACKEND_COMPLETION_REPORT.md` - Backend complet
- `docs/PROJECT_STATUS.md` - État projet
- `docs/SERVICES.md` - Services backend
- `docs/GAPS_TODO.md` - Ce qui reste à faire
- `docs/API_CONFIGURATION.md` - Config APIs externes
- `docs/AUDIT_COMPLET.md` - Audit complet
- `docs/BUSINESS_PLAN_TECHNIQUE.md` - BP technique

---

## 🎯 Workflows Courants

### Ajouter un nouveau service

```bash
# 1. Créer fichier service
touch backend/app/services/mon_service.py

# 2. Créer routes API
touch backend/app/api/mon_service.py

# 3. Enregistrer dans __init__.py
# Ajouter: from app.api import mon_service
# Ajouter: api_router.include_router(mon_service.router)

# 4. Tests
touch backend/tests/test_mon_service.py
pytest tests/test_mon_service.py -v

# 5. Documentation
# Mettre à jour docs/SERVICES.md
```

---

### Ajouter une nouvelle page frontend

```bash
# 1. Créer page
mkdir -p frontend/src/app/ma-page
touch frontend/src/app/ma-page/page.tsx

# 2. Ajouter navigation dans Sidebar.tsx

# 3. Créer composants spécifiques
mkdir -p frontend/src/components/ma-page
touch frontend/src/components/ma-page/MonComposant.tsx

# 4. Hooks API
touch frontend/src/hooks/useMaPage.ts

# 5. Tests E2E
touch frontend/tests/e2e/ma-page.spec.ts
```

---

### Nouvelle migration DB

```bash
cd backend

# 1. Modifier models/
nano app/models/project.py

# 2. Auto-générer migration
alembic revision --autogenerate -m "Add new column"

# 3. Vérifier fichier généré
cat alembic/versions/<revision>_add_new_column.py

# 4. Appliquer
alembic upgrade head

# 5. Vérifier
alembic current
```

---

## 🔐 Sécurité

### Générer nouvelle SECRET_KEY

```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

### Changer mot de passe DB

```bash
# .env
DATABASE_URL=postgresql+asyncpg://refyai:NEW_PASSWORD@localhost:5432/refyai

# docker-compose.yml
POSTGRES_PASSWORD: NEW_PASSWORD

# Recréer container
docker-compose down -v
docker-compose up -d
```

---

## 📞 Support

### Logs Backend
```bash
tail -f backend/logs/app.log
```

### Logs Frontend
```bash
npm run dev 2>&1 | tee frontend.log
```

### Logs PostgreSQL
```bash
docker-compose logs -f postgres
```

---

## ✅ Checklist Déploiement

- [ ] Variables `.env` production remplies
- [ ] `SECRET_KEY` unique et sécurisée
- [ ] `ALLOWED_ORIGINS` configuré
- [ ] OpenAI API key valide
- [ ] Migrations DB lancées
- [ ] Tests passent (pytest)
- [ ] Build frontend OK (npm run build)
- [ ] HTTPS configuré
- [ ] Monitoring actif
- [ ] Backups DB automatiques
- [ ] Rate limiting activé
- [ ] Logs centralisés

---

**Dernière mise à jour**: 31 Décembre 2025  
**Version**: 1.0
