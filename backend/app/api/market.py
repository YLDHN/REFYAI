"""
Routes API pour l'analyse de marché (DVF et comparables)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.services.dvf_service import DVFService, MarketAnalysisService

router = APIRouter(prefix="/market", tags=["market"])

dvf_service = DVFService()
market_service = MarketAnalysisService()


class MarketAnalysisRequest(BaseModel):
    """Requête d'analyse de marché"""
    commune: str
    address: Optional[str] = ""
    surface: float
    type_bien: str = "appartement"
    purchase_price: Optional[float] = 0


@router.post("/analyze")
async def analyze_market(request: MarketAnalysisRequest):
    """
    Analyse complète du marché immobilier local
    
    Returns:
        Valeur de marché, tendances, comparables et recommandations
    """
    project_data = {
        "commune": request.commune,
        "address": request.address,
        "surface": request.surface,
        "type_bien": request.type_bien,
        "purchase_price": request.purchase_price
    }
    
    analysis = await market_service.full_market_analysis(project_data)
    
    return {
        "analysis": analysis,
        "timestamp": "2025-12-31",
        "data_source": "DVF (Demandes de Valeurs Foncières) - data.gouv.fr"
    }


@router.get("/comparables/{commune}")
async def get_comparables(
    commune: str,
    type_local: str = "Appartement",
    months_back: int = 24
):
    """
    Récupère les ventes comparables DVF
    
    Args:
        commune: Code INSEE ou nom de la commune
        type_local: Maison, Appartement, Local commercial, etc.
        months_back: Nombre de mois en arrière
    
    Returns:
        Liste des transactions comparables
    """
    comparables = await dvf_service.get_comparable_sales(
        commune=commune,
        type_local=type_local,
        months_back=months_back
    )
    
    return {
        "comparables": comparables[:50],  # Limiter à 50
        "total_found": len(comparables),
        "commune": commune,
        "type_local": type_local,
        "period": f"{months_back} derniers mois"
    }


@router.get("/trend/{commune}")
async def get_market_trend(commune: str, type_bien: str = "appartement"):
    """
    Analyse la tendance du marché immobilier
    
    Returns:
        Évolution des prix sur 12 mois
    """
    trend = await dvf_service.analyze_market_trend(
        commune=commune,
        type_bien=type_bien
    )
    
    return {
        "trend": trend,
        "commune": commune,
        "type_bien": type_bien
    }


@router.post("/valuation")
async def calculate_valuation(request: MarketAnalysisRequest):
    """
    Calcule la valeur de marché d'un bien
    
    Returns:
        Estimation avec fourchette basse/haute
    """
    valuation = await dvf_service.calculate_market_value(
        address=request.address,
        surface=request.surface,
        commune=request.commune,
        type_bien=request.type_bien
    )
    
    return {
        "valuation": valuation,
        "input": {
            "commune": request.commune,
            "surface": request.surface,
            "type": request.type_bien
        }
    }
