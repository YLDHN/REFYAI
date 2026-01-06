# Guide d'implémentation des méthodes manquantes

## État actuel

Les tests révèlent que **toutes les méthodes métier doivent être implémentées** selon les signatures attendues par les tests.

## Méthodes à implémenter (par priorité)

### Section 1: financial_service (CRITIQUE)

```python
# Signature correcte basée sur test_01
def calculate_technical_score(
    has_construction_permit: bool,
    has_environmental_studies: bool,
    has_soil_study: bool,
    has_abf_clearance: bool,
    has_urban_planning_certificate: bool,
    structural_issues: bool,
    pollution_detected: bool,
    protected_area: bool
) -> Dict[str, Any]:
    """Retourne: {"score": int, "grade": str, "penalties": list}"""
    
def calculate_notary_fees(
    purchase_price: float,
    buyer_profile: str  # "particulier", "mdb"
) -> Dict[str, Any]:
    """Retourne: {"amount": float, "rate_pct": float, "buyer_profile": str}"""
    
def check_mdb_tax_risk(
    is_mdb: bool,
    holding_duration_years: float
) -> Dict[str, Any]:
    """Retourne: {"has_risk": bool, "message": str}"""
    
def calculate_debt_from_ltv/ltc(...)
def generate_project_timeline(...)
def calculate_waterfall(...)
```

### Section 4: document_service

```python
def get_required_documents(asset_type: str) -> List[str]
def get_missing_documents(project_id: int, uploaded_docs: List[str]) -> List[str]
```

### Section 5: capex_service / capex_ai_service

```python
def suggest_capex(...) -> Dict[str, Any]
def get_ai_suggestion(...) -> Dict[str, Any]
```

### Section 6: API routes manquantes

Les endpoints API retournent 404 car les routes n'existent pas:
- POST /api/projects
- GET /api/projects/{id}/score
- GET /api/projects/{id}/capex-suggestion
- GET /api/projects/{id}/missing-documents

### Section 7: excel_service

```python
def generate_business_plan_excel(...) -> bytes
def generate_bank_dossier_pdf(...) -> bytes
def get_bank_dossier_content(...) -> Dict[str, Any]
```

### Section 8: privacy_shield_service

✅ CORRIGÉ - Le problème `metadata` est résolu

## Recommandation

**Implémenter dans l'ordre:**
1. Section 1 (logique pure) - CRITIQUE
2. Section 2-3 (timeline + waterfall)
4. Section 4 (documents)
5. Section 6 (API routes)
6. Section 5 (IA) - peut être mocké
7. Section 7 (exports) - peut attendre

## Commande pour tester une section

```bash
pytest tests/test_01_business_logic.py -v
```
