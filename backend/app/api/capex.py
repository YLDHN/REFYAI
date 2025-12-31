"""
Routes API pour le service CAPEX
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.capex_service import capex_service, CityTier

router = APIRouter(prefix="/capex", tags=["CAPEX"])


class CAPEXItemRequest(BaseModel):
    key: str
    quantity: float


class ProjectCAPEXRequest(BaseModel):
    items: List[CAPEXItemRequest]
    city_tier: int = CityTier.TIER_1
    contingency_rate: float = 0.10


class RenovationEstimateRequest(BaseModel):
    surface: float
    renovation_level: str  # "light", "medium", "heavy", "complete"
    city_tier: int = CityTier.TIER_1


@router.get("/categories")
async def get_capex_categories():
    """
    Obtenir toutes les catégories et postes CAPEX disponibles
    
    Returns:
        Dict des catégories avec leurs postes
    """
    categories = capex_service.get_all_categories()
    
    return {
        "success": True,
        "categories": categories,
        "total_categories": len(categories),
        "total_items": sum(len(items) for items in categories.values())
    }


@router.post("/estimate")
async def estimate_single_item(
    item_key: str,
    quantity: float,
    city_tier: int = CityTier.TIER_1
):
    """
    Estimer le coût d'un poste unique
    
    Args:
        item_key: Clé du poste (ex: "facade_ravalement_simple")
        quantity: Quantité (m2, ml, unités)
        city_tier: Niveau ville (1, 2, 3)
    
    Returns:
        Estimation min/avg/max
    """
    estimate = capex_service.get_cost_estimate(item_key, quantity, city_tier)
    
    if "error" in estimate:
        raise HTTPException(status_code=404, detail=estimate["error"])
    
    return {
        "success": True,
        "estimate": estimate
    }


@router.post("/project")
async def calculate_project_capex(request: ProjectCAPEXRequest):
    """
    Calculer le CAPEX total d'un projet
    
    Body:
        {
            "items": [{"key": "facade_ravalement_simple", "quantity": 100}],
            "city_tier": 1,
            "contingency_rate": 0.10
        }
    
    Returns:
        CAPEX total avec détails par poste
    """
    items = [{"key": item.key, "quantity": item.quantity} for item in request.items]
    
    result = capex_service.calculate_project_capex(
        items,
        request.city_tier,
        request.contingency_rate
    )
    
    return {
        "success": True,
        **result
    }


@router.post("/renovation-estimate")
async def estimate_renovation_budget(request: RenovationEstimateRequest):
    """
    Estimation rapide budget rénovation au m2
    
    Body:
        {
            "surface": 100,
            "renovation_level": "medium",
            "city_tier": 1
        }
    
    Returns:
        Budget estimé avec description
    """
    result = capex_service.estimate_renovation_budget(
        request.surface,
        request.renovation_level,
        request.city_tier
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {
        "success": True,
        **result
    }


@router.get("/city-tiers")
async def get_city_tiers():
    """
    Obtenir les tiers de villes et leurs multiplicateurs
    
    Returns:
        Liste des tiers avec explications
    """
    return {
        "success": True,
        "tiers": [
            {
                "tier": CityTier.TIER_1,
                "name": "Tier 1 - Métropoles",
                "multiplier": 1.0,
                "cities": ["Paris", "Lyon", "Marseille", "Bordeaux"],
                "description": "Coûts de référence (100%)"
            },
            {
                "tier": CityTier.TIER_2,
                "name": "Tier 2 - Grandes villes",
                "multiplier": 0.85,
                "cities": ["Nantes", "Toulouse", "Nice", "Strasbourg"],
                "description": "Coûts réduits de 15%"
            },
            {
                "tier": CityTier.TIER_3,
                "name": "Tier 3 - Province",
                "multiplier": 0.70,
                "cities": ["Villes moyennes et petites"],
                "description": "Coûts réduits de 30%"
            }
        ]
    }
