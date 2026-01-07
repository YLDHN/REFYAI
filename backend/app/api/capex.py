"""
Routes API pour le service CAPEX
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.capex_service import capex_service, CityTier
from app.services.capex_ai_service import capex_ai_service

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
    # Validation de la quantité
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="La quantité doit être supérieure à zéro")
    
    # Validation du city_tier
    if city_tier not in [CityTier.TIER_1, CityTier.TIER_2, CityTier.TIER_3]:
        raise HTTPException(status_code=400, detail=f"City tier invalide. Valeurs acceptées: 1, 2, 3")
    
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


# === NOUVEAU : ENDPOINT IA ===

class CAPEXAISuggestRequest(BaseModel):
    project_description: str
    surface: float
    typologie: str  # NEUF, RENOVATION, CONVERSION, etc.
    city_tier: int = 1


@router.post("/suggest")
async def suggest_capex_with_ai(request: CAPEXAISuggestRequest):
    """
    🤖 NOUVEAU : Suggestions CAPEX intelligentes avec IA
    
    Utilise:
    - LangChain + GPT-4 pour analyse projet
    - ChromaDB RAG pour projets similaires historiques
    - Base de données CAPEX pour coûts réels
    
    Body:
        {
            "project_description": "Réhabilitation immeuble 1900 avec 8 appartements, façade à refaire",
            "surface": 800,
            "typologie": "RENOVATION",
            "city_tier": 1
        }
    
    Returns:
        Suggestions détaillées avec postes + quantités + estimations
    """
    result = await capex_ai_service.suggest_capex_with_ai(
        project_description=request.project_description,
        surface=request.surface,
        typologie=request.typologie,
        city_tier=request.city_tier
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Erreur IA")
        )
    
    return result


# ===== TYPOLOGIE BP : HABITATION / BUREAUX / COMMERCE =====

from app.services.capex_typologie_service import (
    get_typologie_template,
    estimate_capex_by_typologie,
    CAPEXTypology
)


class TypologieEstimateRequest(BaseModel):
    typologie: str  # "habitation", "bureaux", "commerce"
    surface: float
    city_tier: int = 1
    construction_year: int = 2000
    project_description: str = ""


@router.get("/typologies")
async def get_available_typologies():
    """
    Obtenir les 3 typologies disponibles selon Business Plan
    
    Returns:
        Liste des typologies avec description
    """
    return {
        "success": True,
        "typologies": [
            {
                "key": CAPEXTypology.HABITATION,
                "label": "Habitation",
                "description": "Focus : Aménagement résidentiel (appartements, maisons)",
                "icon": "🏠"
            },
            {
                "key": CAPEXTypology.BUREAUX,
                "label": "Bureaux",
                "description": "Focus : Tertiaire avec normes ERP et accessibilité PMR",
                "icon": "🏢"
            },
            {
                "key": CAPEXTypology.COMMERCE,
                "label": "Commerce",
                "description": "Focus : Visibilité, normes ERP (flux de public) et extraction technique",
                "icon": "🛍️"
            }
        ]
    }


@router.get("/typologies/{typologie}/template")
async def get_typologie_capex_template(typologie: str):
    """
    Obtenir le template CAPEX pour une typologie spécifique
    
    Args:
        typologie: "habitation", "bureaux", ou "commerce"
    
    Returns:
        Liste complète des postes CAPEX pour cette typologie
    """
    if typologie.lower() not in [CAPEXTypology.HABITATION, CAPEXTypology.BUREAUX, CAPEXTypology.COMMERCE]:
        raise HTTPException(
            status_code=400,
            detail=f"Typologie invalide. Valeurs acceptées: habitation, bureaux, commerce"
        )
    
    template = get_typologie_template(typologie)
    
    return {
        "success": True,
        "typologie": typologie,
        "template": template,
        "total_items": len(template),
        "format_note": "Format liste (sans astérisques) selon Business Plan"
    }


@router.post("/typologies/estimate")
async def estimate_by_typologie(request: TypologieEstimateRequest):
    """
    🤖 Estimation CAPEX automatique selon typologie BP
    
    L'IA estime directement les coûts sans saisie manuelle.
    
    Body:
        {
            "typologie": "habitation",
            "surface": 800,
            "city_tier": 1,
            "construction_year": 1990,
            "project_description": "Immeuble haussmannien 8 appartements"
        }
    
    Returns:
        Estimation complète avec tous les postes de la typologie
    """
    result = estimate_capex_by_typologie(
        typologie=request.typologie,
        surface=request.surface,
        city_tier=request.city_tier,
        construction_year=request.construction_year,
        project_description=request.project_description
    )
    
    return {
        "success": True,
        **result
    }
