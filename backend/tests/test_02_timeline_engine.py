"""
TEST SECTION 2: MOTEUR DE PHASAGE TEMPOREL (TIMELINE)
Tests du découpage en 3 phases avec alignement des flux
"""
import pytest
from datetime import datetime, timedelta
from app.services.financial_service import financial_service


class TestPhasageProjet:
    """Test découpage projet en 3 phases distinctes"""
    
    def test_trois_phases_obligatoires(self):
        """Tout projet a exactement 3 phases"""
        timeline = financial_service.generate_project_timeline(
            project_start=datetime(2026, 1, 1),
            permit_duration_months=12,
            construction_duration_months=18,
            commercialization_duration_months=12
        )
        
        assert len(timeline["phases"]) == 3
        assert timeline["phases"][0]["name"] == "ÉTUDES_PERMIS"
        assert timeline["phases"][1]["name"] == "TRAVAUX"
        assert timeline["phases"][2]["name"] == "COMMERCIALISATION"
    
    def test_phases_sequentielles_sans_chevauchement(self):
        """Les phases sont strictement séquentielles"""
        timeline = financial_service.generate_project_timeline(
            project_start=datetime(2026, 1, 1),
            permit_duration_months=6,
            construction_duration_months=12,
            commercialization_duration_months=6
        )
        
        phase1_end = timeline["phases"][0]["end_date"]
        phase2_start = timeline["phases"][1]["start_date"]
        phase2_end = timeline["phases"][1]["end_date"]
        phase3_start = timeline["phases"][2]["start_date"]
        
        # Phase 2 commence après phase 1
        assert phase2_start >= phase1_end
        # Phase 3 commence après phase 2
        assert phase3_start >= phase2_end


class TestDecaissementsCAPEX:
    """Test: CAPEX uniquement pendant phase Travaux"""
    
    def test_capex_uniquement_phase_travaux(self):
        """Les décaissements CAPEX n'existent que pendant Travaux"""
        timeline = financial_service.generate_project_timeline(
            project_start=datetime(2026, 1, 1),
            permit_duration_months=6,
            construction_duration_months=12,
            commercialization_duration_months=6
        )
        
        cashflows = financial_service.generate_cashflows(
            timeline=timeline,
            capex_total=1_000_000,
            monthly_rent=0,  # Pas de revenus avant fin
            capex_distribution="LINEAR"
        )
        
        # Aucun CAPEX pendant phase 1 (permis)
        phase1_capex = sum(
            cf["capex"] for cf in cashflows 
            if cf["phase"] == "ÉTUDES_PERMIS"
        )
        assert phase1_capex == 0
        
        # CAPEX uniquement en phase 2 (travaux)
        phase2_capex = sum(
            cf["capex"] for cf in cashflows 
            if cf["phase"] == "TRAVAUX"
        )
        assert phase2_capex == 1_000_000
        
        # Aucun CAPEX pendant phase 3 (commercialisation)
        phase3_capex = sum(
            cf["capex"] for cf in cashflows 
            if cf["phase"] == "COMMERCIALISATION"
        )
        assert phase3_capex == 0
    
    def test_distribution_capex_lineaire(self):
        """Distribution linéaire du CAPEX sur la durée des travaux"""
        timeline = financial_service.generate_project_timeline(
            project_start=datetime(2026, 1, 1),
            permit_duration_months=6,
            construction_duration_months=12,
            commercialization_duration_months=6
        )
        
        cashflows = financial_service.generate_cashflows(
            timeline=timeline,
            capex_total=1_200_000,  # Divisible par 12
            monthly_rent=0,
            capex_distribution="LINEAR"
        )
        
        phase2_cashflows = [cf for cf in cashflows if cf["phase"] == "TRAVAUX"]
        
        # Chaque mois doit avoir le même CAPEX
        monthly_capex_values = [cf["capex"] for cf in phase2_cashflows]
        assert all(v == 100_000 for v in monthly_capex_values)


class TestEntreesCash:
    """Test: Revenus uniquement pendant Commercialisation"""
    
    def test_revenus_uniquement_apres_travaux(self):
        """Les revenus (loyers/ventes) n'existent qu'après les travaux"""
        timeline = financial_service.generate_project_timeline(
            project_start=datetime(2026, 1, 1),
            permit_duration_months=6,
            construction_duration_months=12,
            commercialization_duration_months=12
        )
        
        cashflows = financial_service.generate_cashflows(
            timeline=timeline,
            capex_total=1_000_000,
            monthly_rent=50_000,
            capex_distribution="LINEAR"
        )
        
        # Aucun revenu pendant phases 1 et 2
        phases_1_2_revenue = sum(
            cf["revenue"] for cf in cashflows 
            if cf["phase"] in ["ÉTUDES_PERMIS", "TRAVAUX"]
        )
        assert phases_1_2_revenue == 0
        
        # Revenus uniquement en phase 3
        phase3_revenue = sum(
            cf["revenue"] for cf in cashflows 
            if cf["phase"] == "COMMERCIALISATION"
        )
        assert phase3_revenue > 0
    
    def test_pas_de_revenus_avant_fin_travaux(self):
        """Incohérence temporelle: revenus avant fin travaux = erreur"""
        timeline = financial_service.generate_project_timeline(
            project_start=datetime(2026, 1, 1),
            permit_duration_months=6,
            construction_duration_months=12,
            commercialization_duration_months=12
        )
        
        construction_end = timeline["phases"][1]["end_date"]
        
        cashflows = financial_service.generate_cashflows(
            timeline=timeline,
            capex_total=1_000_000,
            monthly_rent=50_000,
            capex_distribution="LINEAR"
        )
        
        # Vérifier qu'aucun flux de revenus n'existe avant la fin des travaux
        for cf in cashflows:
            if cf["date"] < construction_end:
                assert cf["revenue"] == 0, \
                    "Revenus détectés avant fin travaux (incohérence temporelle)"


class TestAlignementTemporel:
    """Test: Cohérence temporelle globale"""
    
    def test_pas_de_chevauchement_capex_revenus(self):
        """CAPEX et revenus ne doivent jamais se chevaucher"""
        timeline = financial_service.generate_project_timeline(
            project_start=datetime(2026, 1, 1),
            permit_duration_months=6,
            construction_duration_months=12,
            commercialization_duration_months=12
        )
        
        cashflows = financial_service.generate_cashflows(
            timeline=timeline,
            capex_total=1_000_000,
            monthly_rent=50_000,
            capex_distribution="LINEAR"
        )
        
        # Aucun mois ne doit avoir à la fois CAPEX et revenus
        for cf in cashflows:
            if cf["capex"] > 0:
                assert cf["revenue"] == 0, \
                    f"Chevauchement détecté: CAPEX et revenus le même mois ({cf['date']})"
    
    def test_duree_totale_coherente(self):
        """La durée totale = somme des 3 phases"""
        timeline = financial_service.generate_project_timeline(
            project_start=datetime(2026, 1, 1),
            permit_duration_months=6,
            construction_duration_months=12,
            commercialization_duration_months=12
        )
        
        total_duration_months = (
            timeline["phases"][0]["duration_months"] +
            timeline["phases"][1]["duration_months"] +
            timeline["phases"][2]["duration_months"]
        )
        
        project_start = timeline["project_start"]
        project_end = timeline["project_end"]
        actual_duration_months = (project_end.year - project_start.year) * 12 + \
                                 (project_end.month - project_start.month)
        
        assert abs(total_duration_months - actual_duration_months) <= 1  # Tolérance 1 mois


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
