# 🧪 PLAN DE TEST BACKEND - REFY AI V5

## Objectif

Valider **TOUTES les fonctionnalités métier** du backend REFY avant d'intégrer l'IA OpenAI.

**RÈGLE D'OR**: Tant que ces tests ne sont pas tous au vert, **aucune clé OpenAI ne doit être ajoutée**.

---

## Structure des tests

### 📋 8 Sections de tests

| Section | Thème | Fichier | Tests |
|---------|-------|---------|-------|
| **1** | Logique métier pure | `test_01_business_logic.py` | Score technique, Frais notaire, Risque fiscal MDB, LTV/LTC |
| **2** | Moteur de phasage | `test_02_timeline_engine.py` | 3 phases, CAPEX phase travaux, Revenus post-travaux |
| **3** | Waterfall/Promote | `test_03_waterfall_promote.py` | Distribution investisseur/sponsor, Hurdle rate, Promote |
| **4** | Conformité documentaire | `test_04_document_compliance.py` | Checklist dynamique, Documents manquants |
| **5** | IA (mocks) | `test_05_ai_predictions_mock.py` | Suggestions CAPEX sans API réelle |
| **6** | API bout en bout | `test_06_api_end_to_end.py` | Parcours utilisateur complet |
| **7** | Exports | `test_07_exports_excel_pdf.py` | Excel avec formules, PDF dossier banque |
| **8** | Confidentialité | `test_08_privacy_shield.py` | Privacy Shield, Règle 2 mois, Cloisonnement |

---

## 🚀 Lancer les tests

### Option 1: Suite complète (recommandé)
```bash
cd backend
source venv/bin/activate
python tests/run_all_tests.py
```

### Option 2: Section individuelle
```bash
pytest tests/test_01_business_logic.py -v
pytest tests/test_02_timeline_engine.py -v
# etc.
```

### Option 3: Test spécifique
```bash
pytest tests/test_01_business_logic.py::TestScoreTechnique::test_score_parfait_sans_penalites -v
```

---

## 📊 Interprétation des résultats

### ✅ Tous verts
Le backend est **prêt pour l'intégration IA**.
Vous pouvez ajouter votre clé OpenAI.

### ⚠️ Certains tests en échec
**NE PAS intégrer l'IA avant correction.**
Chaque test en échec représente une fonctionnalité métier cassée.

### 🔴 Beaucoup d'échecs
Le backend nécessite des corrections importantes.
Prioriser les sections 1-4 (logique métier pure).

---

## 🎯 Priorités de correction

1. **Section 1-2** : Logique métier + Timeline (CRITIQUE)
2. **Section 3** : Waterfall/Promote (fonds d'investissement)
3. **Section 4** : Documents (compliance réglementaire)
4. **Section 6** : API (expérience utilisateur)
5. **Section 7-8** : Exports + Privacy (finition)

---

## 📝 Critères de validation

### Pour chaque section

- ✅ Tous les tests passent
- ✅ Pas de `pytest.skip()`
- ✅ Pas de `# TODO` dans le code testé
- ✅ Couverture > 80%

### Globalement

- ✅ Aucune dépendance à OpenAI dans les tests 1-4
- ✅ Mocks corrects dans la section 5
- ✅ Pas d'appel réseau dans les tests unitaires
- ✅ Résultats déterministes (même input = même output)

---

## 🔧 Dépendances

```bash
pip install pytest pytest-asyncio pytest-cov openpyxl
```

---

## 📖 Documentation détaillée

Chaque fichier de test contient:
- Description de ce qui est testé
- Pourquoi c'est important
- Cas limites couverts
- Exemples de données

---

## 🎓 Philosophie

Ces tests ne sont pas juste une formalité.
Ils constituent:

1. **Une preuve technique** pour les investisseurs
2. **Une documentation vivante** du comportement attendu
3. **Un filet de sécurité** lors des évolutions futures
4. **Un contrat** entre le métier et la tech

---

## ⚡ Quick Start

```bash
# Installation
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Lancer TOUS les tests
python tests/run_all_tests.py

# Si tout est vert ✅
echo "OPENAI_API_KEY=sk-..." >> .env

# Sinon ❌
# Corriger les tests en échec avant de continuer
```

---

## 🆘 Support

Si des tests échouent et que vous ne comprenez pas pourquoi:

1. Lire le message d'erreur complet
2. Vérifier que les services testés sont implémentés
3. Vérifier la base de données (migrations)
4. Consulter la documentation de chaque section

**Ces tests sont votre meilleur allié pour un backend robuste.**

---

*Dernière mise à jour: 5 janvier 2026*
