# 🎭 Guide des Tests E2E REFYAI

## Modes de lancement

### 1. Mode UI (Recommandé pour voir les tests) 🌟
```bash
cd /Users/yld/Documents/REFYAI/frontend
npm run test:ui
```
**Avantages:**
- Interface graphique interactive
- Voir les tests en temps réel
- Déboguer facilement
- Rejouer les tests

### 2. Mode Headed (Navigateur visible)
```bash
npm run test:headed
```
**Avantages:**
- Voir le navigateur Chrome s'ouvrir
- Voir chaque action automatique
- Idéal pour les démonstrations

### 3. Mode Debug (Pas à pas)
```bash
npm run test:debug
```
**Avantages:**
- Exécution pas à pas
- Console de débogage
- Inspecter chaque étape

### 4. Mode Headless (Sans interface)
```bash
npm test
```
**Avantages:**
- Plus rapide
- Pour CI/CD
- Tests automatisés

## Tests disponibles

### 🎬 Tests de démonstration (`demo.spec.ts`)

#### Test 1: Flux complet visible
```typescript
test('Démonstration complète: Connexion → Dashboard → Déconnexion')
```
**Ce que vous verrez:**
1. Ouverture de la page de connexion
2. Remplissage automatique du formulaire (avec délai visible)
3. Clic sur "Se connecter"
4. Redirection vers le dashboard
5. Affichage des projets
6. Clic sur "Déconnexion"
7. Retour à la page de connexion

#### Test 2: Vérification des appels API
```typescript
test('Vérification des appels API avec le token')
```
**Ce que vous verrez:**
- Console affichant chaque appel API
- Indication si le token JWT est présent
- Compteur des requêtes authentifiées

#### Test 3: Navigation
```typescript
test('Test de navigation complète')
```
**Ce que vous verrez:**
- Navigation entre les pages
- Redirections automatiques
- Protection des routes

#### Test 4: Performance
```typescript
test('Test de performance: Temps de chargement')
```
**Ce que vous verrez:**
- Mesure des temps de réponse
- Temps de connexion
- Temps de chargement des projets

### 🔐 Tests d'authentification (`auth.spec.ts`)

**8 tests couvrant:**
- ✅ Redirection si non authentifié
- ✅ Connexion valide
- ✅ Connexion invalide
- ✅ Affichage des projets
- ✅ Déconnexion
- ✅ Token JWT dans les requêtes
- ✅ Persistance de session
- ✅ Affichage des KPI

### 🔌 Tests API (`api.spec.ts`)

**9 tests couvrant:**
- ✅ GET /api/projects (liste)
- ✅ GET /api/projects/{id} (détail)
- ✅ POST /api/projects (création)
- ✅ PUT /api/projects/{id} (modification)
- ✅ DELETE /api/projects/{id} (suppression)
- ✅ Sécurité sans token (401)
- ✅ Health check
- ✅ Inscription

## Commandes pratiques

### Lancer uniquement les tests de démo (visuels)
```bash
npm run test:headed -- demo.spec.ts
```

### Lancer uniquement l'authentification
```bash
npm run test:headed -- auth.spec.ts
```

### Lancer uniquement les tests API
```bash
npm run test:headed -- api.spec.ts
```

### Voir le rapport après exécution
```bash
npm run test:report
```

## Ce que vous pouvez observer

### Dans le navigateur visible:

1. **Formulaire de connexion**
   - Remplissage automatique des champs
   - Animation du bouton au clic
   - Message d'erreur si mauvais identifiants

2. **Dashboard**
   - Affichage progressif des KPI
   - Chargement de la liste des projets
   - Email de l'utilisateur en haut à droite
   - Bouton de déconnexion

3. **Appels API**
   - Requêtes visibles dans les DevTools
   - Headers avec token JWT
   - Réponses du backend

### Dans la console:

```
🎬 DÉBUT DE LA DÉMONSTRATION
📍 Étape 1/5: Accès à la page de connexion
✓ Page de connexion affichée
📍 Étape 2/5: Remplissage du formulaire
✓ Formulaire rempli
📍 Étape 3/5: Clic sur le bouton de connexion
✓ Redirection vers le dashboard réussie
📍 Étape 4/5: Exploration du dashboard
✓ Titre du dashboard visible
✓ Email utilisateur affiché
✓ KPI "Projets Totaux" visible
✓ KPI "En Cours" visible
✓ KPI "TRI Moyen" visible
✓ KPI "Investissement Total" visible
✓ Projet "Tour de Bureaux - La Défense" visible
✓ Projet "Résidence Étudiante Lyon" visible
✓ Projet "Centre Commercial Bordeaux" visible
📍 Étape 5/5: Déconnexion
✓ Redirection vers login après déconnexion

✨ DÉMONSTRATION TERMINÉE AVEC SUCCÈS!
```

## Captures d'écran automatiques

Les tests créent automatiquement des captures en cas d'échec:
```
playwright-report/
├── index.html
└── data/
    └── screenshots/
        ├── test-failed-1.png
        ├── test-failed-2.png
        └── ...
```

## Débogage visuel

### Voir une capture d'écran à un moment précis:
```typescript
await page.screenshot({ path: 'debug.png' });
```

### Voir une vidéo du test:
Activé automatiquement en cas d'échec

### Mode pas à pas:
```bash
npm run test:debug
```
Puis cliquer sur "Step over" pour chaque action

## Résultats attendus

### Mode UI - Ce que vous verrez:
![Playwright UI](playwright-ui.png)
- Liste des tests à gauche
- Lecteur vidéo au centre
- Timeline en bas
- Possibilité de rejouer

### Mode Headed - Ce que vous verrez:
- Fenêtre Chrome qui s'ouvre
- Actions automatiques visibles
- Texte surligné pendant les interactions
- Fermeture automatique à la fin

### Console - Ce que vous verrez:
```
Running 4 tests using 1 worker

✓ [chromium] › demo.spec.ts:15:3 › 🎬 Démonstration complète (12.5s)
✓ [chromium] › demo.spec.ts:85:3 › 🔍 Vérification des appels API (5.2s)
✓ [chromium] › demo.spec.ts:145:3 › 📱 Test de navigation (4.1s)
✓ [chromium] › demo.spec.ts:180:3 › ⚡ Test de performance (3.8s)

4 passed (26s)
```

## Problèmes courants

### Le navigateur ne s'ouvre pas
```bash
# Réinstaller Chromium
npx playwright install chromium
```

### Timeout
```bash
# Augmenter le timeout dans playwright.config.ts
timeout: 60000  // 60 secondes
```

### Tests qui échouent
1. Vérifier que le backend est lancé: `curl http://localhost:8000/health`
2. Vérifier que le frontend est lancé: `curl http://localhost:3000`
3. Vérifier le compte demo: Lancer `create_demo_projects.py`

## Scripts rapides

```bash
# Tout voir en mode UI (recommandé)
npm run test:ui

# Démo visuelle uniquement
npm run test:headed -- demo.spec.ts

# Tous les tests avec navigateur
npm run test:headed

# Tests rapides sans interface
npm test

# Rapport HTML
npm run test:report
```

## Pour une présentation

1. Lancer le backend et frontend
2. Exécuter: `npm run test:ui`
3. Cliquer sur le test "Démonstration complète"
4. Cliquer sur "Run" ou "Step"
5. Montrer la vidéo de l'exécution

**Les tests montrent:**
- ✅ L'application fonctionne de bout en bout
- ✅ L'authentification est sécurisée
- ✅ Les API sont bien appelées avec le token
- ✅ Les données sont correctement affichées
- ✅ La navigation est fluide
