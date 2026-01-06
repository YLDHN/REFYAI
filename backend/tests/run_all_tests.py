"""
PLAN DE TEST BACKEND REFY AI - EXÉCUTION
=========================================

Ce fichier lance TOUS les tests selon le plan défini.
Les tests sont organisés en 8 sections critiques.

RÈGLE D'OR: Tant que ces tests ne sont pas TOUS au vert,
            AUCUNE clé OpenAI ne doit être intégrée.
"""
import pytest
import sys
from pathlib import Path

# Couleurs pour le terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_section(number, title):
    """Afficher l'en-tête de section"""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}SECTION {number}: {title}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")


def run_test_suite():
    """Exécuter la suite complète de tests"""
    
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}PLAN DE TEST BACKEND - REFY AI V5{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    test_sections = [
        ("01", "LOGIQUE MÉTIER PURE", "test_01_business_logic.py"),
        ("02", "MOTEUR DE PHASAGE TEMPOREL", "test_02_timeline_engine.py"),
        ("03", "MOTEUR FINANCIER (WATERFALL/PROMOTE)", "test_03_waterfall_promote.py"),
        ("04", "CONFORMITÉ DOCUMENTAIRE", "test_04_document_compliance.py"),
        ("05", "IA PRÉDICTIVE (MOCKS)", "test_05_ai_predictions_mock.py"),
        ("06", "API BOUT EN BOUT", "test_06_api_end_to_end.py"),
        ("07", "EXPORTS (EXCEL/PDF)", "test_07_exports_excel_pdf.py"),
        ("08", "CONFIDENTIALITÉ (PRIVACY SHIELD)", "test_08_privacy_shield.py"),
    ]
    
    results = {}
    total_passed = 0
    total_failed = 0
    
    for section_num, section_name, test_file in test_sections:
        print_section(section_num, section_name)
        
        test_path = Path(__file__).parent / test_file
        
        if not test_path.exists():
            print(f"{YELLOW}⚠️  Fichier non trouvé: {test_file}{RESET}")
            results[section_num] = "SKIP"
            continue
        
        # Exécuter les tests de cette section
        result = pytest.main([
            str(test_path),
            "-v",
            "--tb=short",
            "--disable-warnings"
        ])
        
        if result == 0:
            print(f"\n{GREEN}✅ Section {section_num} - RÉUSSIE{RESET}")
            results[section_num] = "PASS"
            total_passed += 1
        else:
            print(f"\n{RED}❌ Section {section_num} - ÉCHEC{RESET}")
            results[section_num] = "FAIL"
            total_failed += 1
    
    # Résumé final
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}RÉSUMÉ DES TESTS{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    for section_num, section_name, _ in test_sections:
        status = results.get(section_num, "SKIP")
        
        if status == "PASS":
            symbol = f"{GREEN}✅{RESET}"
        elif status == "FAIL":
            symbol = f"{RED}❌{RESET}"
        else:
            symbol = f"{YELLOW}⊘{RESET}"
        
        print(f"{symbol} Section {section_num}: {section_name}")
    
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{GREEN}RÉUSSIES: {total_passed}{RESET} | {RED}ÉCHECS: {total_failed}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    # Verdict final
    if total_failed == 0 and total_passed == len(test_sections):
        print(f"{GREEN}╔════════════════════════════════════════════════╗{RESET}")
        print(f"{GREEN}║  ✅ TOUS LES TESTS SONT VERTS                 ║{RESET}")
        print(f"{GREEN}║  Le backend est prêt pour l'intégration IA   ║{RESET}")
        print(f"{GREEN}╚════════════════════════════════════════════════╝{RESET}\n")
        return 0
    else:
        print(f"{RED}╔════════════════════════════════════════════════╗{RESET}")
        print(f"{RED}║  ❌ CERTAINS TESTS ONT ÉCHOUÉ                 ║{RESET}")
        print(f"{RED}║  NE PAS INTÉGRER LA CLÉ OPENAI AVANT FIX     ║{RESET}")
        print(f"{RED}╚════════════════════════════════════════════════╝{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(run_test_suite())
