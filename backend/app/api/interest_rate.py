"""
Routes API pour le calcul des taux d'intérêt
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.services.interest_rate_service import InterestRateService, LoanStructuringService

router = APIRouter(prefix="/interest-rate", tags=["interest-rate"])

rate_service = InterestRateService()
loan_service = LoanStructuringService()


class RateCalculationRequest(BaseModel):
    """Requête de calcul de taux"""
    project_data: Dict[str, Any]
    company_data: Dict[str, Any]
    loan_duration_months: int = 24


class LoanStructureRequest(BaseModel):
    """Requête d'optimisation de structure"""
    project_data: Dict[str, Any]
    company_data: Dict[str, Any]
    target_ltv: float = 0.75


@router.get("/euribor")
async def get_current_euribor(maturity: str = "12m"):
    """
    Récupère le taux Euribor actuel
    
    Args:
        maturity: "3m" ou "12m"
    
    Returns:
        Taux Euribor en vigueur
    """
    euribor = await rate_service.get_current_euribor(maturity)
    
    return {
        "euribor": euribor,
        "maturity": maturity,
        "date": "2025-12-31",
        "source": "European Central Bank (ECB)"
    }


@router.post("/calculate")
async def calculate_interest_rate(request: RateCalculationRequest):
    """
    Calcule le taux d'intérêt personnalisé avec algorithme de risque
    
    Returns:
        Taux final (Euribor + Marge selon risque)
    """
    rate_info = await rate_service.calculate_interest_rate(
        project_data=request.project_data,
        company_data=request.company_data,
        loan_duration_months=request.loan_duration_months
    )
    
    return {
        "rate_info": rate_info,
        "explanation": {
            "formula": "Taux Final = Euribor + Marge Risque",
            "euribor": f"{rate_info['euribor_base']}%",
            "marge": f"{rate_info['adjusted_margin']}%",
            "total": f"{rate_info['final_rate']}%"
        }
    }


@router.post("/risk-score")
async def calculate_risk_score(request: RateCalculationRequest):
    """
    Calcule uniquement le score de risque du projet
    
    Returns:
        Score de 0 à 100 avec détail des facteurs
    """
    risk_score = rate_service.calculate_risk_score(
        project_data=request.project_data,
        company_data=request.company_data
    )
    
    return {
        "risk_score": risk_score,
        "rating": risk_score["category"],
        "interpretation": risk_score["interpretation"]
    }


@router.post("/optimize-structure")
async def optimize_loan_structure(request: LoanStructureRequest):
    """
    Optimise la structure de financement Dette/Equity
    
    Returns:
        Structure optimale avec taux et mensualités
    """
    optimal_structure = await loan_service.optimize_loan_structure(
        project_data=request.project_data,
        company_data=request.company_data,
        target_ltv=request.target_ltv
    )
    
    return {
        "optimal_structure": optimal_structure,
        "summary": {
            "total_cost": optimal_structure["total_cost"],
            "debt": optimal_structure["optimal_debt"],
            "equity": optimal_structure["optimal_equity"],
            "rate": f"{optimal_structure['interest_rate']['final_rate']}%",
            "monthly_payment": optimal_structure["monthly_payment"]
        }
    }


@router.get("/margins")
async def get_margin_info():
    """
    Retourne les marges de base par profil
    
    Returns:
        Grille des marges selon profil de risque
    """
    return {
        "base_margins": rate_service.BASE_MARGIN,
        "adjustments": {
            "tri_bonus": "-0.20% si TRI > 15%",
            "ltv_penalty": "+0.30% si LTV > 80%",
            "fidelity_bonus": "-0.15% si client existant",
            "guarantee_bonus": "-0.25% si garanties supplémentaires"
        },
        "range": "3.0% - 8.0%",
        "note": "Taux final plafonné entre 3% et 8%"
    }
