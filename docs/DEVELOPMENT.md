# Guide de développement REFY AI

## 📚 Table des matières

1. [Structure du projet](#structure-du-projet)
2. [Configuration de l'environnement](#configuration-de-lenvironnement)
3. [Développement Frontend](#développement-frontend)
4. [Développement Backend](#développement-backend)
5. [Base de données](#base-de-données)
6. [IA et Services](#ia-et-services)
7. [Tests](#tests)
8. [Bonnes pratiques](#bonnes-pratiques)

---

## 🏗️ Structure du projet

### Frontend (Next.js + TypeScript + Tailwind)

```
frontend/
├── src/
│   ├── app/                    # App Router Next.js
│   │   ├── layout.tsx         # Layout principal
│   │   ├── page.tsx           # Page d'accueil
│   │   └── globals.css        # Styles globaux
│   │
│   ├── components/            # Composants React
│   │   ├── ui/               # Composants UI réutilisables
│   │   ├── features/         # Composants métier
│   │   └── layouts/          # Layouts
│   │
│   ├── lib/                  # Utilitaires
│   │   ├── api.ts           # Client API
│   │   └── utils.ts         # Fonctions utilitaires
│   │
│   └── types/               # Types TypeScript
│
├── src-tauri/               # Application desktop
│   ├── src/
│   │   └── main.rs         # Point d'entrée Rust
│   ├── Cargo.toml          # Dépendances Rust
│   └── tauri.conf.json     # Configuration Tauri
│
└── public/                 # Assets statiques
```

### Backend (FastAPI + Python)

```
backend/
├── app/
│   ├── main.py                # Point d'entrée FastAPI
│   │
│   ├── core/                  # Configuration centrale
│   │   ├── config.py         # Settings
│   │   ├── database.py       # Configuration DB
│   │   └── security.py       # Auth & sécurité
│   │
│   ├── models/               # Modèles SQLAlchemy
│   │   ├── user.py
│   │   ├── project.py
│   │   └── document.py
│   │
│   ├── schemas/              # Schémas Pydantic (à créer)
│   │   ├── user.py
│   │   ├── project.py
│   │   └── document.py
│   │
│   ├── api/                  # Routes API (à créer)
│   │   └── v1/
│   │       ├── users.py
│   │       ├── projects.py
│   │       └── documents.py
│   │
│   └── services/             # Logique métier
│       ├── ai_service.py     # Service IA
│       ├── excel_service.py  # Génération Excel
│       └── financial_service.py  # Calculs financiers
│
├── alembic/                  # Migrations
│   └── versions/
│
└── requirements.txt          # Dépendances Python
```

---

## ⚙️ Configuration de l'environnement

### 1. Variables d'environnement

#### Backend (`backend/.env`)

```env
# Base de données
DATABASE_URL=postgresql+asyncpg://refyai:refyai@localhost:5432/refyai

# Sécurité
SECRET_KEY=votre-cle-secrete-32-caracteres-minimum
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# IA
OPENAI_API_KEY=sk-votre-cle-openai
OPENAI_MODEL=gpt-4

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","tauri://localhost"]

# Upload
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=52428800
```

#### Frontend (`frontend/.env`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Installation des dépendances

```bash
# Tout installer d'un coup
./scripts/install.sh

# Ou manuellement
# Frontend
cd frontend && npm install

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🎨 Développement Frontend

### Architecture

REFY AI utilise **Next.js 14** avec l'**App Router** et **TypeScript**.

### Créer une nouvelle page

```typescript
// frontend/src/app/projects/page.tsx
export default function ProjectsPage() {
  return (
    <div>
      <h1>Mes Projets</h1>
    </div>
  );
}
```

### Créer un composant

```typescript
// frontend/src/components/ui/Button.tsx
import { cn } from "@/lib/utils";

interface ButtonProps {
  children: React.ReactNode;
  variant?: "primary" | "secondary";
  onClick?: () => void;
}

export function Button({ children, variant = "primary", onClick }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "px-4 py-2 rounded-lg font-semibold transition-colors",
        variant === "primary" && "bg-primary-600 text-white hover:bg-primary-700",
        variant === "secondary" && "bg-gray-200 text-gray-800 hover:bg-gray-300"
      )}
    >
      {children}
    </button>
  );
}
```

### Appeler l'API

```typescript
// frontend/src/lib/api.ts
import { apiClient } from "./api";

export async function getProjects() {
  const response = await apiClient.get("/api/v1/projects");
  return response.data;
}

export async function createProject(data: any) {
  const response = await apiClient.post("/api/v1/projects", data);
  return response.data;
}
```

### Utiliser dans un composant

```typescript
"use client";

import { useEffect, useState } from "react";
import { getProjects } from "@/lib/api";

export default function ProjectsList() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    getProjects().then(setProjects);
  }, []);

  return (
    <div>
      {projects.map((project) => (
        <div key={project.id}>{project.name}</div>
      ))}
    </div>
  );
}
```

---

## 🐍 Développement Backend

### Créer un nouveau endpoint

#### 1. Créer le schéma Pydantic

```python
# backend/app/schemas/project.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    
class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

#### 2. Créer la route

```python
# backend/app/api/v1/projects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models import Project
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter()

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    new_project = Project(**project.dict())
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project

@router.get("/", response_model=list[ProjectResponse])
async def list_projects(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return projects
```

#### 3. Enregistrer le router

```python
# backend/app/main.py
from app.api.v1 import projects

app.include_router(
    projects.router,
    prefix="/api/v1/projects",
    tags=["projects"]
)
```

---

## 🗄️ Base de données

### Créer une migration

```bash
cd backend

# Créer automatiquement depuis les modèles
alembic revision --autogenerate -m "Add columns to projects"

# Créer manuellement
alembic revision -m "Custom migration"
```

### Appliquer les migrations

```bash
# Appliquer toutes les migrations
alembic upgrade head

# Revenir en arrière
alembic downgrade -1

# Voir l'historique
alembic history
```

### Modifier un modèle

```python
# backend/app/models/project.py
from sqlalchemy import Column, String

# Ajouter un nouveau champ
class Project(Base):
    # ... champs existants
    new_field = Column(String, nullable=True)
```

Puis créer la migration :

```bash
alembic revision --autogenerate -m "Add new_field to projects"
alembic upgrade head
```

---

## 🤖 IA et Services

### Utiliser le service IA

```python
from app.services import ai_service

# Analyser un document
result = await ai_service.analyze_document(
    text="Contenu du PLU...",
    document_type="plu"
)

# Chat métier
response = await ai_service.chat_assistance(
    message="Comment calculer le TRI ?",
    context={"project_id": 123}
)
```

### Utiliser le service financier

```python
from app.services import financial_service

# Calcul complet
analysis = financial_service.calculate_full_analysis(
    purchase_price=300000,
    renovation_budget=50000,
    notary_fees=15000,
    loan_amount=280000,
    interest_rate=0.04,
    loan_duration=20,
    monthly_rent=1500,
    project_type="rental"
)

# Résultat contient : TRI, VAN, LTV, DSCR, etc.
print(f"TRI: {analysis['tri']:.2%}")
```

### Générer un Business Plan Excel

```python
from app.services import excel_service

# Générer l'Excel
excel_file = excel_service.generate_business_plan(
    project_data={
        "name": "Projet immobilier",
        "address": "123 rue Example",
        "project_type": "rental"
    },
    financial_data=analysis
)

# Retourner comme réponse FastAPI
from fastapi.responses import StreamingResponse

return StreamingResponse(
    excel_file,
    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    headers={"Content-Disposition": "attachment; filename=business_plan.xlsx"}
)
```

---

## 🧪 Tests

### Backend (pytest)

```python
# backend/tests/test_financial_service.py
from app.services import financial_service

def test_calculate_tri():
    tri = financial_service.calculate_tri(
        initial_investment=100000,
        cash_flows=[15000] * 10,
        periods=10
    )
    assert tri > 0

def test_calculate_ltv():
    ltv = financial_service.calculate_ltv(
        loan_amount=200000,
        property_value=250000
    )
    assert ltv == 0.8
```

Lancer les tests :

```bash
cd backend
pytest
```

### Frontend (Jest - à configurer)

```typescript
// frontend/__tests__/Button.test.tsx
import { render, screen } from '@testing-library/react';
import { Button } from '@/components/ui/Button';

test('renders button', () => {
  render(<Button>Click me</Button>);
  expect(screen.getByText('Click me')).toBeInTheDocument();
});
```

---

## ✅ Bonnes pratiques

### Code

1. **TypeScript** : Toujours typer vos variables et fonctions
2. **Composants** : Garder les composants petits et réutilisables
3. **API calls** : Centraliser dans `lib/api.ts`
4. **Validation** : Utiliser Pydantic pour valider les données
5. **Gestion d'erreurs** : Try/catch et messages clairs

### Git

```bash
# Branches
feature/nom-fonctionnalite
bugfix/nom-bug
hotfix/nom-correction-urgente

# Commits
git commit -m "feat: add project creation endpoint"
git commit -m "fix: resolve TRI calculation bug"
git commit -m "docs: update API documentation"
```

### Performance

1. **Frontend** : Utiliser `React.memo()` pour les composants lourds
2. **Backend** : Utiliser des requêtes asynchrones
3. **Cache** : Mettre en cache les résultats IA coûteux
4. **Images** : Optimiser avec Next.js Image

### Sécurité

1. **Authentification** : Toujours vérifier le token JWT
2. **Validation** : Valider toutes les entrées utilisateur
3. **CORS** : Configurer correctement les origines autorisées
4. **Secrets** : Ne jamais commiter les fichiers `.env`

---

## 🚀 Déploiement (à venir)

- **Frontend** : Vercel / Netlify
- **Backend** : Railway / Render / AWS
- **Base de données** : PostgreSQL managé
- **Desktop** : Distribution via GitHub Releases

---

Pour plus d'informations, consultez le [README principal](../README.md).
