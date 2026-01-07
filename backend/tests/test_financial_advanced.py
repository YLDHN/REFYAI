"""
Tests unitaires pour services financiers avancés
"""
import pytest
from app.services.financial_service import financial_service, AmortizationType
from app.services.notary_fee_service import notary_fee_service, BuyerProfile
from app.services.waterfall_service import waterfall_service
from app.services.asset_management_service import asset_management_service, IndexationType


class TestAmortizationAdvanced:
    """Tests amortissements avancés"""
    
    def test_classic_amortization(self):
        """Test amortissement classique"""
        result = financial_service.calculate_loan_schedule(
            loan_amount=100000,
            annual_rate=0.04,
            years=20,
            amortization_type=AmortizationType.CLASSIC
        )
        
        assert result["success"] is True
        assert len(result["schedule"]) == 240  # 20 ans * 12 mois
        assert result["total_interest"] > 0
        
        # Vérifier première mensualité
        first_payment = result["schedule"][0]
        assert first_payment["month"] == 1
        assert first_payment["principal"] > 0
        assert first_payment["interest"] > 0
        assert first_payment["payment"] > 0
        
        # Vérifier dernière mensualité
        last_payment = result["schedule"][-1]
        assert abs(last_payment["remaining_capital"]) < 1  # Quasi 0
    
    def test_in_fine_amortization(self):
        """Test amortissement In-Fine"""
        result = financial_service.calculate_loan_schedule(
            loan_amount=100000,
            annual_rate=0.04,
            years=20,
            amortization_type=AmortizationType.IN_FINE
        )
        
        assert result["success"] is True
        
        # In-Fine : capital remboursé à la fin uniquement
        first_payment = result["schedule"][0]
        assert first_payment["principal"] == 0
        assert first_payment["interest"] > 0
        
        # Dernière mensualité : capital + intérêts
        last_payment = result["schedule"][-1]
        assert last_payment["principal"] == 100000
        assert last_payment["remaining_capital"] == 0
    
    def test_deferred_amortization_capitalized(self):
        """Test amortissement différé avec capitalisation"""
        result = financial_service.calculate_loan_schedule(
            loan_amount=100000,
            annual_rate=0.04,
            years=20,
            amortization_type=AmortizationType.DEFERRED,
            deferred_months=12,
            deferred_interest_capitalized=True
        )
        
        assert result["success"] is True
        
        # Pendant différé : pas de paiement, capital augmente
        first_payment = result["schedule"][0]
        assert first_payment["payment"] == 0
        assert first_payment["remaining_capital"] > 100000  # Capitalisation
        
        # Après différé : amortissement normal
        post_deferred = result["schedule"][12]
        assert post_deferred["principal"] > 0
        assert post_deferred["interest"] > 0
    
    def test_deferred_amortization_paid(self):
        """Test amortissement différé avec intérêts payés"""
        result = financial_service.calculate_loan_schedule(
            loan_amount=100000,
            annual_rate=0.04,
            years=20,
            amortization_type=AmortizationType.DEFERRED,
            deferred_months=12,
            deferred_interest_capitalized=False
        )
        
        assert result["success"] is True
        
        # Pendant différé : paiement intérêts uniquement
        first_payment = result["schedule"][0]
        assert first_payment["principal"] == 0
        assert first_payment["interest"] > 0
        assert first_payment["payment"] == first_payment["interest"]
        assert first_payment["remaining_capital"] == 100000  # Pas de capitalisation
    
    def test_compare_amortization_types(self):
        """Test comparaison types amortissements"""
        result = financial_service.compare_amortization_types(
            loan_amount=100000,
            annual_rate=0.04,
            years=20
        )
        
        assert result["success"] is True
        assert "classic" in result["comparison"]
        assert "in_fine" in result["comparison"]
        assert "deferred_capitalized" in result["comparison"]
        
        # In-Fine doit être le plus cher (intérêts non amortis)
        classic_cost = result["comparison"]["classic"]["total_cost"]
        in_fine_cost = result["comparison"]["in_fine"]["total_cost"]
        assert in_fine_cost > classic_cost
        
        # Recommandation
        assert result["recommendation"]["cheapest_option"] in ["classic", "in_fine", "deferred_capitalized", "deferred_paid"]


class TestNotaryFees:
    """Tests frais de notaire intelligents"""
    
    def test_notary_fees_neuf(self):
        """Test frais NEUF (2.5%)"""
        result = notary_fee_service.calculate_notary_fees(
            purchase_price=200000,
            buyer_profile=BuyerProfile.NEUF
        )
        
        assert result["success"] is True
        assert result["notary_fee_amount"] == pytest.approx(200000 * 0.025, rel=0.01)
        assert result["notary_fee_rate"] == pytest.approx(0.025, abs=0.001)
        assert result.get("alert") is None  # Pas d'alerte pour NEUF
    
    def test_notary_fees_mdb(self):
        """Test frais MDB (3%)"""
        result = notary_fee_service.calculate_notary_fees(
            purchase_price=200000,
            buyer_profile=BuyerProfile.MDB
        )
        
        assert result["success"] is True
        assert result["notary_fee_amount"] == pytest.approx(200000 * 0.03, rel=0.01)
        
        # Pas d'alerte CRITICAL si pas d'âge bâtiment
        assert result.get("alert_severity") != "CRITICAL"
    
    def test_notary_fees_mdb_alert_old_building(self):
        """Test alerte MDB + immeuble ancien"""
        result = notary_fee_service.calculate_notary_fees(
            purchase_price=200000,
            buyer_profile=BuyerProfile.MDB,
            building_age_years=10  # > 5 ans
        )
        
        assert result["success"] is True
        
        # Alerte CRITIQUE : MDB sur ancien
        assert result.get("alert_severity") == "CRITICAL"
        assert "fiscale" in result.get("alert", "").lower() or "fiscal" in result.get("alert", "").lower()
    
    def test_notary_fees_investor(self):
        """Test frais INVESTOR (7.5%)"""
        result = notary_fee_service.calculate_notary_fees(
            purchase_price=200000,
            buyer_profile=BuyerProfile.INVESTOR
        )
        
        assert result["success"] is True
        assert result["notary_fee_amount"] == pytest.approx(200000 * 0.075, rel=0.01)
    
    def test_compare_profiles(self):
        """Test comparaison profils acheteurs"""
        result = notary_fee_service.compare_profiles(
            purchase_price=200000,
            building_age_years=3  # Bien récent
        )
        
        assert "profiles" in result
        assert len(result["profiles"]) == 3
        
        # NEUF doit être le moins cher
        neuf_fees = result["profiles"]["NEUF"]["notary_fee_amount"]
        investor_fees = result["profiles"]["INVESTOR"]["notary_fee_amount"]
        assert neuf_fees < investor_fees


class TestWaterfall:
    """Tests distribution Waterfall"""
    
    def test_waterfall_simple_below_hurdle(self):
        """Test waterfall simple sous hurdle"""
        result = waterfall_service.calculate_waterfall_simple(
            lp_contrib=100000,
            gp_investment=0,
            profit=5000,  # 5% < 8% hurdle
            hurdle_rate=0.08
        )
        
        assert result["success"] is True
        
        # Sous hurdle : tout aux LP (100%)
        assert result["lp_share"] == pytest.approx(5000, abs=1)
        assert result["gp_share"] == 0
    
    def test_waterfall_simple_above_hurdle(self):
        """Test waterfall simple au-dessus hurdle"""
        result = waterfall_service.calculate_waterfall_simple(
            lp_contrib=100000,
            gp_investment=0,
            profit=15000,  # 15% > 8% hurdle
            hurdle_rate=0.08
        )
        
        assert result["success"] is True
        
        # Au-dessus hurdle : 80/20 sur excédent
        hurdle_amount = 100000 * 0.08  # 8000
        excess = 15000 - hurdle_amount  # 7000
        
        expected_lp = hurdle_amount + (excess * 0.80)  # 8000 + 5600 = 13600
        expected_gp = excess * 0.20  # 1400
        
        assert result["lp_share"] == pytest.approx(expected_lp, abs=1)
        assert result["gp_share"] == pytest.approx(expected_gp, abs=1)
    
    def test_waterfall_advanced_multi_tier(self):
        """Test waterfall avancé multi-paliers"""
        tiers = [
            {"threshold_irr": 0.08, "lp_share": 1.00, "gp_share": 0.00},
            {"threshold_irr": 0.12, "lp_share": 0.80, "gp_share": 0.20},
            {"threshold_irr": 0.18, "lp_share": 0.70, "gp_share": 0.30},
            {"threshold_irr": float('inf'), "lp_share": 0.60, "gp_share": 0.40}
        ]
        
        result = waterfall_service.calculate_waterfall_advanced(
            equity_invested=100000,
            total_profit=25000,  # 25% IRR
            tiers=tiers
        )
        
        assert "distribution" in result
        assert "tiers" in result["distribution"]
    
    def test_waterfall_sensitivity(self):
        """Test analyse sensibilité waterfall"""
        result = waterfall_service.calculate_promote_sensitivity(
            equity_invested=100000,
            profit_range=[5000, 10000, 15000, 20000, 25000, 30000],
            hurdle_rate=0.08
        )
        
        assert isinstance(result, list)
        assert len(result) > 0
        
        # À profit élevé, GP doit augmenter
        if len(result) > 1:
            assert result[-1]["gp_total"] >= result[0]["gp_total"]


class TestAssetManagement:
    """Tests gestion locative"""
    
    def test_rent_schedule_with_rent_free(self):
        """Test loyers avec franchise"""
        from datetime import datetime
        result = asset_management_service.calculate_rent_schedule_with_rent_free(
            annual_rent=12000,  # 1000€/mois
            lease_start_date=datetime(2024, 1, 1),
            lease_duration_years=5,
            rent_free_months=3,
            indexation_type="FIXED",
            indexation_rate=0.0
        )
        
        assert "schedule" in result
        
        # 3 premiers mois à 0
        assert result["schedule"][0]["rent_payment"] == 0
        assert result["schedule"][1]["rent_payment"] == 0
        assert result["schedule"][2]["rent_payment"] == 0
        
        # 4ème mois : loyer normal (12000 / 12 = 1000)
        assert result["schedule"][3]["rent_payment"] == pytest.approx(1000, abs=1)
        
        # Total : (60 mois - 3 mois) * 1000 = 57000
        assert result["financial_impact"]["total_rent_received"] == pytest.approx(57000, abs=100)
    
    def test_rent_schedule_with_indexation_icc(self):
        """Test loyers avec indexation ICC"""
        from datetime import datetime
        result = asset_management_service.calculate_rent_schedule_with_rent_free(
            annual_rent=12000,  # 1000€/mois
            lease_start_date=datetime(2024, 1, 1),
            lease_duration_years=3,
            rent_free_months=0,
            indexation_type="ICC",
            indexation_rate=0.02,
            indexation_start_year=1
        )
        
        assert "schedule" in result
        
        # Année 1 mois 1 : loyer de base (12000 / 12 = 1000)
        assert result["schedule"][0]["rent_payment"] == pytest.approx(1000, abs=1)
        
        # Après première indexation (mois 13)
        assert result["schedule"][12]["rent_payment"] >= 1000
    
    def test_indexation_projection(self):
        """Test projection indexation scenarios"""
        result = asset_management_service.calculate_indexation_projection(
            initial_rent=1000,
            years=10,
            indexation_type="ILAT"
        )
        
        assert "pessimistic" in result or "scenarios" in result
        
        # Vérifier que la projection existe
        if "scenarios" in result:
            assert len(result["scenarios"]) > 0
    
    def test_rent_free_value(self):
        """Test valeur actualisée franchise"""
        result = asset_management_service.calculate_rent_free_value(
            monthly_rent=1000,
            rent_free_months=6,
            discount_rate=0.08
        )
        
        assert "nominal_value" in result
        assert result["nominal_value"] == 6000
        assert result["present_value"] < 6000  # NPV < valeur nominale
        assert result["present_value"] > 5800  # Mais proche
    
    def test_optimize_tenant_improvements(self):
        """Test optimisation travaux locataire"""
        result = asset_management_service.optimize_tenant_improvements(
            monthly_rent=1000,
            tenant_improvements_options=[
                {"cost": 20000, "rent_increase": 200}
            ],
            lease_duration_years=9
        )
        
        assert isinstance(result, dict)
        assert "options_analysis" in result
        assert len(result["options_analysis"]) > 0
        
        # Vérifier le premier élément
        option = result["options_analysis"][0]
        assert option["total_additional_rent"] == pytest.approx(200 * 12 * 9, abs=100)


# === RUN TESTS ===
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
