# Guide de Déploiement REFY AI

## 🚀 Déploiement Backend sur Render

### 1. Créer un compte Render
- Allez sur [render.com](https://render.com)
- Créez un compte (gratuit)

### 2. Créer la base de données PostgreSQL
1. Dans le dashboard Render, cliquez sur **"New +"** → **"PostgreSQL"**
2. Configurez :
   - **Name**: `refyai-db`
   - **Database**: `refyai`
   - **User**: `refyai`
   - **Region**: `Frankfurt` (ou plus proche de vous)
   - **Plan**: `Free`
3. Cliquez sur **"Create Database"**
4. **IMPORTANT**: Notez l'URL de connexion (Internal Database URL)

### 3. Déployer le Backend
1. Dans le dashboard, cliquez sur **"New +"** → **"Blueprint"**
2. Connectez votre repository GitHub
3. Le fichier `render.yaml` sera automatiquement détecté
4. Cliquez sur **"Apply"**

### 4. Configurer les variables d'environnement sur Render
Allez dans votre service `refyai-backend` → **Environment** et ajoutez :

```bash
# Variables à configurer manuellement (sync: false dans render.yaml)

# OBLIGATOIRE - Vos domaines frontend (séparer par des virgules)
ALLOWED_ORIGINS=https://votre-app.vercel.app,https://*.vercel.app,http://localhost:3000

# OBLIGATOIRE - Votre clé OpenAI
OPENAI_API_KEY=sk-votre-cle-openai-ici

# Les autres variables sont auto-générées par render.yaml :
# - DATABASE_URL (lié automatiquement à refyai-db)
# - SECRET_KEY (généré automatiquement)
# - PYTHON_VERSION, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, etc.
```

### 5. Récupérer l'URL du Backend
Une fois déployé, votre backend sera accessible à :
```
https://refyai-backend.onrender.com
```
**Notez cette URL** pour la configuration Vercel.

---

## 🌐 Déploiement Frontend sur Vercel

### 1. Créer un compte Vercel
- Allez sur [vercel.com](https://vercel.com)
- Créez un compte avec GitHub

### 2. Importer le projet
1. Cliquez sur **"Add New..."** → **"Project"**
2. Importez votre repository GitHub
3. Configurez :
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend`
   - **Build Command**: `npx prisma generate && npm run build`
   - **Output Directory**: `.next`

### 3. Configurer les variables d'environnement sur Vercel
Dans **Settings** → **Environment Variables**, ajoutez :

```bash
# OBLIGATOIRE - URL de votre backend Render
NEXT_PUBLIC_API_URL=https://refyai-backend.onrender.com

# Pour tous les environnements (Production, Preview, Development)
```

**IMPORTANT**: Cochez les 3 cases :
- ✅ Production
- ✅ Preview
- ✅ Development

### 4. Mettre à jour vercel.json
Si votre backend n'est pas à `https://refyai-backend.onrender.com`, modifiez dans `frontend/vercel.json` :

```json
"rewrites": [
  {
    "source": "/api/:path*",
    "destination": "https://VOTRE-BACKEND.onrender.com/:path*"
  }
]
```

### 5. Déployer
1. Cliquez sur **"Deploy"**
2. Attendez la fin du build (2-3 minutes)
3. Votre application sera accessible à : `https://votre-app.vercel.app`

---

## 🔄 Mettre à jour le CORS

### Sur Render (Backend)
Mettez à jour `ALLOWED_ORIGINS` avec votre vraie URL Vercel :
```bash
ALLOWED_ORIGINS=https://votre-app.vercel.app,https://*.vercel.app
```

### Redémarrer les services
- Backend Render : **Manual Deploy** → **Clear build cache & deploy**
- Frontend Vercel : **Deployments** → **Redeploy**

---

## ✅ Vérifier le déploiement

### 1. Tester le Backend
```bash
curl https://refyai-backend.onrender.com/health
# Devrait retourner: {"status":"healthy"}
```

### 2. Tester le Frontend
1. Allez sur `https://votre-app.vercel.app`
2. Connectez-vous avec : `demo@refyai.com` / `demo123`
3. Vérifiez que le dashboard charge les projets

---

## 🐛 Dépannage

### Backend Render ne démarre pas
1. Vérifiez les logs : **Logs** dans le dashboard
2. Vérifiez que `DATABASE_URL` est bien configuré
3. Vérifiez que `ALLOWED_ORIGINS` contient votre URL Vercel

### Frontend Vercel - Erreur 500
1. Vérifiez que `NEXT_PUBLIC_API_URL` est configuré
2. Vérifiez les logs : **Deployments** → Cliquez sur le déploiement → **Build Logs**
3. Vérifiez que Prisma génère bien les types : `npx prisma generate`

### CORS Error
```
Access to fetch at 'https://refyai-backend.onrender.com/...' from origin 'https://votre-app.vercel.app' has been blocked by CORS
```

**Solution** : Mettez à jour `ALLOWED_ORIGINS` sur Render avec votre URL Vercel exacte.

---

## 📊 Plan Gratuit - Limites

### Render (Backend)
- ✅ 750 heures/mois
- ⚠️ Le service s'endort après 15 min d'inactivité
- ⏱️ Première requête peut prendre 30-60 secondes (cold start)
- 💾 PostgreSQL: 1GB storage

### Vercel (Frontend)
- ✅ 100GB bandwidth/mois
- ✅ Déploiements illimités
- ✅ Pas de cold start

---

## 🔐 Sécurité en Production

### Avant de mettre en production
1. ✅ Changez `SECRET_KEY` (laissez Render le générer)
2. ✅ Ajoutez votre clé OpenAI
3. ✅ Configurez `ALLOWED_ORIGINS` avec vos vrais domaines
4. ✅ Activez HTTPS (automatique sur Render et Vercel)
5. ✅ Créez un utilisateur admin (pas juste le compte démo)

---

## 📞 Support
Si vous rencontrez des problèmes :
1. Vérifiez les logs Render et Vercel
2. Vérifiez que toutes les variables d'environnement sont configurées
3. Testez le backend avec curl avant de tester le frontend
