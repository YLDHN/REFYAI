# Système d'Authentification REFYAI

## Vue d'ensemble

L'application utilise un système d'authentification JWT (JSON Web Token) complet avec :
- Connexion/Déconnexion
- Protection des routes API backend
- Protection des pages frontend
- Gestion d'état avec Zustand
- Token stocké en local storage

## Architecture

### Frontend

#### Store d'authentification (`/frontend/src/store/authStore.ts`)
- Gestion d'état avec Zustand et middleware persist
- Stockage du token JWT et des informations utilisateur
- Méthodes: `setAuth()`, `logout()`
- Persistance dans localStorage sous la clé `auth-storage`

#### Page de connexion (`/frontend/src/app/login/page.tsx`)
- Formulaire email/mot de passe
- Appel à l'API `/api/auth/login`
- Stockage du token et redirection vers dashboard
- Affichage des erreurs

#### Configuration API (`/frontend/src/lib/api.ts`)
- Intercepteur de requête : ajout automatique du header `Authorization: Bearer <token>`
- Intercepteur de réponse : déconnexion automatique si erreur 401
- Récupération du token depuis le localStorage

#### Protection des pages
- Dashboard et autres pages protégées vérifient `isAuthenticated`
- Redirection vers `/login` si non authentifié
- Page d'accueil (`/`) redirige automatiquement vers dashboard ou login

### Backend

#### Endpoints d'authentification (`/backend/app/api/auth.py`)

##### POST `/api/auth/register`
Inscription d'un nouvel utilisateur
```json
{
  "email": "user@example.com",
  "password": "motdepasse123",
  "full_name": "Jean Dupont"
}
```

##### POST `/api/auth/login`
Connexion (OAuth2 form data)
```
username=user@example.com&password=motdepasse123
```

Retourne:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "Jean Dupont",
    "is_active": true,
    "is_superuser": false
  }
}
```

##### GET `/api/auth/me`
Récupérer les informations de l'utilisateur connecté (nécessite authentification)

#### Protection des endpoints API
- Tous les endpoints de projets nécessitent authentification
- Utilisation de `Depends(get_current_active_user)`
- Filtrage automatique des données par `user_id`

Exemples :
- `GET /api/projects/` - Liste les projets de l'utilisateur connecté uniquement
- `POST /api/projects/` - Crée un projet lié à l'utilisateur connecté
- `GET /api/projects/{id}` - Vérifie que le projet appartient à l'utilisateur

## Utilisation

### Compte de démonstration
```
Email: demo@refyai.com
Mot de passe: demo123
```

### Créer un nouveau compte
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nouveau@exemple.com",
    "password": "monmotdepasse",
    "full_name": "Nom Complet"
  }'
```

### Se connecter
1. Ouvrir http://localhost:3000
2. Entrer email et mot de passe
3. Le token est automatiquement stocké
4. Redirection vers le dashboard

### Se déconnecter
- Cliquer sur le bouton "Déconnexion" dans le dashboard
- Le token est supprimé du localStorage
- Redirection vers la page de connexion

## Sécurité

### Token JWT
- Algorithme : HS256
- Durée de vie : 7 jours (configurable dans `backend/app/core/config.py`)
- Stocké côté client dans localStorage
- Envoyé dans le header `Authorization: Bearer <token>`

### Mots de passe
- Hachage avec bcrypt
- Salt automatique
- Vérification sécurisée avec `verify_password()`

### Protection CSRF
- Les tokens JWT remplacent les sessions traditionnelles
- Pas de cookies, donc pas de risque CSRF

## Flux d'authentification

```
1. Utilisateur → /login
2. Submit formulaire → POST /api/auth/login
3. Backend vérifie email/password
4. Backend génère JWT token
5. Frontend stocke token + user dans Zustand
6. Zustand persiste dans localStorage
7. Toutes les requêtes API incluent le token
8. Backend valide le token à chaque requête
9. Backend filtre les données par user_id
```

## Dépannage

### "Email ou mot de passe incorrect"
- Vérifier l'email et le mot de passe
- Le mot de passe est sensible à la casse
- Créer un nouveau compte si nécessaire

### Redirection en boucle vers /login
- Token expiré ou invalide
- Supprimer manuellement le localStorage : `localStorage.clear()`
- Se reconnecter

### API retourne 401 Unauthorized
- Token manquant ou expiré
- Se reconnecter pour obtenir un nouveau token
- Vérifier que le header Authorization est bien envoyé

### Projets vides après connexion
- Compte nouveau sans projets
- Créer un projet via "Nouveau Projet"
- Ou utiliser le compte demo (demo@refyai.com / demo123)

## Configuration

### Variables d'environnement Backend
```env
# backend/.env
SECRET_KEY=votre_cle_secrete_tres_longue
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 jours
```

### Variables d'environnement Frontend
```env
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Développement

### Désactiver temporairement l'authentification
Pour tester rapidement, commenter la ligne dans les endpoints :
```python
# current_user: User = Depends(get_current_active_user)
```

### Créer des projets de test pour un utilisateur
```bash
cd backend
venv/bin/python create_demo_projects.py
```

### Réinitialiser les utilisateurs
```sql
-- Se connecter à PostgreSQL
DELETE FROM projects;
DELETE FROM users;
```
