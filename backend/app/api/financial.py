from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.services import financial_service
from app.services.notary_fee_service import notary_fee_service
from app.services.waterfall_service import waterfall_service
from typing import List, Optional, Dict, Any

router = APIRouter(prefix="/financial", tags=["financial"])

class FinancialInput(BaseModel):
    purchase_price: float
    renovation_budget: float
    notary_fees: float
    loan_amount: float
    interest_rate: float
    loan_duration: int
    monthly_rent: float = 0
    resale_price: float = 0
    project_type: str = "rental"  # rental ou resale

class FinancialAnalysisResponse(BaseModel):
    total_cost: float
    equity: float
    loan_amount: float
    monthly_payment: float
    annual_debt_service: float
    annual_rent: float
    tri: float
    van: float
    ltv: float
    ltc: float
    dscr: float
    roi: float
    cash_flows: List[float]

@router.post("/analyze", response_model=FinancialAnalysisResponse)
async def calculate_financial_analysis(data: FinancialInput):
    """Calculer une analyse financière complète"""
    
    try:
        analysis = financial_service.calculate_full_analysis(
            purchase_price=data.purchase_price,
            renovation_budget=data.renovation_budget,
            notary_fees=data.notary_fees,
            loan_amount=data.loan_amount,
            interest_rate=data.interest_rate,
            loan_duration=data.loan_duration,
            monthly_rent=data.monthly_rent,
            resale_price=data.resale_price,
            project_type=data.project_type
        )
        
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du calcul: {str(e)}"
        )

@router.post("/tri")
async def calculate_tri(
    initial_investment: float,
    cash_flows: List[float]
):
    """Calculer le TRI (Taux de Rendement Interne)"""
    
    tri = financial_service.calculate_tri(
        initial_investment=initial_investment,
        cash_flows=cash_flows
    )
    
    return {"tri": tri, "tri_percentage": f"{tri * 100:.2f}%"}

@router.post("/ltv")
async def calculate_ltv(
    loan_amount: float,
    property_value: float
):
    """Calculer le LTV (Loan to Value)"""
    
    ltv = financial_service.calculate_ltv(
        loan_amount=loan_amount,
        property_value=property_value
    )
    
    return {"ltv": ltv, "ltv_percentage": f"{ltv * 100:.2f}%"}

@router.post("/dscr")
async def calculate_dscr(
    net_operating_income: float,
    debt_service: float
):
    """Calculer le DSCR (Debt Service Coverage Ratio)"""
    
    dscr = financial_service.calculate_dscr(
        net_operating_income=net_operating_income,
        debt_service=debt_service
    )
    
    return {"dscr": dscr}


# === NOUVEAUX ENDPOINTS FRAIS DE NOTAIRE ===

class NotaryFeeRequest(BaseModel):
    """Requête de calcul des frais de notaire"""
    purchase_price: float = Field(gt=0, description="Prix d'achat du bien")
    buyer_profile: str = Field(description="NEUF, MDB ou INVESTOR")
    building_age_years: Optional[int] = Field(default=None, ge=0, description="Âge du bien en années")
    construction_completion_date: Optional[str] = Field(default=None, description="Date d'achèvement (YYYY-MM-DD)")


class NotaryFeeComparisonRequest(BaseModel):
    """Requête de comparaison des profils"""
    purchase_price: float = Field(gt=0, description="Prix d'achat du bien")
    building_age_years: int = Field(ge=0, description="Âge du bien en années")


@router.post("/notary-fees")
async def calculate_notary_fees(data: NotaryFeeRequest):
    """
    Calculer les frais de notaire avec intelligence fiscale
    
    Profils disponibles :
    - NEUF : Bien en VEFA ou < 5 ans (droits réduits ~2.5%)
    - MDB : Marchand de Biens (TVA sur marge ~3%)
    - INVESTOR : Investisseur classique (droits pleins ~7.5%)
    
    ⚠️ Le service génère des alertes fiscales automatiques en cas de risque
    """
    try:
        result = notary_fee_service.calculate_notary_fees(
            purchase_price=data.purchase_price,
            buyer_profile=data.buyer_profile,
            building_age_years=data.building_age_years,
            construction_completion_date=data.construction_completion_date
        )
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du calcul: {str(e)}"
        )


@router.post("/notary-fees/compare")
async def compare_notary_profiles(data: NotaryFeeComparisonRequest):
    """
    Comparer les frais de notaire selon différents profils
    
    Utile pour :
    - Choisir la meilleure structure d'acquisition
    - Évaluer les économies potentielles
    - Identifier les risques fiscaux
    """
    try:
        result = notary_fee_service.compare_profiles(
            purchase_price=data.purchase_price,
            building_age_years=data.building_age_years
        )
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la comparaison: {str(e)}"
        )


@router.get("/notary-fees/rates")
async def get_notary_rates():
    """
    Récupérer les taux de frais de notaire par profil
    
    Informations de référence pour les utilisateurs
    """
    return {
        "rates": {
            "NEUF": {
                "rate": 0.025,
                "percentage": "2.5%",
                "description": "Droits réduits pour VEFA ou bien < 5 ans",
                "conditions": "Bien neuf ou achevé il y a moins de 5 ans"
            },
            "MDB": {
                "rate": 0.030,
                "percentage": "3.0%",
                "description": "Régime TVA sur marge pour marchands de biens",
                "conditions": "Bien < 5 ans, statut MDB valide",
                "warning": "Risque de requalification si bien > 5 ans"
            },
            "INVESTOR": {
                "rate": 0.075,
                "percentage": "7.5%",
                "description": "Droits de mutation classiques",
                "conditions": "Acquisition standard, bien > 5 ans"
            }
        },
        "age_threshold_years": 5,
        "notes": [
            "Les taux indiqués sont des moyennes incluant tous les frais",
            "Les alertes fiscales sont générées automatiquement",
            "Toujours valider avec un notaire pour cas particuliers"
        ]
    }


# === ENDPOINTS WATERFALL / PROMOTE ===

class WaterfallSimpleRequest(BaseModel):
    """Requête de calcul waterfall simple (2 paliers)"""
    total_profit: float = Field(ge=0, description="Profit total à distribuer")
    equity_invested: float = Field(gt=0, description="Capital investi")
    hurdle_rate: float = Field(default=0.10, ge=0, le=1, description="Taux hurdle (ex: 0.10 = 10%)")
    lp_share_below_hurdle: float = Field(default=1.0, ge=0, le=1, description="Part LP sous hurdle")
    lp_share_above_hurdle: float = Field(default=0.80, ge=0, le=1, description="Part LP au-dessus hurdle")
    gp_share_above_hurdle: float = Field(default=0.20, ge=0, le=1, description="Part GP (Promote)")


class WaterfallAdvancedRequest(BaseModel):
    """Requête de calcul waterfall multi-paliers"""
    total_profit: float = Field(ge=0, description="Profit total à distribuer")
    equity_invested: float = Field(gt=0, description="Capital investi")
    tiers: List[Dict[str, Any]] = Field(
        description="Liste de paliers avec threshold_irr, lp_share, gp_share"
    )


class PromoteSensitivityRequest(BaseModel):
    """Requête d'analyse de sensibilité promote"""
    equity_invested: float = Field(gt=0, description="Capital investi")
    min_profit: float = Field(ge=0, description="Profit minimum")
    max_profit: float = Field(gt=0, description="Profit maximum")
    steps: int = Field(default=10, ge=2, le=50, description="Nombre de scénarios")
    hurdle_rate: float = Field(default=0.10, ge=0, le=1)
    promote_share: float = Field(default=0.20, ge=0, le=1)


@router.post("/waterfall/simple")
async def calculate_waterfall_simple(data: WaterfallSimpleRequest):
    """
    Calculer une distribution waterfall simplifiée (2 paliers)
    
    Structure typique :
    - Palier 1 : 100% LP jusqu'au Hurdle (ex: 10% TRI)
    - Palier 2 : Split LP/GP au-dessus du Hurdle (ex: 80/20 avec promote)
    
    Exemple d'utilisation :
    - Fonds immobilier avec promote 20% au-dessus de 10% TRI
    - Co-investissement avec sponsor
    """
    try:
        result = waterfall_service.calculate_waterfall_simple(
            total_profit=data.total_profit,
            equity_invested=data.equity_invested,
            hurdle_rate=data.hurdle_rate,
            lp_share_below_hurdle=data.lp_share_below_hurdle,
            lp_share_above_hurdle=data.lp_share_above_hurdle,
            gp_share_above_hurdle=data.gp_share_above_hurdle
        )
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du calcul waterfall: {str(e)}"
        )


@router.post("/waterfall/advanced")
async def calculate_waterfall_advanced(data: WaterfallAdvancedRequest):
    """
    Calculer une distribution waterfall multi-paliers personnalisée
    
    Permet de définir plusieurs seuils de promote successifs
    
    Exemple de structure :
    ```json
    {
      "tiers": [
        {"threshold_irr": 0.08, "lp_share": 1.0, "gp_share": 0.0},
        {"threshold_irr": 0.12, "lp_share": 0.85, "gp_share": 0.15},
        {"threshold_irr": 0.18, "lp_share": 0.70, "gp_share": 0.30}
      ]
    }
    ```
    """
    try:
        result = waterfall_service.calculate_waterfall_advanced(
            total_profit=data.total_profit,
            equity_invested=data.equity_invested,
            tiers=data.tiers
        )
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du calcul waterfall avancé: {str(e)}"
        )


@router.post("/waterfall/sensitivity")
async def analyze_promote_sensitivity(data: PromoteSensitivityRequest):
    """
    Analyse de sensibilité : impact du profit sur la distribution LP/GP
    
    Génère plusieurs scénarios de profit pour visualiser :
    - L'effet du promote selon la performance
    - Le point de bascule du hurdle
    - La distribution LP/GP pour chaque scénario
    
    Utile pour :
    - Négociation des termes LP/GP
    - Projection de différents scénarios de sortie
    - Visualisation graphique de la distribution
    """
    try:
        # Générer la plage de profits
        profit_range = [
            data.min_profit + (data.max_profit - data.min_profit) * i / (data.steps - 1)
            for i in range(data.steps)
        ]
        
        results = waterfall_service.calculate_promote_sensitivity(
            equity_invested=data.equity_invested,
            profit_range=profit_range,
            hurdle_rate=data.hurdle_rate,
            promote_share=data.promote_share
        )
        
        return {
            "equity_invested": data.equity_invested,
            "hurdle_rate": data.hurdle_rate,
            "hurdle_rate_pct": f"{data.hurdle_rate * 100:.1f}%",
            "promote_share": data.promote_share,
            "promote_share_pct": f"{data.promote_share * 100:.1f}%",
            "scenarios": results
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse de sensibilité: {str(e)}"
        )


@router.get("/waterfall/templates")
async def get_waterfall_templates():
    """
    Récupérer des templates de structure waterfall typiques
    
    Templates courants dans l'industrie immobilière
    """
    return {
        "templates": {
            "standard_fund": {
                "name": "Fonds Standard",
                "description": "Structure typique d'un fonds immobilier institutionnel",
                "hurdle_rate": 0.08,
                "structure": [
                    {"threshold_irr": 0.08, "lp_share": 1.0, "gp_share": 0.0, "description": "100% LP jusqu'à 8% IRR"},
                    {"threshold_irr": None, "lp_share": 0.80, "gp_share": 0.20, "description": "80/20 au-dessus de 8%"}
                ]
            },
            "aggressive_promote": {
                "name": "Promote Agressif",
                "description": "Structure avec promote élevé pour sponsor expérimenté",
                "hurdle_rate": 0.10,
                "structure": [
                    {"threshold_irr": 0.10, "lp_share": 1.0, "gp_share": 0.0},
                    {"threshold_irr": 0.15, "lp_share": 0.75, "gp_share": 0.25},
                    {"threshold_irr": None, "lp_share": 0.65, "gp_share": 0.35}
                ]
            },
            "conservative": {
                "name": "Conservateur",
                "description": "Structure favorable aux investisseurs",
                "hurdle_rate": 0.12,
                "structure": [
                    {"threshold_irr": 0.12, "lp_share": 1.0, "gp_share": 0.0},
                    {"threshold_irr": None, "lp_share": 0.90, "gp_share": 0.10}
                ]
            },
            "european_style": {
                "name": "Style Européen",
                "description": "Catch-up inclus (GP rattrape sa part)",
                "hurdle_rate": 0.08,
                "structure": [
                    {"threshold_irr": 0.08, "lp_share": 1.0, "gp_share": 0.0, "description": "Hurdle 8%"},
                    {"threshold_irr": 0.10, "lp_share": 0.0, "gp_share": 1.0, "description": "Catch-up GP"},
                    {"threshold_irr": None, "lp_share": 0.80, "gp_share": 0.20, "description": "Split 80/20"}
                ]
            }
        },
        "notes": [
            "Ces templates sont des structures courantes à adapter selon le projet",
            "Le hurdle rate varie selon le risque du projet (6-12% typiquement)",
            "Le promote GP standard est 20% mais peut aller jusqu'à 35%"
        ]
    }


# === ENDPOINTS AMORTISSEMENT AVANCÉ ===

class LoanScheduleRequest(BaseModel):
    """Requête de tableau d'amortissement"""
    loan_amount: float = Field(gt=0, description="Montant du prêt")
    annual_rate: float = Field(ge=0, le=0.20, description="Taux annuel (ex: 0.04 = 4%)")
    years: int = Field(ge=1, le=30, description="Durée en années")
    amortization_type: str = Field(default="classic", description="classic, in_fine ou deferred")
    deferred_months: int = Field(default=0, ge=0, description="Mois de différé (pour type deferred)")
    deferred_interest_capitalized: bool = Field(default=False, description="Capitaliser intérêts du différé")


class AmortizationComparisonRequest(BaseModel):
    """Requête de comparaison des types d'amortissement"""
    loan_amount: float = Field(gt=0, description="Montant du prêt")
    annual_rate: float = Field(ge=0, le=0.20, description="Taux annuel")
    years: int = Field(ge=1, le=30, description="Durée en années")
    deferred_months: int = Field(default=12, ge=1, le=60, description="Durée différé pour comparaison")


@router.post("/loan/schedule")
async def generate_loan_schedule(data: LoanScheduleRequest):
    """
    Générer un tableau d'amortissement détaillé mois par mois
    
    Types d'amortissement :
    - **classic** : Mensualités constantes (amortissement classique)
    - **in_fine** : Intérêts seuls + capital en fin de prêt
    - **deferred** : Différé d'amortissement pendant travaux
    
    Le différé peut être avec :
    - Intérêts capitalisés (ajoutés au capital)
    - Intérêts payés chaque mois
    
    Retourne un tableau complet avec :
    - Mensualité, capital, intérêts par mois
    - Capital restant dû
    - Cumuls
    """
    try:
        schedule = financial_service.calculate_loan_schedule(
            loan_amount=data.loan_amount,
            annual_rate=data.annual_rate,
            years=data.years,
            amortization_type=data.amortization_type,
            deferred_months=data.deferred_months,
            deferred_interest_capitalized=data.deferred_interest_capitalized
        )
        return schedule
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du calcul: {str(e)}"
        )


@router.post("/loan/compare")
async def compare_amortization_options(data: AmortizationComparisonRequest):
    """
    Comparer les coûts selon différents types d'amortissement
    
    Compare 4 options :
    1. Amortissement classique (mensualités fixes)
    2. In-Fine (capital en fin)
    3. Différé avec intérêts capitalisés
    4. Différé avec intérêts payés
    
    Utile pour :
    - Choisir la meilleure option selon le projet
    - Optimiser la trésorerie pendant travaux
    - Comparer les coûts totaux
    """
    try:
        comparison = financial_service.compare_amortization_types(
            loan_amount=data.loan_amount,
            annual_rate=data.annual_rate,
            years=data.years,
            deferred_months=data.deferred_months
        )
        return comparison
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la comparaison: {str(e)}"
        )


@router.get("/loan/types")
async def get_loan_types():
    """
    Documentation des types d'amortissement disponibles
    """
    return {
        "types": {
            "classic": {
                "name": "Amortissement Classique",
                "description": "Mensualités constantes (capital + intérêts)",
                "use_case": "Standard pour tous types de projets",
                "pros": [
                    "Mensualités prévisibles",
                    "Coût total maîtrisé",
                    "Capital remboursé progressivement"
                ],
                "cons": [
                    "Cash-flow négatif dès le début"
                ]
            },
            "in_fine": {
                "name": "In-Fine",
                "description": "Intérêts seuls pendant la durée + capital en une fois à la fin",
                "use_case": "Projet avec revente planifiée, VEFA, promoteur",
                "pros": [
                    "Mensualités faibles pendant le prêt",
                    "Optimisation fiscale (intérêts déductibles)",
                    "Capital disponible pour d'autres investissements"
                ],
                "cons": [
                    "Coût total plus élevé (intérêts sur capital constant)",
                    "Nécessite préparation pour remboursement final",
                    "Risque si revente ne se fait pas"
                ]
            },
            "deferred": {
                "name": "Différé d'amortissement",
                "description": "Pause dans le remboursement pendant travaux",
                "use_case": "Rénovation lourde, immeuble sans revenu initial",
                "options": {
                    "capitalized": "Intérêts capitalisés (ajoutés au capital)",
                    "paid": "Intérêts payés chaque mois"
                },
                "pros": [
                    "Trésorerie préservée pendant travaux",
                    "Remboursement quand revenus démarrent"
                ],
                "cons": [
                    "Coût total plus élevé si capitalisé",
                    "Durée totale allongée"
                ]
            }
        },
        "recommendations": {
            "renovation_with_works": "deferred (capitalized)",
            "buy_and_hold": "classic",
            "flip_resale": "in_fine",
            "vefa_developer": "in_fine"
        }
    }
