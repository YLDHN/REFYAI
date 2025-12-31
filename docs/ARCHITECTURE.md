# Architecture technique REFY AI

## 📐 Vue d'ensemble

REFY AI est construit selon une **architecture client-serveur moderne** avec séparation claire entre :

- **Frontend** : Next.js (web) + Tauri (desktop)
- **Backend** : FastAPI (API REST)
- **Base de données** : PostgreSQL (données) + ChromaDB (vecteurs IA)

---

## 🏗️ Architecture système

```
┌─────────────────────────────────────────────────────────────┐
│                        UTILISATEURS                          │
│                                                              │
│  ┌──────────────────┐          ┌─────────────────────┐     │
│  │   Navigateur Web │          │  Application Desktop│     │
│  │   (React/Next.js)│          │      (Tauri)        │     │
│  └────────┬─────────┘          └──────────┬──────────┘     │
└───────────┼────────────────────────────────┼────────────────┘
            │                                │
            │         HTTP/REST API          │
            └────────────┬───────────────────┘
                         │
         ┌───────────────▼──────────────────┐
         │        BACKEND FastAPI            │
         │                                   │
         │  ┌─────────────────────────────┐ │
         │  │    API Routes               │ │
         │  │  /api/v1/projects           │ │
         │  │  /api/v1/documents          │ │
         │  │  /api/v1/analysis           │ │
         │  └──────────┬──────────────────┘ │
         │             │                     │
         │  ┌──────────▼──────────────────┐ │
         │  │   SERVICES MÉTIER           │ │
         │  │                             │ │
         │  │  ┌─────────────────┐        │ │
         │  │  │  AI Service     │        │ │
         │  │  │  (OpenAI/GPT-4) │        │ │
         │  │  └─────────────────┘        │ │
         │  │                             │ │
         │  │  ┌─────────────────┐        │ │
         │  │  │ Financial       │        │ │
         │  │  │ Service         │        │ │
         │  │  └─────────────────┘        │ │
         │  │                             │ │
         │  │  ┌─────────────────┐        │ │
         │  │  │ Excel Service   │        │ │
         │  │  └─────────────────┘        │ │
         │  └──────────┬──────────────────┘ │
         └─────────────┼────────────────────┘
                       │
         ┌─────────────▼──────────────────┐
         │     DONNÉES                     │
         │                                 │
         │  ┌─────────────┐  ┌──────────┐ │
         │  │ PostgreSQL  │  │ChromaDB  │ │
         │  │ (Principal) │  │(Vecteurs)│ │
         │  └─────────────┘  └──────────┘ │
         └─────────────────────────────────┘
```

---

## 🎨 Frontend Architecture

### Next.js (Web)

```
frontend/src/
├── app/                      # App Router
│   ├── (auth)/              # Groupe d'authentification
│   │   ├── login/
│   │   └── register/
│   │
│   ├── (dashboard)/         # Groupe dashboard (protégé)
│   │   ├── projects/
│   │   ├── analysis/
│   │   └── settings/
│   │
│   ├── layout.tsx           # Layout racine
│   └── page.tsx             # Page d'accueil
│
├── components/
│   ├── ui/                  # Composants UI réutilisables
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Input.tsx
│   │
│   ├── features/            # Composants métier
│   │   ├── ProjectCard.tsx
│   │   ├── AnalysisChart.tsx
│   │   └── AIChat.tsx
│   │
│   └── layouts/             # Layouts
│       ├── Header.tsx
│       └── Sidebar.tsx
│
├── lib/                     # Bibliothèques
│   ├── api.ts              # Client HTTP (Axios)
│   ├── utils.ts            # Utilitaires
│   └── store.ts            # État global (Zustand)
│
└── types/                   # Types TypeScript
    ├── project.ts
    ├── user.ts
    └── api.ts
```

### Tauri (Desktop)

```
frontend/src-tauri/
├── src/
│   └── main.rs             # Point d'entrée Rust
│
├── Cargo.toml              # Dépendances Rust
└── tauri.conf.json         # Configuration
```

**Principe** : Le même code Next.js est utilisé pour le web et le desktop.

---

## ⚙️ Backend Architecture

### FastAPI

```
backend/app/
├── main.py                 # Point d'entrée
│
├── core/                   # Configuration centrale
│   ├── config.py          # Settings (Pydantic)
│   ├── database.py        # Session DB
│   └── security.py        # JWT, hashing
│
├── models/                 # Modèles SQLAlchemy (ORM)
│   ├── user.py
│   ├── project.py
│   └── document.py
│
├── schemas/                # Schémas Pydantic (validation)
│   ├── user.py
│   ├── project.py
│   └── document.py
│
├── api/                    # Routes API
│   └── v1/
│       ├── auth.py        # POST /login, /register
│       ├── projects.py    # CRUD projets
│       ├── documents.py   # Upload, analyse
│       └── analysis.py    # Calculs, IA
│
├── services/               # Logique métier
│   ├── ai_service.py      # Analyse IA
│   ├── financial_service.py  # Calculs financiers
│   └── excel_service.py   # Génération BP Excel
│
└── utils/                  # Utilitaires
    ├── pdf_parser.py
    └── validators.py
```

---

## 🗄️ Modèle de données

### Schéma relationnel

```
┌──────────────┐
│    users     │
├──────────────┤
│ id           │◄──┐
│ email        │   │
│ password     │   │
│ full_name    │   │
│ created_at   │   │
└──────────────┘   │
                   │
                   │ 1:N
                   │
┌──────────────┐   │
│   projects   │───┘
├──────────────┤
│ id           │◄──┐
│ user_id      │   │
│ name         │   │
│ address      │   │
│ status       │   │
│ financial_*  │   │ 1:N
│ created_at   │   │
└──────────────┘   │
                   │
┌──────────────┐   │
│  documents   │───┘
├──────────────┤
│ id           │
│ project_id   │
│ filename     │
│ file_path    │
│ type         │
│ is_analyzed  │
│ uploaded_at  │
└──────────────┘
```

### Modèles principaux

#### User
- Authentification et profil utilisateur
- Liens vers ses projets

#### Project
- Centre du système
- Contient les données du projet immobilier
- Stocke les résultats d'analyses (JSON)

#### Document
- Fichiers uploadés (PLU, diagnostics, etc.)
- Référence vers le projet
- Résultat d'analyse IA

---

## 🤖 Services métier

### AI Service

**Responsabilités** :
- Analyse de documents (PLU, diagnostics)
- Extraction d'informations
- Chat métier

**Technologies** :
- OpenAI GPT-4
- LangChain (orchestration)
- ChromaDB (recherche sémantique)

**Flow** :
```
Document PDF
    ↓
Extraction texte (PyPDF2)
    ↓
Découpage en chunks
    ↓
Vectorisation (ChromaDB)
    ↓
Prompt + Context → GPT-4
    ↓
Analyse structurée
```

### Financial Service

**Responsabilités** :
- Calculs financiers complexes
- TRI, VAN, LTV, DSCR, ROI
- Simulations de scénarios

**Technologies** :
- NumPy
- SciPy (optimisation)
- Pandas (données)

**Formules implémentées** :
```python
TRI = IRR(cash_flows)
VAN = NPV(discount_rate, cash_flows)
LTV = loan_amount / property_value
DSCR = NOI / debt_service
```

### Excel Service

**Responsabilités** :
- Génération de Business Plan Excel
- Formules dynamiques
- Mise en forme professionnelle

**Technologies** :
- XlsxWriter (génération)
- OpenPyXL (manipulation)

**Onglets générés** :
1. Synthèse
2. Hypothèses
3. Plan de financement
4. Compte de résultat
5. Indicateurs financiers

---

## 🔐 Sécurité

### Authentification

**JWT (JSON Web Tokens)** :
```
Client → POST /api/v1/auth/login
         ↓
Backend vérifie credentials
         ↓
Génère JWT token
         ↓
Client stocke le token
         ↓
Client envoie token dans headers:
Authorization: Bearer <token>
```

### Protection des routes

```python
from fastapi import Depends
from app.core.security import get_current_user

@router.get("/projects")
async def get_projects(
    current_user: User = Depends(get_current_user)
):
    # Route protégée
    return projects
```

### Validation des données

**Pydantic** valide automatiquement :
```python
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    purchase_price: float = Field(..., gt=0)
    email: EmailStr
```

---

## 📊 Flux de données typiques

### Création d'un projet

```
1. User clique "Nouveau projet"
   ↓
2. Frontend affiche formulaire
   ↓
3. User remplit et soumet
   ↓
4. POST /api/v1/projects
   ↓
5. Backend valide (Pydantic)
   ↓
6. Backend enregistre (PostgreSQL)
   ↓
7. Backend retourne project_id
   ↓
8. Frontend redirige vers /projects/{id}
```

### Upload et analyse d'un document

```
1. User upload un PDF
   ↓
2. POST /api/v1/documents
   ↓
3. Backend stocke le fichier
   ↓
4. Backend déclenche l'analyse IA
   ↓
5. AI Service extrait le texte
   ↓
6. AI Service vectorise (ChromaDB)
   ↓
7. AI Service envoie à GPT-4
   ↓
8. Résultat stocké en JSON
   ↓
9. Frontend affiche l'analyse
```

### Génération de Business Plan

```
1. User clique "Générer BP"
   ↓
2. GET /api/v1/projects/{id}/export/excel
   ↓
3. Financial Service calcule indicateurs
   ↓
4. Excel Service génère le fichier
   ↓
5. Backend retourne le fichier
   ↓
6. Frontend télécharge automatiquement
```

---

## 🚀 Scalabilité

### Actuelle (MVP)

- **Monolithique** : Backend unique
- **Base de données** : PostgreSQL unique
- **Déploiement** : Docker Compose

### Future (V2+)

- **Microservices** :
  - Service Auth
  - Service Projects
  - Service AI
  - Service Excel

- **Queue de tâches** : Celery + Redis
- **Cache** : Redis
- **CDN** : Cloudflare
- **Load balancer** : NGINX

---

## 🛠️ DevOps

### Développement

```bash
docker-compose up -d  # Services locaux
```

### Production (à venir)

```yaml
# Exemple Kubernetes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: refyai-backend
spec:
  replicas: 3
  ...
```

---

## 📈 Monitoring (à venir)

- **Logs** : Sentry
- **Performance** : New Relic
- **Uptime** : UptimeRobot

---

Pour plus de détails techniques, consultez :
- [Guide de développement](DEVELOPMENT.md)
- [Documentation API](http://localhost:8000/docs)
