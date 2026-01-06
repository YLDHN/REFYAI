"""
Script de test complet des endpoints API
Teste tous les nouveaux endpoints créés
"""
import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
PROJECT_ID = 1  # À adapter selon votre DB


def print_section(title):
    """Print section séparateur"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_endpoint(method, endpoint, data=None, description=""):
    """Test un endpoint et affiche résultat"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n🔍 {description}")
    print(f"   {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            print(f"❌ Méthode {method} non supportée")
            return
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ SUCCESS")
            # Afficher quelques clés importantes
            if isinstance(result, dict):
                if "success" in result:
                    print(f"      Success: {result['success']}")
                if "score" in result:
                    print(f"      Score: {result['score']}")
                if "total_fees" in result:
                    print(f"      Total fees: {result['total_fees']}")
                if "total_capex" in result:
                    print(f"      Total CAPEX: {result['total_capex']}")
        else:
            print(f"   ❌ FAILED: {response.text[:200]}")
    
    except requests.exceptions.ConnectionError:
        print(f"   ⚠️  SERVEUR NON ACCESSIBLE (normal si pas démarré)")
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")


def main():
    """Tests complets de l'API"""
    
    print("\n" + "🚀"*30)
    print("TESTS API REFY AI BACKEND V5")
    print("🚀"*30)
    
    
    # === 1. TIMELINE ===
    print_section("1. TIMELINE - Phases projet")
    
    timeline_data = {
        "project_id": PROJECT_ID,
        "studies_start": "2025-01-01",
        "studies_end": "2025-03-31",
        "studies_budget": 15000,
        "permit_start": "2025-04-01",
        "permit_end": "2025-10-31",
        "permit_budget": 5000,
        "construction_start": "2025-11-01",
        "construction_end": "2026-10-31",
        "construction_budget": 500000,
        "commercialization_start": "2026-11-01",
        "commercialization_end": "2027-04-30",
        "commercialization_budget": 20000,
        "capex_curve_type": "S_CURVE",
        "execution_mode": "sequential"
    }
    
    test_endpoint("POST", "/timeline/", timeline_data, "Créer timeline projet")
    test_endpoint("GET", f"/timeline/{PROJECT_ID}", description="Récupérer timeline")
    test_endpoint("GET", f"/timeline/{PROJECT_ID}/cashflow", description="Calculer cash-flows")
    
    
    # === 2. NOTARY FEES ===
    print_section("2. FRAIS DE NOTAIRE - Algorithme intelligent")
    
    notary_data = {
        "price": 200000,
        "buyer_profile": "MDB",
        "building_age": 10
    }
    
    test_endpoint("POST", "/financial/notary-fees", notary_data, "Calculer frais notaire MDB")
    test_endpoint("POST", "/financial/notary-fees/compare", {"price": 200000}, "Comparer profils")
    
    
    # === 3. WATERFALL ===
    print_section("3. WATERFALL - Distribution LP/GP")
    
    waterfall_simple = {
        "lp_investment": 100000,
        "gp_investment": 0,
        "profit": 15000,
        "hurdle_rate": 0.08
    }
    
    test_endpoint("POST", "/financial/waterfall/simple", waterfall_simple, "Waterfall simple")
    
    waterfall_advanced = {
        "lp_investment": 100000,
        "gp_investment": 0,
        "profit": 25000,
        "tiers": [
            {"threshold": 0.08, "lp_split": 1.00, "gp_split": 0.00},
            {"threshold": 0.15, "lp_split": 0.80, "gp_split": 0.20},
            {"threshold": float('inf'), "lp_split": 0.70, "gp_split": 0.30}
        ]
    }
    
    test_endpoint("POST", "/financial/waterfall/advanced", waterfall_advanced, "Waterfall avancé")
    
    
    # === 4. AMORTIZATION ===
    print_section("4. AMORTISSEMENT - In-Fine et Différé")
    
    classic_loan = {
        "loan_amount": 100000,
        "annual_rate": 0.04,
        "duration_years": 20,
        "amortization_type": "CLASSIC"
    }
    
    test_endpoint("POST", "/financial/loan/schedule", classic_loan, "Amortissement classique")
    
    in_fine_loan = {
        "loan_amount": 100000,
        "annual_rate": 0.04,
        "duration_years": 20,
        "amortization_type": "IN_FINE"
    }
    
    test_endpoint("POST", "/financial/loan/schedule", in_fine_loan, "Amortissement In-Fine")
    
    deferred_loan = {
        "loan_amount": 100000,
        "annual_rate": 0.04,
        "duration_years": 20,
        "amortization_type": "DEFERRED",
        "deferred_months": 12,
        "capitalize_deferred_interest": True
    }
    
    test_endpoint("POST", "/financial/loan/schedule", deferred_loan, "Amortissement différé")
    
    compare_data = {
        "loan_amount": 100000,
        "annual_rate": 0.04,
        "duration_years": 20
    }
    
    test_endpoint("POST", "/financial/loan/compare", compare_data, "Comparer types amortissement")
    
    
    # === 5. ASSET MANAGEMENT ===
    print_section("5. ASSET MANAGEMENT - Rent Free & Indexation")
    
    rent_schedule = {
        "monthly_rent": 1000,
        "rent_free_months": 3,
        "duration_years": 5,
        "indexation_type": "ICC",
        "indexation_rate": 0.02,
        "indexation_start_year": 1
    }
    
    test_endpoint("POST", "/asset-management/rent-schedule", rent_schedule, "Loyers avec franchise")
    
    indexation = {
        "base_rent": 1000,
        "duration_years": 10,
        "indexation_type": "ILAT"
    }
    
    test_endpoint("POST", "/asset-management/indexation-projection", indexation, "Projection indexation")
    
    ti_optimize = {
        "ti_budget": 20000,
        "rent_increase": 200,
        "lease_duration_years": 9
    }
    
    test_endpoint("POST", "/asset-management/ti-optimization", ti_optimize, "Optimiser travaux locataire")
    
    
    # === 6. SCRAPING ===
    print_section("6. SCRAPING - Cadastre & PLU")
    
    test_endpoint("GET", "/scraper/health", description="Santé workers Celery")
    
    scrape_data = {"project_id": PROJECT_ID}
    test_endpoint("POST", f"/scraper/start/{PROJECT_ID}", description="Lancer scraping projet")
    
    
    # === 7. CAPEX IA ===
    print_section("7. CAPEX IA - Suggestions intelligentes")
    
    capex_suggest = {
        "project_description": "Réhabilitation immeuble haussmannien 800m2 Paris, 6 appartements, façade à refaire",
        "surface": 800,
        "typologie": "RENOVATION",
        "city_tier": 1
    }
    
    test_endpoint("POST", "/capex/suggest", capex_suggest, "Suggestions CAPEX IA")
    test_endpoint("GET", "/capex/categories", description="Catégories CAPEX disponibles")
    
    
    # === 8. DOCUMENTS COMPLIANCE ===
    print_section("8. COMPLIANCE - Documents manquants")
    
    test_endpoint("GET", f"/documents/missing/{PROJECT_ID}", description="Analyser documents manquants")
    test_endpoint("GET", "/documents/required/RENOVATION", description="Documents requis RENOVATION")
    
    
    # === 9. SCORING TECHNIQUE ===
    print_section("9. SCORING - Score technique /100")
    
    scoring_data = {
        "abf_zone": False,
        "secteur_sauvegarde": False,
        "plu_zone": "U",
        "amiante_present": True,
        "dpe_classe": "F",
        "ltv": 0.75,
        "dscr": 1.3,
        "tri": 0.10,
        "zone_inondable": False
    }
    
    test_endpoint("POST", "/scoring/calculate", scoring_data, "Calculer score technique")
    test_endpoint("GET", "/scoring/risks-reference", description="Référentiel risques")
    
    
    # === 10. PDF EXPORTS ===
    print_section("10. EXPORTS - Dossier banque PDF")
    
    test_endpoint("POST", f"/exports/bank-package/{PROJECT_ID}?include_documents=true", 
                 description="Générer dossier banque PDF")
    
    
    # === RÉSUMÉ ===
    print("\n" + "="*60)
    print("✅ TESTS TERMINÉS")
    print("="*60)
    print("\n📝 Notes:")
    print("   - Erreurs 'SERVEUR NON ACCESSIBLE' = normal si backend pas démarré")
    print("   - Erreurs 404 = normal si projet_id=1 n'existe pas")
    print("   - Pour tests réels: démarrer backend avec 'uvicorn app.main:app'")
    print("   - Documentation Swagger: http://localhost:8000/docs")
    print("\n")


if __name__ == "__main__":
    main()
