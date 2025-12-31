"""
Routes API pour le service de délais administratifs
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.administrative_delay_service import (
    administrative_delay_service,
    ComplexityLevel,
    ProcedureType
)

router = APIRouter(prefix="/admin-delays", tags=["Administrative Delays"])


class ProcedureDelayRequest(BaseModel):
    city: str
    procedure_type: str
    complexity: float = ComplexityLevel.SIMPLE
    has_abf: bool = False


class ProcedureItem(BaseModel):
    type: str
    complexity: float = ComplexityLevel.SIMPLE
    has_abf: bool = False


class ProjectTimelineRequest(BaseModel):
    city: str
    procedures: List[ProcedureItem]
    parallel_execution: bool = False


class FullProjectDurationRequest(BaseModel):
    city: str
    has_pc: bool = False
    has_dp: bool = False
    has_abf: bool = False
    complexity: float = ComplexityLevel.SIMPLE
    construction_months: int = 6


@router.post("/procedure")
async def get_procedure_delay(request: ProcedureDelayRequest):
    """
    Obtenir le délai pour une procédure administrative
    
    Body:
        {
            "city": "Paris",
            "procedure_type": "permis_construire",
            "complexity": 1.3,
            "has_abf": true
        }
    
    Returns:
        Délais min/avg/max en jours et mois
    """
    result = administrative_delay_service.get_procedure_delay(
        request.city,
        request.procedure_type,
        request.complexity,
        request.has_abf
    )
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return {
        "success": True,
        **result
    }


@router.post("/project-timeline")
async def calculate_project_timeline(request: ProjectTimelineRequest):
    """
    Calculer le planning complet d'un projet
    
    Body:
        {
            "city": "Paris",
            "procedures": [
                {"type": "permis_construire", "complexity": 1.5, "has_abf": true}
            ],
            "parallel_execution": false
        }
    
    Returns:
        Timeline complète avec dates estimées
    """
    procedures = [
        {
            "type": proc.type,
            "complexity": proc.complexity,
            "has_abf": proc.has_abf
        }
        for proc in request.procedures
    ]
    
    result = administrative_delay_service.calculate_project_timeline(
        request.city,
        procedures,
        request.parallel_execution
    )
    
    return {
        "success": True,
        **result
    }


@router.post("/full-duration")
async def estimate_full_project_duration(request: FullProjectDurationRequest):
    """
    Estimation complète durée projet (études + admin + travaux + DAACT)
    
    Body:
        {
            "city": "Paris",
            "has_pc": true,
            "has_abf": true,
            "complexity": 1.5,
            "construction_months": 8
        }
    
    Returns:
        Durée totale par phases avec dates
    """
    project_data = {
        "has_pc": request.has_pc,
        "has_dp": request.has_dp,
        "has_abf": request.has_abf,
        "complexity": request.complexity,
        "construction_months": request.construction_months
    }
    
    result = administrative_delay_service.estimate_full_project_duration(
        request.city,
        project_data
    )
    
    return {
        "success": True,
        **result
    }


@router.get("/available-procedures")
async def get_available_procedures():
    """
    Liste des procédures administratives disponibles
    
    Returns:
        Liste des procédures avec descriptions
    """
    return {
        "success": True,
        "procedures": [
            {
                "type": ProcedureType.PC,
                "name": "Permis de Construire",
                "typical_delay_days": 60,
                "description": "Construction neuve ou travaux lourds"
            },
            {
                "type": ProcedureType.DP,
                "name": "Déclaration Préalable",
                "typical_delay_days": 30,
                "description": "Travaux moyens, extensions < 40m²"
            },
            {
                "type": ProcedureType.AT,
                "name": "Autorisation de Travaux",
                "typical_delay_days": 30,
                "description": "Travaux en copropriété ou zone protégée"
            },
            {
                "type": ProcedureType.ABF,
                "name": "Avis ABF",
                "typical_delay_days": 45,
                "description": "Avis Architecte Bâtiments de France"
            },
            {
                "type": ProcedureType.PD,
                "name": "Permis de Démolir",
                "typical_delay_days": 60,
                "description": "Démolition totale ou partielle"
            },
            {
                "type": ProcedureType.CU,
                "name": "Certificat d'Urbanisme",
                "typical_delay_days": 30,
                "description": "Renseignements d'urbanisme"
            },
            {
                "type": ProcedureType.DAACT,
                "name": "Déclaration d'Achèvement",
                "typical_delay_days": 90,
                "description": "Visite conformité post-travaux"
            }
        ]
    }


@router.get("/cities")
async def get_cities_with_data():
    """
    Liste des villes avec données spécifiques
    
    Returns:
        Liste des villes
    """
    cities = administrative_delay_service.get_cities_with_data()
    
    return {
        "success": True,
        "cities": cities,
        "total": len(cities),
        "note": "Pour les autres villes, des délais par défaut sont utilisés"
    }


@router.get("/complexity-levels")
async def get_complexity_levels():
    """
    Niveaux de complexité disponibles
    
    Returns:
        Liste des niveaux avec descriptions
    """
    return {
        "success": True,
        "complexity_levels": [
            {
                "value": ComplexityLevel.SIMPLE,
                "name": "Simple",
                "description": "Projet standard sans contraintes particulières"
            },
            {
                "value": ComplexityLevel.MODERATE,
                "name": "Modéré",
                "description": "Quelques contraintes (ABF, site classé, etc.)"
            },
            {
                "value": ComplexityLevel.COMPLEX,
                "name": "Complexe",
                "description": "Nombreuses contraintes réglementaires"
            },
            {
                "value": ComplexityLevel.VERY_COMPLEX,
                "name": "Très Complexe",
                "description": "Projet exceptionnel (monuments historiques, etc.)"
            }
        ]
    }
