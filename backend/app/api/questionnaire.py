"""
Routes API pour le questionnaire de localisation
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from app.services.location_questionnaire_service import LocationQuestionnaireService

router = APIRouter(prefix="/questionnaire", tags=["questionnaire"])

questionnaire_service = LocationQuestionnaireService()


class QuestionnaireAnswers(BaseModel):
    """Modèle pour les réponses du questionnaire"""
    answers: Dict[str, Any]


@router.get("/questions")
async def get_questionnaire():
    """
    Récupère le questionnaire de localisation complet
    
    Returns:
        Liste des questions avec types et options
    """
    return {
        "questions": questionnaire_service.get_questions(),
        "total_questions": len(questionnaire_service.QUESTIONS),
        "estimated_time_minutes": 5
    }


@router.post("/validate")
async def validate_answers(data: QuestionnaireAnswers):
    """
    Valide les réponses du questionnaire
    
    Returns:
        Résultat de validation avec erreurs et warnings
    """
    validation = questionnaire_service.validate_answers(data.answers)
    
    return {
        "validation": validation,
        "answers_count": len(data.answers),
        "required_count": len([q for q in questionnaire_service.QUESTIONS if q["required"]])
    }


@router.post("/extract-filters")
async def extract_plu_filters(data: QuestionnaireAnswers):
    """
    Extrait les filtres PLU optimisés à partir des réponses
    
    Returns:
        Critères de recherche PLU personnalisés
    """
    filters = questionnaire_service.extract_plu_filters(data.answers)
    
    return {
        "filters": filters,
        "estimated_plu_pages": "500-3000",
        "estimated_analysis_time": "30-60 secondes",
        "message": "Filtres optimisés pour analyse PLU ciblée"
    }
