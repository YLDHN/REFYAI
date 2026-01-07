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


# ===== NOUVEAUX ENDPOINTS BP : FINANCEMENT INVERSÉ =====

from app.services.euribor_service import euribor_service
from app.services.financing_calculator import (
    calculate_financing_amount,
    calculate_equity_required,
    calculate_dscr,
    calculate_annual_debt_service,
    get_recommended_ltv,
    AmortizationType,
    StrategyType
)


class FinancingCalculationRequest(BaseModel):
    """Calcul financement depuis LTV (logique inversée BP)"""
    purchase_price: float
    ltv: float  # En pourcentage (ex: 70 pour 70%)
    strategy: str = "core"  # core, core_plus, value_add


class DSCRCalculationRequest(BaseModel):
    """Calcul DSCR pour projets Core"""
    noi: float  # Net Operating Income annuel
    loan_amount: float
    annual_interest_rate: float  # En décimal (ex: 0.035 pour 3.5%)
    duration_years: int
    amortization_type: str = "constant"


@router.get("/euribor-realtime")
async def get_euribor_realtime():
    """
    🆕 Récupération Euribor 1M en temps réel (BP)
    
    Returns:
        Taux Euribor actuel depuis source publique
    """
    euribor_data = euribor_service.get_euribor_1m()
    
    return {
        "success": True,
        "euribor": euribor_data
    }


@router.post("/calculate-financing")
async def calculate_financing(request: FinancingCalculationRequest):
    """
    🆕 Calcul financement depuis LTV (logique inversée BP)
    
    Entrée: LTV → Sortie: Montant financement
    
    Body:
        {
            "purchase_price": 1000000,
            "ltv": 70,
            "strategy": "core"
        }
    
    Returns:
        Montant financement, equity requis, LTV recommandée
    """
    # Calculs
    financing_amount = calculate_financing_amount(request.purchase_price, request.ltv)
    equity_required = calculate_equity_required(request.purchase_price, request.ltv)
    
    # Récupérer Euribor actuel
    euribor_data = euribor_service.get_euribor_1m()
    
    # Recommandation LTV selon stratégie
    strategy_enum = StrategyType(request.strategy)
    ltv_recommendation = get_recommended_ltv(strategy_enum, "standard")
    
    # Estimation marge bancaire (simplifiée)
    risk_margin = 1.5 if request.strategy == "core" else 2.0 if request.strategy == "core_plus" else 2.5
    estimated_rate = euribor_data["rate"] + risk_margin
    
    return {
        "success": True,
        "financing": {
            "purchase_price": request.purchase_price,
            "ltv_input": request.ltv,
            "financing_amount": round(financing_amount, 2),
            "equity_required": round(equity_required, 2),
            "ltv_percentage": request.ltv
        },
        "rate_estimate": {
            "euribor_1m": euribor_data["rate"],
            "risk_margin": risk_margin,
            "estimated_total_rate": round(estimated_rate, 2),
            "euribor_date": euribor_data["date"],
            "euribor_source": euribor_data["source"]
        },
        "ltv_recommendation": ltv_recommendation,
        "strategy": request.strategy
    }


@router.post("/calculate-dscr")
async def calculate_dscr_endpoint(request: DSCRCalculationRequest):
    """
    🆕 Calcul DSCR (Debt Service Coverage Ratio)
    
    Requis pour projets Core selon BP.
    
    Body:
        {
            "noi": 120000,
            "loan_amount": 800000,
            "annual_interest_rate": 0.04,
            "duration_years": 15,
            "amortization_type": "constant"
        }
    
    Returns:
        DSCR avec interprétation et statut
    """
    # Calculer service de la dette
    amortization = AmortizationType(request.amortization_type)
    debt_service_info = calculate_annual_debt_service(
        request.loan_amount,
        request.annual_interest_rate,
        request.duration_years,
        amortization
    )
    
    # Calculer DSCR
    dscr_result = calculate_dscr(
        request.noi,
        debt_service_info["annual_debt_service"]
    )
    
    return {
        "success": True,
        "dscr": dscr_result,
        "debt_service": debt_service_info,
        "inputs": {
            "noi": request.noi,
            "loan_amount": request.loan_amount,
            "annual_rate": request.annual_interest_rate,
            "duration_years": request.duration_years
        }
    }


@router.get("/amortization-types")
async def get_amortization_types():
    """
    🆕 Liste des types d'amortissement disponibles
    
    Returns:
        Types avec descriptions
    """
    return {
        "success": True,
        "amortization_types": [
            {
                "key": AmortizationType.CONSTANT.value,
                "label": "Amortissement constant",
                "description": "Mensualités constantes (amortissement français classique)"
            },
            {
                "key": AmortizationType.IN_FINE.value,
                "label": "In Fine",
                "description": "Remboursement du capital à la fin, intérêts périodiques"
            },
            {
                "key": AmortizationType.PROGRESSIF.value,
                "label": "Progressif",
                "description": "Mensualités croissantes dans le temps"
            },
            {
                "key": AmortizationType.DEGRESSIF.value,
                "label": "Dégressif",
                "description": "Mensualités décroissantes (amortissement constant du capital)"
            }
        ]
    }
