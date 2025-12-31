"""
Routes API pour la détection des showstoppers
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from app.services.showstopper_service import ShowstopperDetectionService

router = APIRouter(prefix="/showstoppers", tags=["showstoppers"])

showstopper_service = ShowstopperDetectionService()


class ShowstopperAnalysisRequest(BaseModel):
    """Requête d'analyse des showstoppers"""
    project_data: Dict[str, Any]
    questionnaire_answers: Dict[str, Any]
    plu_analysis: Dict[str, Any] = {}
    technical_analysis: Dict[str, Any] = {}


@router.post("/detect")
async def detect_showstoppers(request: ShowstopperAnalysisRequest):
    """
    Détecte automatiquement les points bloquants du projet
    
    Returns:
        Liste complète des showstoppers avec recommandations
    """
    showstoppers = showstopper_service.detect_showstoppers(
        project_data=request.project_data,
        questionnaire_answers=request.questionnaire_answers,
        plu_analysis=request.plu_analysis,
        technical_analysis=request.technical_analysis
    )
    
    return {
        "showstoppers": showstoppers,
        "total_count": len(showstoppers),
        "critical_count": len([s for s in showstoppers if s["severity"] == "critical"]),
        "high_count": len([s for s in showstoppers if s["severity"] == "high"]),
        "project_status": "BLOQUÉ" if any(s["severity"] == "critical" for s in showstoppers) else "VIABLE"
    }


@router.post("/action-plan")
async def generate_action_plan(request: ShowstopperAnalysisRequest):
    """
    Génère un plan d'action priorisé pour résoudre les showstoppers
    
    Returns:
        Plan d'action avec timeline et budget
    """
    showstoppers = showstopper_service.detect_showstoppers(
        project_data=request.project_data,
        questionnaire_answers=request.questionnaire_answers,
        plu_analysis=request.plu_analysis,
        technical_analysis=request.technical_analysis
    )
    
    action_plan = showstopper_service.generate_action_plan(showstoppers)
    
    return {
        "action_plan": action_plan,
        "showstoppers": showstoppers,
        "recommendation": "Traiter les points CRITICAL en priorité absolue"
    }


@router.get("/categories")
async def get_showstopper_categories():
    """
    Retourne les catégories et sévérités de showstoppers
    
    Returns:
        Documentation des showstoppers possibles
    """
    return {
        "severities": [
            {"level": "critical", "description": "Bloquant absolu - Projet irréalisable"},
            {"level": "high", "description": "Très risqué - Coûts et délais importants"},
            {"level": "medium", "description": "À surveiller - Impact modéré"},
            {"level": "low", "description": "Mineur - Impact limité"}
        ],
        "categories": [
            {"type": "regulatory", "description": "Réglementaire - PLU, urbanisme, autorisations"},
            {"type": "technical", "description": "Technique - Structure, conformité, travaux"},
            {"type": "financial", "description": "Financier - Rentabilité, financement"},
            {"type": "legal", "description": "Juridique - Servitudes, copropriété, litiges"}
        ],
        "common_showstoppers": [
            "Zone non constructible",
            "Dépassement COS/CES",
            "ABF obligatoire",
            "Risque structurel majeur",
            "Amiante/Plomb",
            "Non-conformité incendie",
            "Non-conformité PMR",
            "TRI insuffisant",
            "LTV trop élevé"
        ]
    }
