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
            duration_years=20,
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
        assert first_payment["total_payment"] > 0
        
        # Vérifier dernière mensualité
        last_payment = result["schedule"][-1]
        assert abs(last_payment["remaining_balance"]) < 1  # Quasi 0
    
    def test_in_fine_amortization(self):
        """Test amortissement In-Fine"""
        result = financial_service.calculate_loan_schedule(
            loan_amount=100000,
            annual_rate=0.04,
            duration_years=20,
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
        assert last_payment["remaining_balance"] == 0
    
    def test_deferred_amortization_capitalized(self):
        """Test amortissement différé avec capitalisation"""
        result = financial_service.calculate_loan_schedule(
            loan_amount=100000,
            annual_rate=0.04,
            duration_years=20,
            amortization_type=AmortizationType.DEFERRED,
            deferred_months=12,
            capitalize_deferred_interest=True
        )
        
        assert result["success"] is True
        
        # Pendant différé : pas de paiement, capital augmente
        first_payment = result["schedule"][0]
        assert first_payment["total_payment"] == 0
        assert first_payment["remaining_balance"] > 100000  # Capitalisation
        
        # Après différé : amortissement normal
        post_deferred = result["schedule"][12]
        assert post_deferred["principal"] > 0
        assert post_deferred["interest"] > 0
    
    def test_deferred_amortization_paid(self):
        """Test amortissement différé avec intérêts payés"""
        result = financial_service.calculate_loan_schedule(
            loan_amount=100000,
            annual_rate=0.04,
            duration_years=20,
            amortization_type=AmortizationType.DEFERRED,
            deferred_months=12,
            capitalize_deferred_interest=False
        )
        
        assert result["success"] is True
        
        # Pendant différé : paiement intérêts uniquement
        first_payment = result["schedule"][0]
        assert first_payment["principal"] == 0
        assert first_payment["interest"] > 0
        assert first_payment["total_payment"] == first_payment["interest"]
        assert first_payment["remaining_balance"] == 100000  # Pas de capitalisation
    
    def test_compare_amortization_types(self):
        """Test comparaison types amortissements"""
        result = financial_service.compare_amortization_types(
            loan_amount=100000,
            annual_rate=0.04,
            duration_years=20
        )
        
        assert result["success"] is True
        assert "CLASSIC" in result["comparisons"]
        assert "IN_FINE" in result["comparisons"]
        assert "DEFERRED" in result["comparisons"]
        
        # In-Fine doit être le plus cher (intérêts non amortis)
        classic_cost = result["comparisons"]["CLASSIC"]["total_cost"]
        in_fine_cost = result["comparisons"]["IN_FINE"]["total_cost"]
        assert in_fine_cost > classic_cost
        
        # Recommandation
        assert result["recommendation"] in ["CLASSIC", "IN_FINE", "DEFERRED"]


class TestNotaryFees:
    """Tests frais de notaire intelligents"""
    
    def test_notary_fees_neuf(self):
        """Test frais NEUF (2.5%)"""
        result = notary_fee_service.calculate_notary_fees(
            price=200000,
            buyer_profile=BuyerProfile.NEUF
        )
        
        assert result["success"] is True
        assert result["total_fees"] == pytest.approx(200000 * 0.025, rel=0.01)
        assert result["effective_rate"] == pytest.approx(0.025, abs=0.001)
        assert len(result["alerts"]) == 0  # Pas d'alerte pour NEUF
    
    def test_notary_fees_mdb(self):
        """Test frais MDB (3%)"""
        result = notary_fee_service.calculate_notary_fees(
            price=200000,
            buyer_profile=BuyerProfile.MDB
        )
        
        assert result["success"] is True
        assert result["total_fees"] == pytest.approx(200000 * 0.03, rel=0.01)
        
        # Pas d'alerte si pas d'âge bâtiment
        assert all(a["level"] != "CRITICAL" for a in result["alerts"])
    
    def test_notary_fees_mdb_alert_old_building(self):
        """Test alerte MDB + immeuble ancien"""
        result = notary_fee_service.calculate_notary_fees(
            price=200000,
            buyer_profile=BuyerProfile.MDB,
            building_age=10  # > 5 ans
        )
        
        assert result["success"] is True
        
        # Alerte CRITIQUE : MDB sur ancien
        critical_alerts = [a for a in result["alerts"] if a["level"] == "CRITICAL"]
        assert len(critical_alerts) > 0
        assert "fiscale" in critical_alerts[0]["message"].lower()
    
    def test_notary_fees_investor(self):
        """Test frais INVESTOR (7.5%)"""
        result = notary_fee_service.calculate_notary_fees(
            price=200000,
            buyer_profile=BuyerProfile.INVESTOR
        )
        
        assert result["success"] is True
        assert result["total_fees"] == pytest.approx(200000 * 0.075, rel=0.01)
    
    def test_compare_profiles(self):
        """Test comparaison profils acheteurs"""
        result = notary_fee_service.compare_profiles(price=200000)
        
        assert result["success"] is True
        assert len(result["profiles"]) == 3
        
        # NEUF doit être le moins cher
        neuf_fees = next(p["fees"] for p in result["profiles"] if p["profile"] == "NEUF")
        investor_fees = next(p["fees"] for p in result["profiles"] if p["profile"] == "INVESTOR")
        assert neuf_fees < investor_fees


class TestWaterfall:
    """Tests distribution Waterfall"""
    
    def test_waterfall_simple_below_hurdle(self):
        """Test waterfall simple sous hurdle"""
        result = waterfall_service.calculate_waterfall_simple(
            lp_investment=100000,
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
            lp_investment=100000,
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
            {"threshold": 0.08, "lp_split": 1.00, "gp_split": 0.00},
            {"threshold": 0.12, "lp_split": 0.80, "gp_split": 0.20},
            {"threshold": 0.18, "lp_split": 0.70, "gp_split": 0.30},
            {"threshold": float('inf'), "lp_split": 0.60, "gp_split": 0.40}
        ]
        
        result = waterfall_service.calculate_waterfall_advanced(
            lp_investment=100000,
            gp_investment=0,
            profit=25000,  # 25% IRR
            tiers=tiers
        )
        
        assert result["success"] is True
        assert len(result["tiers_breakdown"]) == 4
        
        # GP doit recevoir quelque chose (profit au-dessus 1er hurdle)
        assert result["gp_share"] > 0
        
        # Total doit être égal au profit
        assert result["lp_share"] + result["gp_share"] == pytest.approx(25000, abs=1)
    
    def test_waterfall_sensitivity(self):
        """Test analyse sensibilité waterfall"""
        result = waterfall_service.calculate_promote_sensitivity(
            lp_investment=100000,
            gp_investment=0,
            profit_range=(5000, 30000, 5000),
            hurdle_rate=0.08
        )
        
        assert result["success"] is True
        assert len(result["scenarios"]) > 0
        
        # À profit élevé, GP% doit augmenter
        first_scenario = result["scenarios"][0]
        last_scenario = result["scenarios"][-1]
        assert last_scenario["gp_percentage"] >= first_scenario["gp_percentage"]


class TestAssetManagement:
    """Tests gestion locative"""
    
    def test_rent_schedule_with_rent_free(self):
        """Test loyers avec franchise"""
        result = asset_management_service.calculate_rent_schedule_with_rent_free(
            monthly_rent=1000,
            rent_free_months=3,
            duration_years=5,
            indexation_type=IndexationType.NONE,
            indexation_rate=0.0
        )
        
        assert result["success"] is True
        
        # 3 premiers mois à 0
        assert result["schedule"][0]["rent"] == 0
        assert result["schedule"][1]["rent"] == 0
        assert result["schedule"][2]["rent"] == 0
        
        # 4ème mois : loyer normal
        assert result["schedule"][3]["rent"] == 1000
        
        # Total : (60 mois - 3 mois) * 1000 = 57000
        assert result["total_rent"] == 57000
    
    def test_rent_schedule_with_indexation_icc(self):
        """Test loyers avec indexation ICC"""
        result = asset_management_service.calculate_rent_schedule_with_rent_free(
            monthly_rent=1000,
            rent_free_months=0,
            duration_years=3,
            indexation_type=IndexationType.ICC,
            indexation_rate=0.02,
            indexation_start_year=1
        )
        
        assert result["success"] is True
        
        # Année 1 : pas d'indexation
        assert result["schedule"][0]["rent"] == 1000
        
        # Année 2 : indexation +2%
        assert result["schedule"][12]["rent"] == pytest.approx(1020, abs=1)
        
        # Année 3 : indexation cumulée
        assert result["schedule"][24]["rent"] == pytest.approx(1040.4, abs=1)
    
    def test_indexation_projection(self):
        """Test projection indexation scenarios"""
        result = asset_management_service.calculate_indexation_projection(
            base_rent=1000,
            duration_years=10,
            indexation_type=IndexationType.ILAT
        )
        
        assert result["success"] is True
        assert "pessimistic" in result["scenarios"]
        assert "base" in result["scenarios"]
        assert "optimistic" in result["scenarios"]
        
        # Pessimiste < Base < Optimiste
        pess_final = result["scenarios"]["pessimistic"]["years"][-1]["annual_rent"]
        base_final = result["scenarios"]["base"]["years"][-1]["annual_rent"]
        opt_final = result["scenarios"]["optimistic"]["years"][-1]["annual_rent"]
        
        assert pess_final < base_final < opt_final
    
    def test_rent_free_value(self):
        """Test valeur actualisée franchise"""
        result = asset_management_service.calculate_rent_free_value(
            monthly_rent=1000,
            rent_free_months=6,
            discount_rate=0.08
        )
        
        assert result["success"] is True
        assert result["total_rent_free"] == 6000
        assert result["npv_rent_free"] < 6000  # NPV < valeur nominale
        assert result["npv_rent_free"] > 5800  # Mais proche
    
    def test_optimize_tenant_improvements(self):
        """Test optimisation travaux locataire"""
        result = asset_management_service.optimize_tenant_improvements(
            ti_budget=20000,
            rent_increase=200,
            lease_duration_years=9
        )
        
        assert result["success"] is True
        assert result["total_rent_increase"] == 200 * 12 * 9  # 21600
        assert result["roi"] > 0
        assert result["payback_years"] > 0
        
        # ROI = (21600 - 20000) / 20000 = 8%
        assert result["roi"] == pytest.approx(0.08, abs=0.01)


# === RUN TESTS ===
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
