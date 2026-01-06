"""
TEST SECTION 1: LOGIQUE MÉTIER PURE
Tests déterministes sans IA, sans API, sans base externe
"""
import pytest
from app.services.financial_service import financial_service


class TestScoreTechnique:
    """Test du calcul du score technique (/100) avec pénalités cumulées"""
    
    def test_score_parfait_sans_penalites(self):
        """Projet parfait = 100/100"""
        result = financial_service.calculate_technical_score(
            has_construction_permit=True,
            has_environmental_studies=True,
            has_soil_study=True,
            has_abf_clearance=True,
            has_urban_planning_certificate=True,
            structural_issues=False,
            pollution_detected=False,
            protected_area=False
        )
        
        assert result["score"] == 100
        assert result["grade"] == "A"
        assert len(result["penalties"]) == 0
    
    def test_score_avec_penalites_multiples(self):
        """Plusieurs pénalités doivent s'accumuler"""
        result = financial_service.calculate_technical_score(
            has_construction_permit=False,  # -20 points
            has_environmental_studies=False,  # -15 points
            has_soil_study=True,
            has_abf_clearance=True,
            has_urban_planning_certificate=True,
            structural_issues=True,  # -25 points
            pollution_detected=False,
            protected_area=False
        )
        
        assert result["score"] == 40  # 100 - 20 - 15 - 25
        assert result["grade"] == "E"
        assert len(result["penalties"]) == 3
    
    def test_score_minimum_zero(self):
        """Le score ne peut pas être négatif"""
        result = financial_service.calculate_technical_score(
            has_construction_permit=False,
            has_environmental_studies=False,
            has_soil_study=False,
            has_abf_clearance=False,
            has_urban_planning_certificate=False,
            structural_issues=True,
            pollution_detected=True,
            protected_area=True
        )
        
        assert result["score"] >= 0
        assert result["grade"] == "F"


class TestFraisNotaire:
    """Test calcul frais de notaire selon profil"""
    
    def test_frais_notaire_neuf(self):
        """Neuf = 2-3% du prix"""
        result = financial_service.calculate_notary_fees(
            purchase_price=1_000_000,
            property_type="NEUF",
            buyer_profile="PRIMO_ACCEDANT"
        )
        
        assert 20_000 <= result["notary_fees"] <= 30_000
        assert result["tax_rate"] < 0.05  # Réduit pour le neuf
    
    def test_frais_notaire_ancien(self):
        """Ancien = 7-8% du prix"""
        result = financial_service.calculate_notary_fees(
            purchase_price=1_000_000,
            property_type="ANCIEN",
            buyer_profile="INVESTISSEUR"
        )
        
        assert 70_000 <= result["notary_fees"] <= 80_000
        assert result["tax_rate"] > 0.05
    
    def test_frais_notaire_mdb(self):
        """MDB (Marchand de Biens) avec régime spécifique"""
        result = financial_service.calculate_notary_fees(
            purchase_price=1_000_000,
            property_type="ANCIEN",
            buyer_profile="MDB"
        )
        
        # MDB peut bénéficier d'un régime réduit
        assert result["notary_fees"] < 80_000
        assert result["buyer_profile"] == "MDB"


class TestRisqueFiscalMDB:
    """Test détection automatique risque fiscal MDB"""
    
    def test_pas_de_risque_si_duree_courte(self):
        """Pas de risque fiscal si durée < 5 ans"""
        result = financial_service.check_mdb_tax_risk(
            project_duration_years=4,
            buyer_profile="MDB"
        )
        
        assert result["has_risk"] is False
        assert "warning" not in result
    
    def test_risque_si_duree_longue(self):
        """Risque fiscal si durée > 5 ans pour MDB"""
        result = financial_service.check_mdb_tax_risk(
            project_duration_years=6,
            buyer_profile="MDB"
        )
        
        assert result["has_risk"] is True
        assert "warning" in result
        assert "5 ans" in result["warning"].lower()
    
    def test_pas_de_risque_si_pas_mdb(self):
        """Pas de risque si ce n'est pas un MDB"""
        result = financial_service.check_mdb_tax_risk(
            project_duration_years=10,
            buyer_profile="INVESTISSEUR"
        )
        
        assert result["has_risk"] is False


class TestCalculDette:
    """Test calcul dette à partir LTV/LTC (logique inversée)"""
    
    def test_calcul_dette_ltv(self):
        """Dette = Valeur × LTV"""
        result = financial_service.calculate_debt_from_ltv(
            asset_value=1_000_000,
            ltv=0.70
        )
        
        assert result["debt_amount"] == 700_000
        assert result["equity"] == 300_000
        assert result["ltv"] == 0.70
    
    def test_calcul_dette_ltc(self):
        """Dette = Coût Total × LTC"""
        result = financial_service.calculate_debt_from_ltc(
            total_cost=1_200_000,  # Acquisition + Travaux
            ltc=0.65
        )
        
        assert result["debt_amount"] == 780_000
        assert result["equity"] == 420_000
        assert result["ltc"] == 0.65
    
    def test_ltv_maximum_100(self):
        """LTV ne peut pas dépasser 100%"""
        with pytest.raises(ValueError, match="LTV ne peut pas dépasser 100%"):
            financial_service.calculate_debt_from_ltv(
                asset_value=1_000_000,
                ltv=1.20
            )
    
    def test_calcul_deterministe(self):
        """Résultats strictement déterministes"""
        result1 = financial_service.calculate_debt_from_ltv(500_000, 0.75)
        result2 = financial_service.calculate_debt_from_ltv(500_000, 0.75)
        
        assert result1 == result2
        assert result1["debt_amount"] == 375_000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
