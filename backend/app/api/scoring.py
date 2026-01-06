"""
Routes API pour scoring technique projet
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from app.services.scoring_service import scoring_service

router = APIRouter(prefix="/scoring", tags=["Technical Scoring"])


class TechnicalScoringRequest(BaseModel):
    """Requête scoring technique"""
    # Urbanisme
    abf_zone: bool = False
    secteur_sauvegarde: bool = False
    distance_monument_historique: Optional[float] = None
    plu_zone: str = "U"
    ces_calcule: Optional[float] = None
    ces_max_autorise: Optional[float] = None
    
    # Technique
    amiante_present: bool = False
    plomb_present: bool = False
    structure_etat: str = "bon"  # bon, moyen, fragile
    dpe_classe: str = "D"  # A, B, C, D, E, F, G
    electricite_conforme: bool = True
    
    # Financier
    ltv: float = 0.70
    dscr: float = 1.5
    tri: float = 0.12
    capex_budgete: Optional[float] = None
    capex_median_marche: Optional[float] = None
    
    # Juridique
    copro_contentieux: bool = False
    servitudes_count: int = 0
    
    # Environnemental
    zone_inondable: bool = False
    pollution_sol: bool = False
    radon_zone: int = 1  # 1, 2, 3


@router.post("/calculate")
async def calculate_technical_score(request: TechnicalScoringRequest):
    """
    📊 Calcule score technique projet sur /100
    
    Analyse:
    - Risques urbanistiques (ABF, secteur sauvegardé, PLU)
    - Risques techniques (amiante, structure, DPE)
    - Risques financiers (LTV, DSCR, TRI)
    - Risques juridiques (copropriété, servitudes)
    - Risques environnementaux (inondation, pollution)
    
    Pénalités:
    - CRITICAL: -25 points
    - MAJOR: -10 points
    - MINOR: -5 points
    
    Body:
        {
            "abf_zone": false,
            "ltv": 0.75,
            "dscr": 1.3,
            "tri": 0.10,
            "amiante_present": true,
            "dpe_classe": "F"
        }
    
    Returns:
        Score /100 + détails risques + recommandations
    """
    project_data = request.dict()
    result = scoring_service.calculate_technical_score(project_data)
    
    return result


@router.get("/risks-reference")
async def get_risks_reference():
    """
    📋 Documentation complète des risques évalués
    
    Returns:
        Liste tous les risques avec description + mitigation
    """
    return {
        "success": True,
        "categories": [
            "URBANISME",
            "TECHNIQUE",
            "FINANCIER",
            "JURIDIQUE",
            "ENVIRONNEMENTAL"
        ],
        "risk_levels": {
            "CRITICAL": {
                "penalty": -25,
                "description": "Risque bloquant ou impact majeur sur viabilité"
            },
            "MAJOR": {
                "penalty": -10,
                "description": "Risque significatif nécessitant mitigation"
            },
            "MINOR": {
                "penalty": -5,
                "description": "Risque gérable avec précautions"
            }
        },
        "total_rules": len(scoring_service.RISK_RULES),
        "sample_risks": [
            {
                "key": "secteur_sauvegarde",
                "label": "Secteur sauvegardé",
                "category": "URBANISME",
                "level": "CRITICAL",
                "penalty": -25,
                "description": "Autorisations très restrictives",
                "mitigation": "Étude patrimoine + autorisation spéciale"
            },
            {
                "key": "amiante_detecte",
                "label": "Présence amiante",
                "category": "TECHNIQUE",
                "level": "MAJOR",
                "penalty": -10,
                "description": "Désamiantage +15% budget",
                "mitigation": "30-80€/m2 + entreprise certifiée"
            }
        ]
    }
