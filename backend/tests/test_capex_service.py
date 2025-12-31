"""
Tests unitaires pour le service CAPEX
"""
import pytest
from app.services.capex_service import CAPEXService, CityTier


@pytest.fixture
def capex_service():
    return CAPEXService()


def test_get_cost_estimate_simple(capex_service):
    """Test estimation coût simple"""
    result = capex_service.get_cost_estimate(
        "facade_ravalement_simple",
        100,  # 100 m²
        CityTier.TIER_1
    )
    
    assert "error" not in result
    assert result["item"] == "facade_ravalement_simple"
    assert result["unit"] == "m2"
    assert result["quantity"] == 100
    assert result["city_tier"] == CityTier.TIER_1
    assert "unit_prices" in result
    assert "total_costs" in result
    assert result["total_costs"]["avg"] > 0


def test_get_cost_estimate_with_tier_adjustment(capex_service):
    """Test ajustement coût selon tier ville"""
    # Tier 1 (référence)
    result_tier1 = capex_service.get_cost_estimate(
        "facade_ravalement_simple",
        100,
        CityTier.TIER_1
    )
    
    # Tier 3 (Province, -30%)
    result_tier3 = capex_service.get_cost_estimate(
        "facade_ravalement_simple",
        100,
        CityTier.TIER_3
    )
    
    assert result_tier3["total_costs"]["avg"] < result_tier1["total_costs"]["avg"]
    # Vérifier ratio environ 0.7
    ratio = result_tier3["total_costs"]["avg"] / result_tier1["total_costs"]["avg"]
    assert 0.68 < ratio < 0.72


def test_get_cost_estimate_invalid_item(capex_service):
    """Test item invalide"""
    result = capex_service.get_cost_estimate(
        "item_inexistant",
        100,
        CityTier.TIER_1
    )
    
    assert "error" in result
    assert "available_items" in result


def test_calculate_project_capex(capex_service):
    """Test calcul CAPEX projet complet"""
    items = [
        {"key": "facade_ravalement_simple", "quantity": 100},
        {"key": "toiture_refection_complete", "quantity": 80},
        {"key": "electricite_renovation_complete", "quantity": 120}
    ]
    
    result = capex_service.calculate_project_capex(
        items,
        CityTier.TIER_1,
        contingency_rate=0.10
    )
    
    assert "project_capex" in result
    assert "items_detail" in result
    assert "summary" in result
    
    capex = result["project_capex"]
    assert "base_costs" in capex
    assert "contingency" in capex
    assert "total_with_contingency" in capex
    
    # Vérifier que total = base + contingency
    assert capex["total_with_contingency"]["avg"] == \
           capex["base_costs"]["avg"] + capex["contingency"]["amount_avg"]
    
    # Vérifier 3 items
    assert len(result["items_detail"]) == 3


def test_calculate_project_capex_with_contingency(capex_service):
    """Test calcul avec aléas"""
    items = [{"key": "facade_ravalement_simple", "quantity": 100}]
    
    # Avec 10% aléas
    result_10 = capex_service.calculate_project_capex(items, CityTier.TIER_1, 0.10)
    
    # Avec 20% aléas
    result_20 = capex_service.calculate_project_capex(items, CityTier.TIER_1, 0.20)
    
    base_cost = result_10["project_capex"]["base_costs"]["avg"]
    contingency_10 = result_10["project_capex"]["contingency"]["amount_avg"]
    contingency_20 = result_20["project_capex"]["contingency"]["amount_avg"]
    
    assert contingency_10 == base_cost * 0.10
    assert contingency_20 == base_cost * 0.20
    assert contingency_20 > contingency_10


def test_estimate_renovation_budget(capex_service):
    """Test estimation budget rénovation"""
    result = capex_service.estimate_renovation_budget(
        surface=100,
        renovation_level="medium",
        city_tier=CityTier.TIER_1
    )
    
    assert "error" not in result
    assert result["renovation_level"] == "medium"
    assert result["surface_m2"] == 100
    assert "cost_per_m2" in result
    assert "total_budget" in result
    assert "description" in result
    
    # Vérifier cohérence total = surface × coût/m²
    assert result["total_budget"]["avg"] == \
           result["cost_per_m2"]["avg"] * 100


def test_estimate_renovation_budget_levels(capex_service):
    """Test différents niveaux de rénovation"""
    surface = 100
    
    light = capex_service.estimate_renovation_budget(surface, "light", CityTier.TIER_1)
    medium = capex_service.estimate_renovation_budget(surface, "medium", CityTier.TIER_1)
    heavy = capex_service.estimate_renovation_budget(surface, "heavy", CityTier.TIER_1)
    complete = capex_service.estimate_renovation_budget(surface, "complete", CityTier.TIER_1)
    
    # Vérifier ordre croissant
    assert light["total_budget"]["avg"] < medium["total_budget"]["avg"]
    assert medium["total_budget"]["avg"] < heavy["total_budget"]["avg"]
    assert heavy["total_budget"]["avg"] < complete["total_budget"]["avg"]


def test_estimate_renovation_budget_invalid_level(capex_service):
    """Test niveau rénovation invalide"""
    result = capex_service.estimate_renovation_budget(
        surface=100,
        renovation_level="invalid",
        city_tier=CityTier.TIER_1
    )
    
    assert "error" in result


def test_get_all_categories(capex_service):
    """Test récupération catégories"""
    categories = capex_service.get_all_categories()
    
    assert isinstance(categories, dict)
    assert len(categories) > 0
    
    # Vérifier présence catégories principales
    assert "facade" in categories
    assert "toiture" in categories
    assert "electricite" in categories
    
    # Vérifier structure
    for category, items in categories.items():
        assert isinstance(items, list)
        assert len(items) > 0


def test_tier_multiplier_values(capex_service):
    """Test valeurs multiplicateurs tier"""
    assert capex_service._get_tier_multiplier(CityTier.TIER_1) == 1.0
    assert capex_service._get_tier_multiplier(CityTier.TIER_2) == 0.85
    assert capex_service._get_tier_multiplier(CityTier.TIER_3) == 0.70


def test_pmr_costs(capex_service):
    """Test coûts PMR (accessibilité)"""
    result = capex_service.get_cost_estimate(
        "pmr_rampe_acces",
        1,  # 1 unité
        CityTier.TIER_1
    )
    
    assert "error" not in result
    assert result["unit"] == "unite"
    assert result["total_costs"]["min"] >= 2000
    assert result["total_costs"]["max"] <= 8000


def test_security_costs(capex_service):
    """Test coûts sécurité incendie"""
    items = [
        {"key": "securite_detecteurs", "quantity": 10},
        {"key": "securite_porte_coupe_feu", "quantity": 3},
        {"key": "securite_extinction", "quantity": 100}
    ]
    
    result = capex_service.calculate_project_capex(items, CityTier.TIER_1)
    
    assert len(result["items_detail"]) == 3
    assert result["project_capex"]["base_costs"]["avg"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
