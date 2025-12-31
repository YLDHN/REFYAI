# REFY AI

<div align="center">

**L'Agent IA Administratif & Technique au service de la Performance Immobilière**

Automatisation de la due diligence technique et administrative pour professionnels de l'immobilier

[🚀 Démarrage rapide](#démarrage-rapide) • [📖 Documentation](#documentation) • [💡 Fonctionnalités](#fonctionnalités) • [🎯 Business Plan](#business-plan)

</div>

---

## 📋 Table des matières

- [À propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
- [Nouveautés 2025](#nouveautés-2025)
- [Stack technique](#stack-technique)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Démarrage rapide](#démarrage-rapide)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Business Plan](#business-plan)
- [Roadmap](#roadmap)

---

## 🎯 À propos

**REFY AI** est un Agent IA révolutionnaire conçu pour **automatiser la due diligence technique et administrative** des professionnels de l'immobilier (Fonds Value-Add, Fonds de Dette, Promoteurs, MDB).

### Mission

Supprimer le **goulot d'étranglement administratif** lié à l'obtention du Permis de Construire.

### Transformation

**Dossier brut (IM)** → **Stratégie d'investissement complète** + **Business Plan dynamique** en **< 1 heure**.

### Valeur Ajoutée

- ⏱️ **Temps**: 10 jours → 1 heure (**-95%**)
- 💰 **Coût**: 5 000€ → 200€/mois (**-98%**)
- 📈 **Deals sauvés**: +30% (détection early des showstoppers)
- 💎 **TRI optimisé**: +1-2% (meilleure négociation prix)

---

## ✨ Fonctionnalités

### 🏠 Core Features

- ✅ **Analyse réglementaire** : PLU, urbanisme, contraintes légales
- ✅ **Analyse technique** : Normes ERP, incendie, PMR, DPE
- ✅ **Analyse financière** : CAPEX, TRI, VAN, LTV, LTC, DSCR
- ✅ **Génération Business Plan Excel** : Formules dynamiques exploitables
- ✅ **Chat IA métier** : Assistant expert immobilier

### 🆕 Nouveautés 2025

#### 📝 **1. Questionnaire de Localisation**
Filtrage précis du PLU via 12 questions ciblées :
- Commune, adresse, parcelle cadastrale
- Zone PLU, surface, hauteur
- ABF / Monuments Historiques
- Nature travaux (extension, changement destination...)
- **Gain**: 3 000 pages PLU → 60 secondes d'analyse

#### 🚨 **2. Détection Showstoppers**
Identification automatique des points bloquants :
- **4 catégories**: Réglementaire, Technique, Financier, Juridique
- **4 sévérités**: CRITICAL, HIGH, MEDIUM, LOW
- Recommandations + Délais + Coûts
- **Plan d'action priorisé**

Exemples:
- Zone non constructible (CRITICAL)
- Amiante/Plomb détecté (HIGH)
- LTV > 85% (MEDIUM)

#### 📊 **3. Analyse Marché (DVF)**
Données officielles data.gouv.fr :
- **Ventes comparables** derniers 24 mois
- **Prix médian/moyen au m²**
- **Tendance marché**: Hausse, Baisse, Stable
- **Stratégie Exit automatique**: Locatif vs Revente

#### 💰 **4. Algorithme Taux d'Intérêt**
Calcul personnalisé : **Euribor + Marge Risque**
- **Score de risque** (0-100) sur 7 facteurs
- **Marge adaptative**: 0.8% à 2.5%
- **Optimisation structure** Dette/Equity
- **Taux réaliste** pour financement bancaire

#### 🔒 **5. Privacy Shield (Règle des 2 mois)**
Protection du secret des affaires :
- Isolation données projets en cours
- Anonymisation automatique
- Libération après 2 mois post-tender
- Aucun concurrent ne voit vos données

---

## 🎨 Design

Interface moderne professionnelle :
- **Sidebar dark** avec navigation intuitive
- **Dashboard** avec KPIs et projets récents
- **Grille projets** avec filtres et badges
- **Design system** cohérent (Bleu, Vert, Violet, Orange)

---

## 🛠️ Stack technique

### Frontend
- **Framework** : Next.js 14 (App Router)
- **UI** : React 18 + TypeScript
- **Styling** : Tailwind CSS 3
- **Desktop** : Tauri 2.0
- **State** : React Hooks
- **HTTP** : Axios

### Backend
- **Framework** : FastAPI
- **Langage** : Python 3.14
- **ORM** : SQLAlchemy 2.0 (Async)
- **Database** : PostgreSQL
- **Migrations** : Alembic
- **Auth** : JWT (python-jose)
- **IA** : OpenAI API (GPT-4)

### Services IA & Business
- **Questionnaire** : location_questionnaire_service.py
- **Showstoppers** : showstopper_service.py
- **DVF Marché** : dvf_service.py
- **Taux Intérêt** : interest_rate_service.py
- **Privacy Shield** : privacy_shield_service.py
- **Financier** : financial_service.py
- **Excel** : excel_service.py
- **IA Analyse** : ai_service.py

### Infrastructure
- **Containerisation** : Docker + Docker Compose
- **Reverse Proxy** : Nginx (production)
- **CI/CD** : GitHub Actions (à venir)

---

### Frontend
- **Next.js 14** : Framework React avec App Router
- **TypeScript** : Typage statique
- **Tailwind CSS** : Styling moderne et responsive
- **Tauri 2** : Application desktop multi-plateforme

### Backend
- **Python 3.12** : Langage principal
- **FastAPI** : Framework API moderne et performant
- **SQLAlchemy** : ORM pour PostgreSQL
- **Alembic** : Migrations de base de données

### Base de données
- **PostgreSQL** : Base de données principale
- **ChromaDB** : Base vectorielle pour l'IA

### IA & Documents
- **OpenAI GPT-4** : Analyse de documents et chat
- **LangChain** : Orchestration IA
- **PyPDF2** : Extraction PDF
- **OpenPyXL/XlsxWriter** : Génération Excel

### DevOps
- **Docker & Docker Compose** : Containerisation
- **Git** : Versioning

---

## 📦 Prérequis

### Pour le développement web

- **Node.js** : v20+ ([Télécharger](https://nodejs.org/))
- **Python** : 3.12+ ([Télécharger](https://www.python.org/))
- **PostgreSQL** : 16+ ([Télécharger](https://www.postgresql.org/))
- **Docker Desktop** : Dernière version ([Télécharger](https://www.docker.com/products/docker-desktop/))

### Pour l'application desktop (en plus)

- **Rust** : Dernière version stable ([Installer](https://rustup.rs/))
- **Dépendances système** :
  - **macOS** : Xcode Command Line Tools
  - **Windows** : Visual Studio 2022 Build Tools
  - **Linux** : `libwebkit2gtk-4.1-dev`, `build-essential`, `curl`, etc.

---

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone <votre-repo>
cd REFYAI
```

### 2. Installation automatique

```bash
./scripts/install.sh
```

Cette commande installe :
- Les dépendances frontend (Node.js)
- Les dépendances backend (Python)
- L'environnement virtuel Python

### 3. Configuration

#### Backend

```bash
cp backend/.env.example backend/.env
```

Éditez `backend/.env` et ajoutez votre clé OpenAI :

```env
OPENAI_API_KEY=sk-votre-cle-openai
```

#### Frontend

```bash
cp frontend/.env.example frontend/.env
```

---

## 🎬 Démarrage rapide

### Avec Docker (Recommandé)

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

Services disponibles :
- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **API Docs** : http://localhost:8000/docs
- **PostgreSQL** : localhost:5432

### Sans Docker (Développement)

#### Terminal 1 : Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Terminal 2 : Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Terminal 3 : PostgreSQL

```bash
# Avec Docker uniquement pour PostgreSQL
docker-compose up -d postgres
```

### Initialiser la base de données

```bash
./scripts/init-db.sh
```

---

## 🖥️ Application Desktop

### Mode développement

```bash
./scripts/dev-desktop.sh
```

### Build de production

```bash
./scripts/build-desktop.sh
```

L'application compilée se trouve dans `frontend/src-tauri/target/release/`

---

## 🏗️ Architecture

```
REFYAI/
├── frontend/                 # Application Next.js
│   ├── src/
│   │   ├── app/             # Pages et layouts (App Router)
│   │   ├── components/      # Composants React
│   │   └── lib/             # Utilitaires et API client
│   ├── src-tauri/           # Application Tauri (desktop)
│   └── public/              # Assets statiques
│
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── main.py         # Point d'entrée
│   │   ├── core/           # Configuration, DB, sécurité
│   │   ├── models/         # Modèles SQLAlchemy
│   │   ├── services/       # Logique métier (IA, Excel, Finance)
│   │   └── api/            # Routes API
│   ├── alembic/            # Migrations de base de données
│   └── requirements.txt    # Dépendances Python
│
├── docs/                    # Documentation
│   ├── BUSINESS PLAN.pdf
│   └── maquette.pdf
│
├── scripts/                 # Scripts d'automatisation
│   ├── install.sh
│   ├── start.sh
│   ├── init-db.sh
│   ├── build-desktop.sh
│   └── dev-desktop.sh
│
└── docker-compose.yml       # Configuration Docker
```

### Flux de données

```
[Utilisateur] 
    ↓
[Frontend Next.js / Tauri]
    ↓ HTTP/REST
[Backend FastAPI]
    ↓
[Services métier]
    ├── IA Service (OpenAI)
    ├── Excel Service (XlsxWriter)
    └── Financial Service (Calculs)
    ↓
[PostgreSQL / ChromaDB]
```

---

## 📖 Documentation

### Documentation API

Une fois le backend lancé, accédez à :

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### Documents du projet

- [Business Plan](docs/BUSINESS%20PLAN.pdf) : Présentation complète du projet
- [Maquette](docs/maquette.pdf) : Design et wireframes

### Guides de développement

#### Créer un nouveau modèle

1. Créer le modèle dans `backend/app/models/`
2. Créer une migration : `alembic revision --autogenerate -m "Description"`
3. Appliquer : `alembic upgrade head`

#### Ajouter une route API

1. Créer le fichier dans `backend/app/api/v1/`
2. Importer dans `backend/app/main.py`

#### Créer un composant frontend

```bash
cd frontend/src/components
# Créer votre composant TypeScript
```

---

## 🔧 Développement

### Commandes utiles

#### Backend

```bash
# Lancer le serveur
uvicorn app.main:app --reload

# Créer une migration
alembic revision --autogenerate -m "Description"

# Appliquer les migrations
alembic upgrade head

# Tests (à venir)
pytest
```

#### Frontend

```bash
# Mode développement
npm run dev

# Build production
npm run build

# Lancer Tauri
npm run tauri dev

# Build Tauri
npm run tauri build

# Lint
npm run lint
```

#### Docker

```bash
# Rebuild les images
docker-compose build

# Voir les logs d'un service
docker-compose logs -f backend

# Redémarrer un service
docker-compose restart backend

# Shell dans un container
docker-compose exec backend bash
```

### Variables d'environnement

#### Backend (.env)

```env
DATABASE_URL=postgresql+asyncpg://refyai:refyai@localhost:5432/refyai
SECRET_KEY=votre-cle-secrete
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
```

#### Frontend (.env)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🧪 Tests (À venir)

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

---

## 📝 Roadmap

### Version 0.1 (MVP) - Actuelle
- [x] Architecture complète
- [x] Frontend Next.js + Tailwind
## 🗓️ Roadmap

### ✅ V0.1 - Core MVP (Décembre 2025)
- [x] Frontend Next.js + Design moderne
- [x] Backend FastAPI + 9 services métier
- [x] Questionnaire de Localisation
- [x] Détection Showstoppers
- [x] Intégration DVF (Marché)
- [x] Algorithme Taux d'Intérêt
- [x] Privacy Shield
- [x] Calculs financiers (TRI, VAN, LTV, LTC, DSCR)
- [x] Génération Excel BP

### 🚧 V0.2 - Frontend Complet (Q1 2026)
- [ ] Pages Questionnaire guidé
- [ ] Pages Showstoppers + plan d'action
- [ ] Pages Analyse Marché (graphiques DVF)
- [ ] Pages Calculateur Taux
- [ ] Page Détails Projet (onglets)
- [ ] Tests E2E (Playwright)

### 📊 V0.3 - Dataset & Normes (Q2 2026)
- [ ] PLU Top 50 villes France
- [ ] Normes ERP complètes
- [ ] Normes Incendie + compartimentage
- [ ] Normes PMR détaillées
- [ ] CAPEX dynamique
- [ ] Délais d'instruction administrative

### 🚀 V1.0 - Pilote Client (Q3 2026)
- [ ] Onboarding 3-5 fonds partenaires
- [ ] 6 mois gratuits (selon Business Plan)
- [ ] Feedback terrain
- [ ] Amélioration IA cas réels
- [ ] Privacy Shield production
- [ ] API publique documentée

### 🏢 V2.0 - Module Tertiaire (2027)
- [ ] Décret Tertiaire
- [ ] DPE avancé
- [ ] Normes ESG/RSE
- [ ] Certification HQE, BREEAM
- [ ] Bureaux & Commerces

---

## 💼 Business Plan

**Cible**: Fonds Value-Add, Fonds de Dette, Promoteurs, Marchands de Biens

**Modèle**: SaaS B2B par abonnement
- **Starter**: 200€/mois (5 projets/mois)
- **Pro**: 800€/mois (20 projets/mois)
- **Enterprise**: Sur-mesure (illimité)

**Avantages vs Bureau d'étude**:
| Critère | Bureau Étude | REFY AI |
|---------|--------------|---------|
| Délai | 5-10 jours | < 1 heure |
| Coût | 3 000-8 000€ | 50-200€/mois |
| Erreurs PLU | Fréquentes | Zéro (filtrage guidé) |
| Showstoppers | Tardifs | Immédiats |
| DVF | Manuel | Automatique |
| Taux bancaire | Estimation | Algorithme précis |

**Gains Client**:
- ⏱️ Temps: **-95%** (10 jours → 1h)
- 💰 Coût: **-98%** (5 000€ → 200€/mois)
- 📈 Deals sauvés: **+30%** (showstoppers early)
- 💎 TRI optimisé: **+1-2%** (meilleure négociation)

**Timeline**:
- **Été 2026**: Sortie V1.0
- **Sept 2026 - Juin 2027**: Pilote gratuit 6 mois
- **2027**: Commercialisation SaaS B2B

**Équipe**:
- Équipe dev + Advisors stratégiques
- Pierre Soria (ex-Salesforce): Scale B2B

**Documentation complète**:
- 📊 [Business Plan Technique](docs/BUSINESS_PLAN_TECHNIQUE.md)
- 📋 [Audit Complet](docs/AUDIT_COMPLET.md)
- ⚠️ [Gaps & TODO](docs/GAPS_TODO.md)

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📄 Licence

Ce projet est sous licence propriétaire. Tous droits réservés.

---

## 👥 Équipe

**REFY AI Team**
- **Advisors**: Pierre Soria (ex-Salesforce)

---

## 📞 Support & Contact

**Pilote 2026**: Rejoignez-nous comme partenaire stratégique (6 mois gratuits) !

- **Email** : contact@refy.ai
- **Website** : www.refy.ai
- **LinkedIn** : linkedin.com/company/refy-ai
- **Documentation** : [docs/](docs/)

---

<div align="center">

**Fait avec ❤️ par l'équipe REFY AI**

*Automatiser la due diligence immobilière - Une analyse à la fois*

</div>

</div>
