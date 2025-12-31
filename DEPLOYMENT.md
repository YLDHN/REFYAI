# 🚀 Guide de Déploiement REFYAI

## 📋 Prérequis

- Compte GitHub
- Compte Render (backend)
- Compte Vercel (frontend)
- Clés API : OpenAI, Mistral (optionnel)

---

## 🔧 Déploiement Backend sur Render

### 1. Créer un compte Render
Allez sur https://render.com et créez un compte (gratuit)

### 2. Créer une base de données PostgreSQL

1. Dans le dashboard Render, cliquez sur **"New +"** → **"PostgreSQL"**
2. Configuration :
   - **Name** : `refyai-db`
   - **Database** : `refyai`
   - **User** : `refyai`
   - **Region** : Europe (Paris ou Frankfurt)
   - **Plan** : Free
3. Cliquez sur **"Create Database"**
4. **Notez l'URL interne** (Internal Database URL) - vous en aurez besoin

### 3. Déployer le Backend

#### Option A : Utiliser le Blueprint (Automatique)

1. Dans Render, cliquez sur **"New +"** → **"Blueprint"**
2. Connectez votre repository GitHub : `YLDHN/REFYAI`
3. Render détectera automatiquement le fichier `render.yaml`
4. Cliquez sur **"Apply"**

#### Option B : Configuration Manuelle

1. Cliquez sur **"New +"** → **"Web Service"**
2. Connectez votre repository GitHub : `YLDHN/REFYAI`
3. Configuration :
   - **Name** : `refyai-backend`
   - **Root Directory** : `backend`
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan** : Free

### 4. Variables d'environnement Backend

Dans la section **"Environment"** de votre service Render :

```env
DATABASE_URL=<URL_INTERNE_POSTGRES>
SECRET_KEY=<GENERER_CLE_SECURISEE>
OPENAI_API_KEY=<VOTRE_CLE_OPENAI>
MISTRAL_API_KEY=<VOTRE_CLE_MISTRAL>
ENVIRONMENT=production
ALLOWED_ORIGINS=https://refyai.vercel.app,https://*.vercel.app
PYTHON_VERSION=3.11
```

#### Générer une clé secrète sécurisée :
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Déploiement

- Cliquez sur **"Create Web Service"**
- Render va automatiquement :
  - Cloner le repository
  - Installer les dépendances
  - Démarrer le serveur
  - Vous donner une URL : `https://refyai-backend.onrender.com`

### 6. Vérifier le Backend

Testez votre backend :
- Health check : `https://refyai-backend.onrender.com/health`
- API docs : `https://refyai-backend.onrender.com/docs`

---

## 🌐 Déploiement Frontend sur Vercel

### 1. Créer un compte Vercel
Allez sur https://vercel.com et créez un compte avec GitHub

### 2. Importer le Projet

1. Dans le dashboard Vercel, cliquez sur **"Add New..."** → **"Project"**
2. Importez le repository : `YLDHN/REFYAI`
3. Configuration :
   - **Framework Preset** : Next.js (détecté automatiquement)
   - **Root Directory** : `frontend`
   - **Build Command** : `npm run build` (par défaut)
   - **Output Directory** : `.next` (par défaut)
   - **Install Command** : `npm install` (par défaut)

### 3. Variables d'environnement Frontend

Dans la section **"Environment Variables"** :

```env
NEXT_PUBLIC_API_URL=https://refyai-backend.onrender.com
```

⚠️ **Important** : Remplacez `refyai-backend.onrender.com` par l'URL réelle de votre backend Render

### 4. Déploiement

1. Cliquez sur **"Deploy"**
2. Vercel va automatiquement :
   - Installer les dépendances
   - Builder l'application
   - Déployer sur CDN global
   - Vous donner une URL : `https://refyai.vercel.app` (ou similaire)

### 5. Configuration du Domaine (Optionnel)

1. Dans Vercel, allez dans **Settings** → **Domains**
2. Ajoutez votre domaine personnalisé
3. Suivez les instructions DNS

---

## 🔄 Déploiement Automatique

Une fois configuré, chaque `git push` sur la branche `main` déclenchera automatiquement :

- ✅ **Render** : Rebuild et redéploiement du backend
- ✅ **Vercel** : Rebuild et redéploiement du frontend

```bash
git add .
git commit -m "feat: nouvelle fonctionnalité"
git push origin main
```

---

## 🔐 Sécurité Post-Déploiement

### Backend (Render)

1. **Activer HTTPS** (activé par défaut)
2. **Limiter les origins CORS** :
   - Remplacez `https://*.vercel.app` par votre URL exacte
3. **Variables d'environnement** :
   - Ne jamais commiter les clés API
   - Utiliser les variables Render

### Frontend (Vercel)

1. **Variables d'environnement** :
   - Seules les variables `NEXT_PUBLIC_*` sont exposées au client
   - Les autres restent côté serveur

---

## 📊 Monitoring

### Render

- **Logs** : Dashboard → Logs (temps réel)
- **Métriques** : CPU, RAM, requêtes
- **Alertes** : Configurer des notifications

### Vercel

- **Analytics** : Dashboard → Analytics
- **Logs** : Dashboard → Deployments → Logs
- **Performance** : Web Vitals, Response Times

---

## 🐛 Dépannage

### Backend ne démarre pas

1. Vérifier les logs Render
2. Vérifier `DATABASE_URL` est correcte
3. Vérifier `requirements.txt` est à jour
4. Tester en local : `uvicorn app.main:app --reload`

### Frontend ne se connecte pas au Backend

1. Vérifier `NEXT_PUBLIC_API_URL` dans Vercel
2. Vérifier CORS dans `backend/app/core/config.py`
3. Tester l'URL backend directement : `/health`
4. Vérifier les logs navigateur (Network tab)

### Base de données vide

1. Se connecter à la DB Render via Shell
2. Exécuter les migrations Alembic :
   ```bash
   alembic upgrade head
   ```

---

## 💰 Coûts

### Plan Gratuit (Suffisant pour démarrer)

- **Render** :
  - Web Service Free : 750h/mois
  - PostgreSQL Free : 1GB, 90 jours puis supprimé
  - ⚠️ Le service s'endort après 15 min d'inactivité (redémarre en ~30s)

- **Vercel** :
  - Hobby Plan : Gratuit
  - 100GB bande passante/mois
  - Déploiements illimités

### Plans Payants (Pour production)

- **Render** :
  - Starter ($7/mois) : Pas de sleep, 512MB RAM
  - PostgreSQL Standard ($7/mois) : Persistent, backups

- **Vercel** :
  - Pro ($20/mois) : Analytics avancés, 1TB bande passante

---

## 🔄 Mises à jour

### Mise à jour du Backend

```bash
cd backend
# Modifier le code
git add .
git commit -m "fix: correction bug"
git push origin main
# Render redéploie automatiquement
```

### Mise à jour du Frontend

```bash
cd frontend
# Modifier le code
git add .
git commit -m "feat: nouveau design"
git push origin main
# Vercel redéploie automatiquement
```

---

## ✅ Checklist Finale

Avant de considérer le déploiement terminé :

- [ ] Backend accessible sur `https://refyai-backend.onrender.com/health`
- [ ] API docs accessibles sur `https://refyai-backend.onrender.com/docs`
- [ ] Frontend accessible sur `https://refyai.vercel.app`
- [ ] Frontend peut appeler l'API (tester une route)
- [ ] Base de données fonctionne (créer un projet test)
- [ ] Variables d'environnement configurées (Backend + Frontend)
- [ ] CORS configuré correctement
- [ ] Déploiement automatique activé (git push)
- [ ] Logs accessibles (Render + Vercel)
- [ ] Clés API configurées (OpenAI, Mistral si nécessaire)

---

## 📚 Ressources

- **Render Docs** : https://render.com/docs
- **Vercel Docs** : https://vercel.com/docs
- **Next.js Deployment** : https://nextjs.org/docs/deployment
- **FastAPI Deployment** : https://fastapi.tiangolo.com/deployment/

---

## 🆘 Support

En cas de problème :

1. Consultez les logs (Render + Vercel)
2. Vérifiez les variables d'environnement
3. Testez en local d'abord
4. Consultez la documentation officielle

**Bon déploiement ! 🚀**
