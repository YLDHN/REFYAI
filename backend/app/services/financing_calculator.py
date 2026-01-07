"""
Service de calcul financement avec logique inversée (LTV → Montant)
et calcul DSCR pour projets Core.
"""
from typing import Dict, Optional
from enum import Enum


class AmortizationType(str, Enum):
    """Types d'amortissement de prêt"""
    CONSTANT = "constant"  # Mensualités constantes
    IN_FINE = "in_fine"    # Remboursement capital à la fin
    PROGRESSIF = "progressif"  # Mensualités progressives
    DEGRESSIF = "degressif"    # Mensualités dégressives


class StrategyType(str, Enum):
    """Stratégies d'investissement"""
    CORE = "core"
    CORE_PLUS = "core_plus"
    VALUE_ADD = "value_add"


def calculate_financing_amount(purchase_price: float, ltv: float) -> float:
    """
    Calcul du montant de financement depuis la LTV (calcul inversé)
    
    Args:
        purchase_price: Prix d'acquisition
        ltv: Loan-to-Value en pourcentage (ex: 70 pour 70%)
    
    Returns:
        Montant du financement
    """
    if ltv < 0 or ltv > 100:
        raise ValueError("LTV doit être entre 0 et 100")
    
    return purchase_price * (ltv / 100.0)


def calculate_equity_required(purchase_price: float, ltv: float) -> float:
    """
    Calcul des fonds propres requis
    
    Args:
        purchase_price: Prix d'acquisition
        ltv: Loan-to-Value en pourcentage
    
    Returns:
        Montant fonds propres requis
    """
    financing = calculate_financing_amount(purchase_price, ltv)
    return purchase_price - financing


def calculate_dscr(noi: float, annual_debt_service: float) -> Dict:
    """
    Calcul du DSCR (Debt Service Coverage Ratio)
    
    Formule: DSCR = NOI / Service de la dette annuel
    
    Args:
        noi: Net Operating Income (NOI) annuel
        annual_debt_service: Service de la dette annuel (capital + intérêts)
    
    Returns:
        Dict avec DSCR et interprétation
    """
    if annual_debt_service <= 0:
        return {
            "dscr": None,
            "status": "ERROR",
            "message": "Service de la dette invalide"
        }
    
    dscr = noi / annual_debt_service
    
    # Interprétation selon standards
    if dscr < 1.0:
        status = "INSUFFICIENT"
        message = "Le NOI ne couvre pas le service de la dette (risque élevé)"
        color = "red"
    elif dscr < 1.2:
        status = "WEAK"
        message = "Couverture faible (minimum bancaire généralement 1.2x)"
        color = "orange"
    elif dscr < 1.4:
        status = "ACCEPTABLE"
        message = "Couverture acceptable pour projets Core"
        color = "yellow"
    else:
        status = "STRONG"
        message = "Excellente couverture de la dette"
        color = "green"
    
    return {
        "dscr": round(dscr, 2),
        "dscr_formatted": f"{dscr:.2f}x",
        "status": status,
        "message": message,
        "color": color,
        "noi": noi,
        "annual_debt_service": annual_debt_service
    }


def calculate_annual_debt_service(
    loan_amount: float,
    annual_interest_rate: float,
    duration_years: int,
    amortization_type: AmortizationType = AmortizationType.CONSTANT
) -> Dict:
    """
    Calcul du service de la dette annuel selon type d'amortissement
    
    Args:
        loan_amount: Montant du prêt
        annual_interest_rate: Taux d'intérêt annuel (ex: 0.035 pour 3.5%)
        duration_years: Durée en années
        amortization_type: Type d'amortissement
    
    Returns:
        Dict avec service de la dette et détails
    """
    monthly_rate = annual_interest_rate / 12
    n_payments = duration_years * 12
    
    if amortization_type == AmortizationType.CONSTANT:
        # Mensualité constante (amortissement français)
        if monthly_rate == 0:
            monthly_payment = loan_amount / n_payments
        else:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
        
        annual_payment = monthly_payment * 12
        total_interest = (monthly_payment * n_payments) - loan_amount
        
    elif amortization_type == AmortizationType.IN_FINE:
        # Remboursement capital à la fin
        annual_interest = loan_amount * annual_interest_rate
        annual_payment = annual_interest  # Pendant la durée
        # À la dernière année: annual_payment + loan_amount
        total_interest = loan_amount * annual_interest_rate * duration_years
        
    elif amortization_type == AmortizationType.PROGRESSIF:
        # Simplification: utiliser constant pour l'instant
        # TODO: Implémenter progression réelle
        return calculate_annual_debt_service(
            loan_amount, annual_interest_rate, duration_years, AmortizationType.CONSTANT
        )
    
    else:  # DEGRESSIF
        # Amortissement constant du capital
        capital_per_month = loan_amount / n_payments
        # Première mensualité (la plus élevée)
        first_monthly_payment = capital_per_month + (loan_amount * monthly_rate)
        # Moyenne approximative pour l'année
        annual_payment = first_monthly_payment * 12 * 0.8  # Approximation
        total_interest = loan_amount * annual_interest_rate * duration_years * 0.5  # Approximation
    
    return {
        "annual_debt_service": round(annual_payment, 2),
        "monthly_payment": round(annual_payment / 12, 2),
        "total_interest": round(total_interest, 2),
        "total_cost": round(loan_amount + total_interest, 2),
        "amortization_type": amortization_type.value
    }


def get_recommended_ltv(strategy: StrategyType, asset_quality: str = "standard") -> Dict:
    """
    Recommandation LTV selon stratégie et qualité de l'actif
    
    Args:
        strategy: Stratégie d'investissement
        asset_quality: "prime", "standard", "secondary"
    
    Returns:
        Dict avec LTV recommandée et DSCR minimum
    """
    recommendations = {
        StrategyType.CORE: {
            "prime": {"ltv": 70, "dscr_min": 1.3, "description": "Actif Core Prime"},
            "standard": {"ltv": 65, "dscr_min": 1.4, "description": "Actif Core Standard"},
            "secondary": {"ltv": 60, "dscr_min": 1.5, "description": "Actif Core Secondaire"}
        },
        StrategyType.CORE_PLUS: {
            "prime": {"ltv": 65, "dscr_min": 1.2, "description": "Actif Core+ Prime"},
            "standard": {"ltv": 60, "dscr_min": 1.3, "description": "Actif Core+ Standard"},
            "secondary": {"ltv": 55, "dscr_min": 1.4, "description": "Actif Core+ Secondaire"}
        },
        StrategyType.VALUE_ADD: {
            "prime": {"ltv": 60, "dscr_min": 1.1, "description": "Value Add Prime"},
            "standard": {"ltv": 55, "dscr_min": 1.2, "description": "Value Add Standard"},
            "secondary": {"ltv": 50, "dscr_min": 1.3, "description": "Value Add Secondaire"}
        }
    }
    
    rec = recommendations.get(strategy, {}).get(asset_quality, recommendations[StrategyType.CORE]["standard"])
    
    return {
        "recommended_ltv": rec["ltv"],
        "ltv_range": {"min": rec["ltv"] - 5, "max": rec["ltv"] + 5},
        "dscr_minimum": rec["dscr_min"],
        "description": rec["description"],
        "strategy": strategy.value,
        "asset_quality": asset_quality
    }
