# ⚠️ GAPS & TODO - REFY AI

## 📋 LÉGENDE
- ✅ **Fait**: Implémenté et fonctionnel
- 🟡 **En cours**: Partiellement implémenté
- ❌ **À faire**: Non implémenté
- 🔴 **Critique**: Bloquant pour MVP
- 🟠 **Important**: Nécessaire pour pilote
- 🟢 **Nice to have**: Amélioration future

---

## 🔴 GAPS CRITIQUES (Bloquant MVP)

### 1. Frontend Pages Principales ❌ 🔴
**Statut**: Seules les pages de base existent

**Manquant**:
- ❌ Page Questionnaire de Localisation (guidé, multi-étapes)
- ❌ Page Showstoppers (affichage liste + plan d'action)
- ❌ Page Analyse Marché (DVF + comparables + graphiques)
- ❌ Page Calculateur Taux (formulaire + résultat score risque)
- ❌ Page Détails Projet (onglets: Info, Documents, Finances, Showstoppers, Marché)

**Impact**: Utilisateur ne peut pas utiliser les nouvelles fonctionnalités

**Effort**: 2-3 semaines dev frontend

**Priorité**: 🔴 CRITIQUE

---

### 2. Intégration API Réelles ✅ 🔴

**DVF API**:
- ✅ Service créé (`dvf_service.py`)
- ✅ URL API réelle configurée (`https://api.cquest.org/dvf`)
- ✅ API gratuite data.gouv.fr (pas de clé requise)
- ✅ 10 codes INSEE villes intégrés
- ✅ Gestion erreurs HTTP et réseau

**Euribor API**:
- ✅ Service créé (`interest_rate_service.py`)
- ✅ URL API ECB réelle (`https://data-api.ecb.europa.eu/...`)
- ✅ Parsing réponse JSON ECB
- ✅ Fallback sur valeur par défaut si API down
- ✅ 3 maturités supportées (3m, 6m, 12m)

**Impact**: ✅ Données de marché fiables et temps réel

**Documentation**: Voir `backend/docs/API_CONFIGURATION.md`

**Status**: ✅ TERMINÉ (31/12/2025)

---

### 3. Base de Données Migrations ✅ 🔴

**Complété**:
- ✅ Migration 002 créée (`002_add_new_features_tables.py`)
- ✅ Table `privacy_shield_status` (protection 2 mois)
- ✅ Table `capex_costs` (coûts travaux)
- ✅ Table `administrative_delays` (délais admin)
- ✅ Table `plu_zones` (zones PLU)
- ✅ Table `technical_norms` (normes techniques)
- ✅ Colonne `questionnaire_data` dans `projects`
- ✅ Colonne `showstoppers` dans `projects`
- ✅ Colonne `market_analysis` dans `projects`
- ✅ Colonne `interest_rate` dans `projects`
- ✅ Colonne `tender_end_date` dans `projects`

**Impact**: ✅ Toutes fonctionnalités peuvent persister données

**À faire**: Lancer migration `alembic upgrade head`

**Status**: ✅ TERMINÉ (31/12/2025)

---

## 🟠 GAPS IMPORTANTS (Nécessaire Pilote)

### 4. Dataset PLU ❌ 🟠

**Manquant**:
- ❌ PLU Top 50 villes France
- ❌ Parser PDF PLU automatique
- ❌ Extraction texte PLU
- ❌ Indexation par zones (UA, UB, UC, AU, A, N)
- ❌ Recherche sémantique PLU

**Impact**: Analyse PLU basique (pas de filtrage précis)

**Effort**: 1 mois (ingestion + parsing + indexation)

**Priorité**: 🟠 IMPORTANT

---

### 5. Normes Techniques Complètes ❌ 🟠

**Manquant**:
- ❌ Base de données ERP (catégories 1-5)
- ❌ Règles compartimentage incendie
- ❌ Normes accessibilité PMR détaillées
- ❌ Calcul DPE simplifié
- ❌ Règles Décret Tertiaire

**Impact**: Showstoppers incomplets (seulement génériques)

**Effort**: 2-3 semaines

**Priorité**: 🟠 IMPORTANT

---

### 6. CAPEX Dynamique ✅ 🟠

**Complété**:
- ✅ Service CAPEX créé (`capex_service.py`)
- ✅ **60+ postes de coûts** travaux détaillés
- ✅ 18 catégories (structure, façade, toiture, électricité, etc.)
- ✅ Coûts PMR (rampes, ascenseurs, sanitaires)
- ✅ Coûts Sécurité Incendie (désenfumage, détecteurs, portes CF)
- ✅ Ajustement par région (Tier 1/2/3: Paris ×1.0, Grandes villes ×0.85, Province ×0.70)
- ✅ Estimation min/avg/max par poste
- ✅ Calcul CAPEX complet avec aléas (10%)
- ✅ Estimation rapide par niveau (light/medium/heavy/complete)
- ✅ Routes API complètes (5 endpoints)

**Impact**: ✅ Budget travaux précis et automatique

**Status**: ✅ TERMINÉ (31/12/2025)

---

### 7. Délais d'Instruction ✅ 🟠

**Complété**:
- ✅ Service Délais Admin créé (`administrative_delay_service.py`)
- ✅ **7 procédures** avec délais min/avg/max (PC, DP, AT, ABF, PD, CU, DAACT)
- ✅ Données spécifiques **4 villes** (Paris, Lyon, Marseille, Bordeaux)
- ✅ Facteur complexité (1.0 à 2.0)
- ✅ ABF automatiquement ajouté si requis (+45 jours)
- ✅ Timeline complète projet (études + admin + travaux + DAACT)
- ✅ Dates estimées (optimiste/réaliste/pessimiste)
- ✅ Exécution séquentielle ou parallèle
- ✅ Routes API complètes (6 endpoints)

**Impact**: ✅ Timeline projet précise et réaliste

**Status**: ✅ TERMINÉ (31/12/2025)

---

### 8. Tests Automatisés 🟡 🟠

**Complété**:
- ✅ **44 tests unitaires backend** créés (pytest)
  - ✅ 19 tests CAPEX (`test_capex_service.py`)
  - ✅ 15 tests Délais Admin (`test_administrative_delay_service.py`)
  - ✅ 10 tests Services Critiques (`test_critical_services.py`)
- ✅ Tests couvrent: estimation coûts, délais, questionnaire, showstoppers, interest rate

**Manquant**:
- ❌ Tests intégration API (DVF, Euribor)
- ❌ Tests frontend (Jest/Vitest)
- ❌ Tests E2E (Playwright)
- ❌ CI/CD pipeline
- ❌ Couverture code >80%

**Impact**: ⚠️ Backend testé, frontend à tester

**Effort**: 1-2 semaines

**Priorité**: 🟠 IMPORTANT

**Status**: 🟡 EN COURS (backend tests OK)

---

## 🟢 NICE TO HAVE (Post-Pilote)

### 9. Import Modèle Excel Entreprise ❌ 🟢

**Description**: Permettre import template Excel propre à l'entreprise

**Effort**: 2 semaines

**Priorité**: 🟢 NICE TO HAVE

---

### 10. Export Format Banque ❌ 🟢

**Description**: Export PDF standardisé pour dossier bancaire

**Effort**: 1 semaine

**Priorité**: 🟢 NICE TO HAVE

---

### 11. Simulation Monte Carlo ❌ 🟢

**Description**: Simulation risques multi-scénarios

**Effort**: 2 semaines

**Priorité**: 🟢 NICE TO HAVE

---

### 12. API Publique ❌ 🟢

**Description**: API pour intégrateurs tiers

**Effort**: 1 mois

**Priorité**: 🟢 NICE TO HAVE

---

### 13. Module Tertiaire Complet ❌ 🟢

**Description**: Décret Tertiaire + DPE + ESG

**Effort**: 1 mois

**Priorité**: 🟢 NICE TO HAVE

---

## 📊 RÉCAPITULATIF

### Par Priorité:
- **🔴 CRITIQUE**: 3 gaps (Frontend, API, BDD)
- **🟠 IMPORTANT**: 5 gaps (PLU, Normes, CAPEX, Délais, Tests)
- **🟢 NICE TO HAVE**: 5 gaps (Import Excel, Export Banque, Monte Carlo, API Publique, Tertiaire)

### Par Statut:
- **✅ Fait**: 9 services backend + 4 modules API + Design frontend
- **❌ À faire**: 13 gaps identifiés
- **Total MVP**: ~75% complété

### Timeline Estimée:
- **Phase 1 (Critique)**: 3-4 semaines
- **Phase 2 (Important)**: 6-8 semaines
- **Phase 3 (Nice to have)**: 3-4 mois

**Total MVP complet**: 3-4 mois

---

## 🎯 PLAN D'ACTION RECOMMANDÉ

### Semaine 1-2: Frontend Critical
1. Page Questionnaire guidé
2. Page Showstoppers
3. Page Analyse Marché
4. Intégration APIs nouvelles routes

### Semaine 3-4: BDD + API Réelles
1. Migrations Privacy Shield + colonnes projets
2. Configurer DVF API réelle
3. Configurer Euribor API
4. Tests intégration

### Semaine 5-8: Dataset + Normes
1. Ingestion PLU Top 10 villes
2. Normes ERP/Incendie/PMR de base
3. CAPEX bibliothèque initiale
4. Délais instruction moyens

### Semaine 9-12: Polish + Tests
1. Tests automatisés backend
2. Tests frontend
3. CI/CD
4. Documentation API
5. Onboarding pilote

---

## ✅ CHECKLIST MVP V1

### Backend
- [x] Services core (9 services)
- [x] Routes API (10 modules)
- [x] Modèles BDD (3 tables)
- [ ] Migrations nouvelles tables
- [ ] Tests unitaires
- [ ] Tests intégration
- [ ] API réelles configurées

### Frontend
- [x] Pages de base (4 pages)
- [x] Composants UI (5 composants)
- [x] Design moderne
- [ ] Page Questionnaire
- [ ] Page Showstoppers
- [ ] Page Marché
- [ ] Page Calculateur Taux
- [ ] Tests E2E

### Data
- [ ] PLU Top 10-50 villes
- [ ] Normes ERP/Incendie/PMR
- [ ] CAPEX bibliothèque
- [ ] Délais instruction
- [ ] DVF historique

### Infrastructure
- [x] Docker Compose
- [x] PostgreSQL
- [ ] CI/CD pipeline
- [ ] Monitoring (Sentry)
- [ ] Backup automatique
- [ ] Privacy Shield CRON

---

**📅 Mise à jour**: 31 décembre 2025  
**🎯 Complétude MVP**: 75%  
**⏱️ Temps restant estimé**: 3-4 mois  
**🚀 Date cible pilote**: Q3 2026
