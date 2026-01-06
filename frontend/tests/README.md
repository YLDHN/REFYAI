# Tests E2E REFYAI

## Description

Suite de tests end-to-end avec Playwright pour valider l'intégration complète frontend-backend de l'application REFYAI.

## Tests d'Authentification (`auth.spec.ts`)

✅ **Redirection vers login si non authentifié**
- Vérifie que l'accès à `/` redirige vers `/login`
- Vérifie l'affichage du formulaire de connexion

✅ **Connexion avec identifiants valides**
- Remplit le formulaire avec demo@refyai.com / demo123
- Vérifie la redirection vers `/dashboard`
- Vérifie l'affichage de l'email utilisateur
- Vérifie la présence du bouton déconnexion

✅ **Connexion avec identifiants invalides**
- Teste avec de mauvais identifiants
- Vérifie le message d'erreur
- Vérifie qu'on reste sur `/login`

✅ **Affichage des projets après connexion**
- Se connecte et accède au dashboard
- Vérifie l'affichage des 3 projets de démo
- Vérifie les statistiques KPI

✅ **Déconnexion et redirection**
- Se connecte puis se déconnecte
- Vérifie la redirection vers `/login`
- Vérifie l'impossibilité d'accéder au dashboard

✅ **Token JWT dans les requêtes API**
- Intercepte les requêtes API
- Vérifie la présence du header `Authorization: Bearer <token>`
- Compte les appels API authentifiés

✅ **Persistance de la session**
- Se connecte
- Recharge la page
- Vérifie que la session est maintenue

✅ **Affichage des KPI**
- Vérifie les 4 cartes statistiques
- Vérifie les valeurs affichées

## Tests API (`api.spec.ts`)

✅ **GET /api/projects**
- Récupère la liste des projets
- Vérifie la structure des données
- Vérifie qu'il y a au moins un projet

✅ **GET /api/projects/{id}**
- Récupère un projet spécifique
- Vérifie les détails du projet

✅ **POST /api/projects**
- Crée un nouveau projet
- Vérifie les données retournées
- Nettoie après le test

✅ **PUT /api/projects/{id}**
- Crée puis modifie un projet
- Vérifie les modifications
- Nettoie après le test

✅ **DELETE /api/projects/{id}**
- Crée puis supprime un projet
- Vérifie le code 204
- Vérifie que le projet n'existe plus (404)

✅ **Sécurité sans token**
- Teste l'accès sans authentification
- Vérifie le code 401

✅ **Health check**
- Vérifie `/health`
- Vérifie le statut du backend et de la base de données

✅ **Inscription d'un nouvel utilisateur**
- Crée un compte
- Vérifie les données utilisateur

## Lancer les tests

### Mode Normal (headless)
```bash
cd frontend
npm test
```

### Mode UI (interface graphique Playwright)
```bash
npm run test:ui
```

### Mode Headed (navigateur visible) 🌟
```bash
npm run test:headed
```

### Mode Debug (pas à pas)
```bash
npm run test:debug
```

### Voir le rapport HTML
```bash
npm run test:report
```

## Prérequis

1. **Backend en cours d'exécution**
```bash
cd /Users/yld/Documents/REFYAI/backend
nohup venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
```

2. **Frontend en cours d'exécution**
```bash
cd /Users/yld/Documents/REFYAI/frontend
npm run dev
```

3. **Compte de test disponible**
- Email: demo@refyai.com
- Mot de passe: demo123
- Au moins 3 projets créés

## Structure des tests

```
frontend/
├── playwright.config.ts          # Configuration Playwright
├── tests/
│   └── e2e/
│       ├── auth.spec.ts          # Tests authentification
│       └── api.spec.ts           # Tests API backend
└── playwright-report/            # Rapports HTML générés
```

## Commandes rapides

```bash
# Tout tester en mode visible
npm run test:headed

# Tester uniquement l'authentification
npm run test:headed -- auth.spec.ts

# Tester uniquement l'API
npm run test:headed -- api.spec.ts

# Mode UI interactif (recommandé)
npm run test:ui
```

## Ce qui est testé

### Frontend → Backend
- ✅ Appels API avec token JWT
- ✅ Gestion des erreurs 401
- ✅ Redirection automatique
- ✅ Persistance de la session

### Backend → Base de données
- ✅ CRUD complet sur les projets
- ✅ Filtrage par user_id
- ✅ Authentification JWT
- ✅ Validation des données

### UI/UX
- ✅ Affichage des formulaires
- ✅ Messages d'erreur
- ✅ Navigation entre pages
- ✅ Affichage des données

## Résultats attendus

```
Running 16 tests using 1 worker

✓ Redirection vers login si non authentifié
✓ Connexion avec identifiants valides
✓ Connexion avec identifiants invalides
✓ Affichage des projets après connexion
✓ Déconnexion et redirection vers login
✓ Token JWT est bien envoyé dans les requêtes API
✓ Persistance de la session après rechargement
✓ Affichage correct des KPI dans le dashboard
✓ GET /api/projects retourne la liste des projets
✓ GET /api/projects/{id} retourne un projet spécifique
✓ POST /api/projects crée un nouveau projet
✓ PUT /api/projects/{id} met à jour un projet
✓ DELETE /api/projects/{id} supprime un projet
✓ Requêtes sans token retournent 401
✓ GET /health vérifie l'état du backend
✓ POST /api/auth/register crée un nouvel utilisateur

16 passed (45s)
```

## Dépannage

### "Error: page.goto: net::ERR_CONNECTION_REFUSED"
→ Le frontend n'est pas démarré. Lancer `npm run dev`

### "Error: 401 Unauthorized"
→ Le compte demo n'existe pas. Créer avec:
```bash
cd backend
venv/bin/python create_demo_projects.py
```

### "Test timeout"
→ Le backend est trop lent. Vérifier qu'il est en cours d'exécution.

### "Cannot find projects"
→ Aucun projet pour l'utilisateur demo. Lancer `create_demo_projects.py`
