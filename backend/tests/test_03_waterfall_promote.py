"""
TEST SECTION 3: MOTEUR FINANCIER AVANCÉ (WATERFALL / PROMOTE)
Tests de la distribution selon logique fonds PE/VC
"""
import pytest
from app.services.financial_service import financial_service


class TestWaterfallBasique:
    """Test waterfall à paliers"""
    
    def test_100_percent_investisseur_si_sous_hurdle(self):
        """Tant que le hurdle rate n'est pas atteint, 100% à l'investisseur"""
        result = financial_service.calculate_waterfall(
            total_proceeds=1_200_000,
            initial_investment=1_000_000,
            hurdle_rate=0.15,  # 15% TRI attendu
            promote_percentage=0.20,  # 20% de promote au-delà
            investment_duration_years=3
        )
        
        # TRI = 6.27% < 15% hurdle
        assert result["irr"] < 0.15
        
        # L'investisseur récupère tout
        assert result["investor_distribution"] == 1_200_000
        assert result["sponsor_distribution"] == 0
        assert result["sponsor_promote"] == 0
    
    def test_partage_si_depasse_hurdle(self):
        """Au-delà du hurdle, distribution selon promote"""
        result = financial_service.calculate_waterfall(
            total_proceeds=2_000_000,
            initial_investment=1_000_000,
            hurdle_rate=0.15,
            promote_percentage=0.20,
            investment_duration_years=3
        )
        
        # TRI = 26% > 15% hurdle
        assert result["irr"] > 0.15
        
        # L'investisseur récupère son capital + hurdle
        hurdle_amount = 1_000_000 * (1.15 ** 3)  # ~1_520_875
        
        # Le surplus est partagé
        surplus = 2_000_000 - hurdle_amount
        expected_sponsor = surplus * 0.20
        expected_investor = hurdle_amount + (surplus * 0.80)
        
        assert abs(result["sponsor_distribution"] - expected_sponsor) < 1000
        assert abs(result["investor_distribution"] - expected_investor) < 1000


class TestPromote:
    """Test du promote sponsor"""
    
    def test_sponsor_ne_touche_rien_sous_hurdle(self):
        """Si TRI < hurdle, sponsor = 0€"""
        result = financial_service.calculate_waterfall(
            total_proceeds=1_050_000,
            initial_investment=1_000_000,
            hurdle_rate=0.10,
            promote_percentage=0.25,
            investment_duration_years=1
        )
        
        # TRI = 5% < 10% hurdle
        assert result["sponsor_promote"] == 0
        assert result["sponsor_distribution"] == 0
    
    def test_promote_proportionnel_au_surplus(self):
        """Le promote est proportionnel au surplus au-delà du hurdle"""
        result = financial_service.calculate_waterfall(
            total_proceeds=2_500_000,
            initial_investment=1_000_000,
            hurdle_rate=0.20,
            promote_percentage=0.30,  # 30% de promote
            investment_duration_years=3
        )
        
        # Calcul manuel du surplus
        hurdle_amount = 1_000_000 * (1.20 ** 3)  # ~1_728_000
        surplus = 2_500_000 - hurdle_amount  # ~772_000
        expected_promote = surplus * 0.30  # ~231_600
        
        assert abs(result["sponsor_promote"] - expected_promote) < 1000
    
    def test_promote_different_selon_palier(self):
        """Le promote peut avoir plusieurs paliers"""
        result = financial_service.calculate_waterfall_multi_tier(
            total_proceeds=3_000_000,
            initial_investment=1_000_000,
            hurdle_tiers=[
                {"threshold_irr": 0.10, "promote": 0.10},  # 10% TRI → 10% promote
                {"threshold_irr": 0.20, "promote": 0.20},  # 20% TRI → 20% promote
                {"threshold_irr": 0.30, "promote": 0.30},  # 30% TRI → 30% promote
            ],
            investment_duration_years=3
        )
        
        # TRI élevé → promote élevé
        assert result["irr"] > 0.30
        assert result["sponsor_promote"] > 0
        assert result["effective_promote_rate"] >= 0.30


class TestCoherenceFinanciere:
    """Test cohérence des calculs financiers"""
    
    def test_somme_distributions_egale_proceeds(self):
        """Sponsor + Investisseur = Total Proceeds"""
        result = financial_service.calculate_waterfall(
            total_proceeds=1_800_000,
            initial_investment=1_000_000,
            hurdle_rate=0.12,
            promote_percentage=0.20,
            investment_duration_years=4
        )
        
        total_distributed = (
            result["investor_distribution"] +
            result["sponsor_distribution"]
        )
        
        assert abs(total_distributed - 1_800_000) < 10  # Tolérance arrondi
    
    def test_investisseur_recupere_toujours_capital(self):
        """L'investisseur doit toujours récupérer au moins son capital"""
        result = financial_service.calculate_waterfall(
            total_proceeds=1_200_000,
            initial_investment=1_000_000,
            hurdle_rate=0.15,
            promote_percentage=0.25,
            investment_duration_years=2
        )
        
        assert result["investor_distribution"] >= 1_000_000
    
    def test_conformite_standards_pe(self):
        """Résultats cohérents avec standards Private Equity"""
        result = financial_service.calculate_waterfall(
            total_proceeds=2_000_000,
            initial_investment=1_000_000,
            hurdle_rate=0.08,  # 8% hurdle classique
            promote_percentage=0.20,  # 80/20 split classique
            investment_duration_years=5
        )
        
        # Vérifications standards PE
        assert result["irr"] > 0
        assert 0 <= result["effective_promote_rate"] <= 1
        assert result["multiple_on_invested_capital"] == 2.0


class TestCasLimites:
    """Test des cas limites"""
    
    def test_perte_totale(self):
        """Si perte, l'investisseur perd et le sponsor ne touche rien"""
        result = financial_service.calculate_waterfall(
            total_proceeds=500_000,
            initial_investment=1_000_000,
            hurdle_rate=0.10,
            promote_percentage=0.20,
            investment_duration_years=3
        )
        
        assert result["irr"] < 0  # TRI négatif
        assert result["sponsor_promote"] == 0
        assert result["investor_distribution"] == 500_000
    
    def test_hurdle_zero(self):
        """Si hurdle = 0%, promote dès le premier euro de gain"""
        result = financial_service.calculate_waterfall(
            total_proceeds=1_100_000,
            initial_investment=1_000_000,
            hurdle_rate=0.0,
            promote_percentage=0.20,
            investment_duration_years=1
        )
        
        surplus = 100_000
        expected_promote = surplus * 0.20
        
        assert abs(result["sponsor_promote"] - expected_promote) < 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
