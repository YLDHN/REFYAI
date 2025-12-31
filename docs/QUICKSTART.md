# Guide de démarrage rapide REFY AI

## 🚀 Installation en 5 minutes

### Prérequis

Assurez-vous d'avoir installé :

- [Node.js 20+](https://nodejs.org/)
- [Python 3.12+](https://www.python.org/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Étape 1 : Installation

```bash
# Cloner le projet
git clone <votre-repo>
cd REFYAI

# Installer les dépendances
./scripts/install.sh
```

### Étape 2 : Configuration

```bash
# Copier les fichiers d'environnement
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Éditez `backend/.env` et ajoutez votre clé OpenAI :

```env
OPENAI_API_KEY=sk-votre-cle-ici
```

### Étape 3 : Démarrage

```bash
# Démarrer avec Docker
docker-compose up -d

# OU manuellement

# Terminal 1 : PostgreSQL
docker-compose up -d postgres

# Terminal 2 : Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 3 : Frontend
cd frontend
npm run dev
```

### Étape 4 : Initialiser la base de données

```bash
./scripts/init-db.sh
```

### ✅ C'est prêt !

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **API Docs** : http://localhost:8000/docs

---

## 🖥️ Application Desktop (optionnel)

### Prérequis supplémentaires

- [Rust](https://rustup.rs/)

### Développement

```bash
./scripts/dev-desktop.sh
```

### Build

```bash
./scripts/build-desktop.sh
```

---

## 📚 Prochaines étapes

- Consultez le [README complet](../README.md)
- Lisez le [guide de développement](DEVELOPMENT.md)
- Explorez les [exemples d'API](http://localhost:8000/docs)

---

## ❓ Problèmes courants

### Le backend ne démarre pas

```bash
# Vérifier que PostgreSQL est lancé
docker-compose ps

# Vérifier les logs
docker-compose logs postgres
```

### Erreur de dépendances Python

```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

### Erreur de dépendances Node

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port déjà utilisé

```bash
# Changer le port dans .env
NEXT_PUBLIC_API_URL=http://localhost:8001

# Ou arrêter le processus
lsof -ti:8000 | xargs kill -9
```

---

Pour plus d'aide, consultez la [documentation complète](../README.md).
