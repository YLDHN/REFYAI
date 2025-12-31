# 📊 BUSINESS PLAN REFY AI - Implémentation Technique

## 🎯 RÉSUMÉ EXÉCUTIF

REFY AI est un Agent IA révolutionnaire qui automatise la **due diligence technique et administrative** des professionnels de l'immobilier (Fonds Value-Add, Fonds de Dette, Promoteurs, MDB).

**Mission**: Supprimer le goulot d'étranglement administratif lié au Permis de Construire.

**Transformation**: Dossier brut (IM) → **Stratégie d'investissement complète** + **Business Plan dynamique** en **< 1 heure**.

---

## 🔍 ANALYSE DU PROBLÈME

### Le Goulot d'Étranglement Manuel

**Chiffres clés**:
- PLU: Jusqu'à **3 000 pages** par commune
- Analyse humaine: **5-10 jours** + coûteuse + sujette à erreur
- **Deals ratés**: Projets rentables abandonnés (mal chiffrés)
- **Risques de conformité**: Sous-estimation normes (ERP, incendie, PMR) = budgets explosés

---

## 💡 LA SOLUTION REFY AI

### A. Stratégie de Données (Dataset)

#### 1. **Urbanisme**
- ✅ Ingestion PLU France
- ✅ Code de l'Urbanisme
- ✅ **Questionnaire de Localisation** (12 questions ciblées)
  - Filtrage précis PLU
  - Détection ABF/Monuments Historiques
  - Identification zone, COS, CES

#### 2. **Technique**
- ✅ Normes ERP
- ✅ Sécurité incendie + compartimentage
- ✅ DPE (Diagnostic Performance Énergétique)
- ✅ Décret Tertiaire
- ✅ Accessibilité PMR

#### 3. **Marché**
- ✅ **DVF (Demandes de Valeurs Foncières)** - API data.gouv.fr
- ✅ Transactions comparables temps réel
- ✅ Analyse tendances marché
- ✅ Évolution prix 12 mois

#### 4. **Financier**
- ✅ Bibliothèques CAPEX construction
- ✅ Ratios construction par type de bien
- ✅ **Algorithme taux d'intérêt** (Euribor + marge risque)

---

### B. Fonctionnalités Clés

#### 🔹 **1. Questionnaire de Localisation**
**Implémenté**: ✅ `location_questionnaire_service.py`

Filtrage précis du PLU pour une **analyse garantie sans erreur**.

**12 Questions**:
- Commune, adresse, parcelle cadastrale
- Zone PLU, surface terrain/construite
- Hauteur, niveaux
- Monuments Historiques / ABF
- Nature travaux (extension, surélévation, changement destination)
- Destination finale (habitation, bureaux, commerce, hôtel)

**Output**: Filtres PLU optimisés avec mots-clés ciblés.

**Gain**: **500-3000 pages PLU** → **30-60 secondes** d'analyse ciblée.

---

#### 🔹 **2. Audit Technique & Showstoppers**
**Implémenté**: ✅ `showstopper_service.py`

Identification **immédiate des points bloquants**.

**4 Catégories**:
- **Réglementaire**: Zone non constructible, COS dépassé, ABF
- **Technique**: Structure dangereuse, amiante, non-conformité incendie/PMR
- **Financier**: TRI < 5%, LTV > 85%
- **Juridique**: Servitudes, copropriété conflictuelle

**4 Niveaux de Sévérité**:
- CRITICAL: Bloquant absolu
- HIGH: Très risqué
- MEDIUM: À surveiller
- LOW: Impact limité

**Output**:
- Liste showstoppers avec recommandations
- Estimation délais et coûts
- **Plan d'action priorisé**
- Timeline globale

**Exemple Showstopper CRITICAL**:
```
Zone non constructible (Zone A/N)
→ Impact: Projet impossible sans dérogation
→ Délai: 6-24 mois
→ Coût: 10 000 - 50 000 €
```

---

#### 🔹 **3. Analyse Marché (DVF)**
**Implémenté**: ✅ `dvf_service.py`

Données officielles **data.gouv.fr** pour valeur de marché.

**Fonctionnalités**:
- **Ventes comparables** (derniers 24 mois)
- **Prix médian/moyen au m²**
- **Estimation basse/haute** (P25/P75)
- **Tendance marché**: Hausse, Baisse, Stable
- **Évolution 12 mois** (%)

**Stratégie Exit Automatique**:
- **Marché haussier + bon prix** → Revente court terme (18-36 mois)
- **Marché baissier** → Location longue (5-10 ans)
- **Marché stable** → Mixte selon opportunités

**Output**:
```json
{
  "prix_median_m2": 5200,
  "estimation_mediane": 520000,
  "trend": "hausse",
  "evolution_12m": +8.5%,
  "strategie_recommandee": "revente_court_terme"
}
```

---

#### 🔹 **4. Générateur Business Plan Excel**
**Implémenté**: ✅ `excel_service.py`

Création matrice **dynamique avec formules vivantes**.

**5 Onglets**:
1. **Synthèse**: KPIs clés (TRI, VAN, LTV, DSCR)
2. **Hypothèses**: Inputs modifiables
3. **Plan de financement**: Dette/Equity
4. **Compte de résultat**: Prévisionnel 10-20 ans
5. **Indicateurs**: Ratios et sensibilité

**Personnalisation**: REFY permet d'**incorporer le modèle Excel propre** à l'entreprise pour garantir clarté stratégie corporate.

---

## 📈 MODÈLE FINANCIER & LOGIQUE

### A. Hypothèses et Algorithmes

#### 🔹 **Structure de Financement**
- ✅ Paramétrage **LTV** (Loan-to-Value): 65-85%
- ✅ Paramétrage **LTC** (Loan-to-Cost): 70-90%

#### 🔹 **Algorithme de Risque (Taux d'Intérêt)**
**Implémenté**: ✅ `interest_rate_service.py`

**Taux ≠ figé**. REFY le calcule via algorithme de risque.

**Formule**: `Taux Final = Euribor + Marge Risque`

**7 Facteurs de Risque** (Score 0-100):
1. **Géographie**: Tier 1 (Paris, Lyon...) = -0 pts | Tier 2-3 = -8 pts
2. **LTV**: > 80% = Pénalité -20 pts
3. **TRI**: < 10% = Pénalité -15 pts
4. **Showstoppers**: Chaque showstopper = -3 pts
5. **Expérience entreprise**: Novice = -15 pts | Expert = -0 pts
6. **Marché**: Baisse = -10 pts | Stable = -5 pts | Hausse = -0 pts
7. **Technique**: Chaque problème majeur = -5 pts

**Catégories**:
- **Excellent** (Score ≥ 85): Marge +0.8%
- **Bon** (70-84): Marge +1.2%
- **Moyen** (50-69): Marge +1.8%
- **Risque** (< 50): Marge +2.5%

**Ajustements**:
- TRI > 15%: Bonus -0.20%
- LTV > 80%: Pénalité +0.30%
- Client existant: Bonus -0.15%
- Garanties supplémentaires: Bonus -0.25%

**Exemple**:
```
Euribor 12M: 3.45%
Score Risque: 72 (Bon)
Marge Base: +1.2%
Ajustements: -0.15% (fidélité)
→ Taux Final: 4.50%
```

---

#### 🔹 **CAPEX & Délais**
- ✅ Chiffrage basé sur **audit technique**
- ✅ Optimisation **délais d'instruction administrative**
- ❌ TODO: CAPEX dynamique selon showstoppers

#### 🔹 **Exit Métrique**
- ✅ Calcul valeur revente (data **DVF**)
- ✅ Offre comparable temps réel
- ✅ Stratégie **locatif vs revente**

---

### B. KPIs et Performance

#### 🔹 **Optimisation TRI**
La vitesse d'analyse réduit le temps **acquisition → travaux**, boostant mécaniquement le rendement.

**Avant REFY**: 10-15 jours analyse → Retard projet
**Avec REFY**: < 1 heure → **Lancement immédiat** → +0.5-1% TRI

#### 🔹 **Détermination Stratégie**
L'IA aide à choisir entre:
- **Stratégie locative**: Revenus récurrents
- **Revente directe**: Plus-value rapide
- **Mixte**: Selon opportunités marché

---

## 🏢 FOCUS TERTIAIRE & ENVIRONNEMENTAL

**Phase 2** (après résidentiel):

### Audit Tertiaire
- ✅ Conformité **Décret Tertiaire**
- ✅ Normes **ESG / RSE**
- ✅ Certification HQE, BREEAM

### Évaluation DPE
- ✅ Calcul investissements énergétiques nécessaires
- ✅ Impact sur **valeur vénale**
- ✅ Aides CEE, MaPrimeRénov'

---

## 💼 BUSINESS MODEL

### A. SaaS B2B
**Abonnement récurrent** pour professionnels:
- **Starter**: 200€/mois (5 projets/mois)
- **Pro**: 800€/mois (20 projets/mois)
- **Enterprise**: Sur-mesure (illimité)

### B. Privacy Shield (Règle des 2 Mois)
**Implémenté**: ✅ `privacy_shield_service.py`

**Protection secret des affaires**:

Les données des **opérations en cours** sont **isolées sur serveurs étanches**. L'IA n'incorpore ces données au modèle global qu'**après 2 mois** suivant fin d'appel d'offres.

**Mécanismes**:
1. Enregistrement projet sous Privacy Shield
2. Date fin appel d'offres + 60 jours = Release Date
3. Anonymisation automatique (adresse, prix, nom)
4. Libération CRON après délai
5. Agrégation données publiques uniquement

**Garantie**: Aucun concurrent ne peut voir vos données avant 2 mois post-tender.

---

## 🗓️ ROADMAP & ÉQUIPE

### Timeline
- **Été 2026**: Sortie **V1** (Assistant Admin + BP Excel complet)
- **Sept 2026 - Juin 2027**: Phase **pilote 6 mois gratuits** avec partenaires stratégiques (Fonds PE et Dette)

### Équipe
- **Équipe jeune** + **advisors stratégiques**
- **Pierre Soria** (ex-Salesforce): Scale B2B

---

## 🎯 AVANTAGES COMPÉTITIFS

### vs Bureaux d'études traditionnels:
| Critère | Bureau Étude | REFY AI |
|---------|-------------|---------|
| Délai | 5-10 jours | < 1 heure |
| Coût | 3 000-8 000€ | 50-200€/mois |
| Showstoppers | Tardifs | Immédiats |
| DVF | Manuel | Automatique |
| Taux Intérêt | Estimation | Algorithme précis |
| Privacy | Variable | Garantie 2 mois |

### Innovations Uniques:
1. **Questionnaire Guidé** → Zéro erreur PLU
2. **Showstoppers Detection** → Early warning
3. **DVF + IA** → Exit strategy data-driven
4. **Algorithme Taux** → Financement réaliste
5. **Privacy Shield** → Secret affaires protégé
6. **BP Excel Dynamique** → Formules exploitables

---

## 📊 MÉTRIQUES SUCCÈS

### Gains Client:
- **Temps**: 10 jours → 1 heure = **-95%**
- **Coût**: 5 000€ → 200€/mois = **-98%**
- **Deals sauvés**: +30% (showstoppers early)
- **TRI optimisé**: +1-2% (meilleure négociation)

### KPIs Technique:
- Analyse PLU: < 60 sec ✅
- Précision showstoppers: > 95%
- Erreur DVF: < 10%
- Disponibilité: > 99%

---

## 🚀 PROCHAINES ÉTAPES

### Phase 1 (Q1 2026): MVP
- ✅ Questionnaire frontend
- ✅ Showstoppers frontend
- ✅ Analyse Marché frontend
- ✅ DVF API réelle
- ✅ Tests flux complet

### Phase 2 (Q2 2026): Dataset
- Intégrer PLU Top 50 villes
- Normes ERP/Incendie/PMR complètes
- Bibliothèque CAPEX
- DVF historique complet

### Phase 3 (Q3 2026): Pilote
- Onboarding 3-5 fonds partenaires
- Feedback terrain
- Amélioration IA
- Privacy Shield production

### Phase 4 (2027): Scale
- SaaS B2B packagé
- Intégration bancaire
- API publique
- Module tertiaire (DPE + Décret)

---

**📅 Document**: 31 décembre 2025  
**🎯 Statut**: MVP V1 Core + 5 modules avancés implémentés  
**🚀 Objectif**: Pilote client Q3 2026 (6 mois gratuits)

---

## 📧 CONTACT

**Email**: contact@refy.ai  
**Website**: www.refy.ai  
**LinkedIn**: linkedin.com/company/refy-ai

**Pour pilote 2026**: Rejoignez-nous comme partenaire stratégique et bénéficiez de 6 mois gratuits !
