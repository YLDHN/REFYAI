from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.core.database import get_db
from app.models.timeline import ProjectTimeline, CurveType
from app.models.project import Project
from app.services.timeline_service import timeline_service

router = APIRouter(prefix="/timeline", tags=["timeline"])


class TimelineCreateRequest(BaseModel):
    """Requête de création de timeline"""
    project_id: int
    
    # Phase Études
    study_phase_start: datetime
    study_duration_months: int = Field(ge=1, le=24, description="Durée études en mois")
    study_phase_budget: float = Field(ge=0, description="Budget études")
    
    # Phase Permis
    permit_duration_months: int = Field(ge=1, le=36, description="Durée instruction permis")
    permit_fees: float = Field(default=0, ge=0)
    
    # Phase Travaux
    construction_duration_months: int = Field(ge=1, le=60, description="Durée travaux")
    construction_budget: float = Field(ge=0, description="Budget travaux")
    capex_curve_type: str = Field(default="s_curve", description="Type courbe CAPEX")
    
    # Phase Commercialisation
    commercialization_duration_months: int = Field(ge=0, le=60)
    commercialization_type: str = Field(description="VEFA, RENTAL, RESALE, MIXED")
    
    # Options
    execution_mode: str = Field(default="sequential", description="sequential ou parallel")
    notes: Optional[str] = None


class TimelineUpdateRequest(BaseModel):
    """Requête de mise à jour de timeline"""
    study_phase_start: Optional[datetime] = None
    study_duration_months: Optional[int] = None
    study_phase_budget: Optional[float] = None
    permit_duration_months: Optional[int] = None
    permit_fees: Optional[float] = None
    construction_duration_months: Optional[int] = None
    construction_budget: Optional[float] = None
    capex_curve_type: Optional[str] = None
    commercialization_duration_months: Optional[int] = None
    commercialization_type: Optional[str] = None
    execution_mode: Optional[str] = None
    notes: Optional[str] = None


class TimelineResponse(BaseModel):
    """Réponse avec timeline complète"""
    id: int
    project_id: int
    
    # Dates calculées
    project_start_date: Optional[datetime]
    project_end_date: Optional[datetime]
    total_duration_months: Optional[int]
    
    # Phases
    study_phase_start: Optional[datetime]
    study_phase_end: Optional[datetime]
    study_phase_budget: float
    
    permit_phase_start: Optional[datetime]
    permit_phase_end: Optional[datetime]
    permit_fees: float
    
    construction_phase_start: Optional[datetime]
    construction_phase_end: Optional[datetime]
    construction_budget: float
    capex_curve_type: str
    
    commercialization_phase_start: Optional[datetime]
    commercialization_phase_end: Optional[datetime]
    commercialization_type: Optional[str]
    
    execution_mode: str
    notes: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


@router.post("/", response_model=TimelineResponse, status_code=status.HTTP_201_CREATED)
async def create_timeline(
    data: TimelineCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Créer une timeline pour un projet
    """
    # Vérifier que le projet existe
    result = await db.execute(
        select(Project).where(Project.id == data.project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projet {data.project_id} introuvable"
        )
    
    # Vérifier qu'il n'y a pas déjà une timeline
    result = await db.execute(
        select(ProjectTimeline).where(ProjectTimeline.project_id == data.project_id)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Une timeline existe déjà pour ce projet"
        )
    
    # Générer les dates de phases
    phases = timeline_service.generate_phase_dates(
        start_date=data.study_phase_start,
        study_months=data.study_duration_months,
        permit_months=data.permit_duration_months,
        construction_months=data.construction_duration_months,
        commercialization_months=data.commercialization_duration_months,
        execution_mode=data.execution_mode
    )
    
    # Calculer la courbe CAPEX
    capex_curve = timeline_service.calculate_capex_curve(
        total_capex=data.construction_budget,
        construction_months=data.construction_duration_months,
        curve_type=data.capex_curve_type
    )
    
    # Calculer durée totale
    duration = timeline_service.calculate_project_duration(
        study_months=data.study_duration_months,
        permit_months=data.permit_duration_months,
        construction_months=data.construction_duration_months,
        commercialization_months=data.commercialization_duration_months,
        execution_mode=data.execution_mode
    )
    
    # Créer la timeline
    timeline = ProjectTimeline(
        project_id=data.project_id,
        
        # Phase Études
        study_phase_start=phases["studies"]["start"],
        study_phase_end=phases["studies"]["end"],
        study_phase_budget=data.study_phase_budget,
        
        # Phase Permis
        permit_phase_start=phases["permit"]["start"],
        permit_phase_end=phases["permit"]["end"],
        permit_fees=data.permit_fees,
        
        # Phase Travaux
        construction_phase_start=phases["construction"]["start"],
        construction_phase_end=phases["construction"]["end"],
        construction_budget=data.construction_budget,
        capex_curve_type=data.capex_curve_type,
        
        # Phase Commercialisation
        commercialization_phase_start=phases["commercialization"]["start"],
        commercialization_phase_end=phases["commercialization"]["end"],
        commercialization_type=data.commercialization_type,
        
        # Calculés
        project_start_date=phases["studies"]["start"],
        project_end_date=phases["commercialization"]["end"],
        total_duration_months=duration["total_months"],
        
        # Méta
        execution_mode=data.execution_mode,
        notes=data.notes,
        
        # Stockage courbe CAPEX
        construction_milestones=capex_curve
    )
    
    db.add(timeline)
    await db.commit()
    await db.refresh(timeline)
    
    return timeline


@router.get("/{project_id}", response_model=TimelineResponse)
async def get_timeline(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupérer la timeline d'un projet
    """
    result = await db.execute(
        select(ProjectTimeline).where(ProjectTimeline.project_id == project_id)
    )
    timeline = result.scalar_one_or_none()
    
    if not timeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune timeline pour le projet {project_id}"
        )
    
    return timeline


@router.put("/{project_id}", response_model=TimelineResponse)
async def update_timeline(
    project_id: int,
    data: TimelineUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Mettre à jour une timeline existante
    """
    result = await db.execute(
        select(ProjectTimeline).where(ProjectTimeline.project_id == project_id)
    )
    timeline = result.scalar_one_or_none()
    
    if not timeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune timeline pour le projet {project_id}"
        )
    
    # Mise à jour des champs fournis
    update_data = data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if hasattr(timeline, field):
            setattr(timeline, field, value)
    
    # Recalculer les dates si nécessaire
    # TODO: Ajouter logique de recalcul intelligent
    
    await db.commit()
    await db.refresh(timeline)
    
    return timeline


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timeline(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Supprimer une timeline
    """
    result = await db.execute(
        select(ProjectTimeline).where(ProjectTimeline.project_id == project_id)
    )
    timeline = result.scalar_one_or_none()
    
    if not timeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune timeline pour le projet {project_id}"
        )
    
    await db.delete(timeline)
    await db.commit()


@router.get("/{project_id}/capex-curve")
async def get_capex_curve(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupérer la courbe de décaissement CAPEX mensuelle
    """
    result = await db.execute(
        select(ProjectTimeline).where(ProjectTimeline.project_id == project_id)
    )
    timeline = result.scalar_one_or_none()
    
    if not timeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune timeline pour le projet {project_id}"
        )
    
    return {
        "project_id": project_id,
        "curve_type": timeline.capex_curve_type,
        "total_budget": timeline.construction_budget,
        "duration_months": timeline.total_duration_months,
        "curve": timeline.construction_milestones or []
    }


@router.get("/{project_id}/summary")
async def get_timeline_summary(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupérer un résumé visuel de la timeline
    """
    result = await db.execute(
        select(ProjectTimeline).where(ProjectTimeline.project_id == project_id)
    )
    timeline = result.scalar_one_or_none()
    
    if not timeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune timeline pour le projet {project_id}"
        )
    
    return {
        "project_id": project_id,
        "total_duration_months": timeline.total_duration_months,
        "total_duration_years": round(timeline.total_duration_months / 12, 1),
        "start_date": timeline.project_start_date,
        "end_date": timeline.project_end_date,
        "phases": {
            "studies": {
                "start": timeline.study_phase_start,
                "end": timeline.study_phase_end,
                "budget": timeline.study_phase_budget
            },
            "permit": {
                "start": timeline.permit_phase_start,
                "end": timeline.permit_phase_end,
                "fees": timeline.permit_fees
            },
            "construction": {
                "start": timeline.construction_phase_start,
                "end": timeline.construction_phase_end,
                "budget": timeline.construction_budget,
                "curve_type": timeline.capex_curve_type
            },
            "commercialization": {
                "start": timeline.commercialization_phase_start,
                "end": timeline.commercialization_phase_end,
                "type": timeline.commercialization_type
            }
        },
        "execution_mode": timeline.execution_mode
    }
