"""
Routes API pour les statistiques du dashboard selon BP
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Dict
from app.core.database import get_db
from app.models.project import Project, ProjectStatus

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
async def get_dashboard_stats(
    user_id: int,  # TODO: Récupérer depuis auth token
    db: Session = Depends(get_db)
):
    """
    Statistiques dashboard selon Business Plan
    
    Métriques:
    - Nombre de projets en cours
    - Equity disponible
    - Durée moyenne opérations en cours
    - Scoring technique moyen
    
    Returns:
        Stats adaptées au BP
    """
    # Statuts considérés "en cours"
    active_statuses = [
        ProjectStatus.ANALYZING.value,
        ProjectStatus.NEGOTIATING.value,
        ProjectStatus.OFFER_SENT.value,
        ProjectStatus.FINANCING_SEARCH.value,
        ProjectStatus.DUE_DILIGENCE.value,
        ProjectStatus.UNDER_CONTRACT.value,
        # Anciens pour compatibilité
        ProjectStatus.IN_PROGRESS.value,
        ProjectStatus.DRAFT.value
    ]
    
    # Requêtes
    query_base = db.query(Project).filter(Project.user_id == user_id)
    
    # Nombre total de projets
    total_projects = query_base.count()
    
    # Projets en cours
    active_projects_query = query_base.filter(Project.status.in_(active_statuses))
    active_projects_count = active_projects_query.count()
    
    # Equity disponible (simplifié: assumant equity fixe - equity investie)
    # TODO: Intégrer avec vraie gestion equity utilisateur
    total_equity_assumed = 10_000_000  # À remplacer par vraie donnée utilisateur
    active_projects_list = active_projects_query.all()
    
    equity_invested = sum([
        (p.purchase_price or 0) - (p.financing_amount or 0) +
        (p.renovation_budget or 0)
        for p in active_projects_list
    ])
    
    equity_available = max(0, total_equity_assumed - equity_invested)
    
    # Durée moyenne restante (estimée selon status)
    # Mapping status → durée typique restante (mois)
    status_duration_map = {
        ProjectStatus.ANALYZING.value: 6,
        ProjectStatus.NEGOTIATING.value: 4,
        ProjectStatus.OFFER_SENT.value: 3,
        ProjectStatus.FINANCING_SEARCH.value: 2,
        ProjectStatus.DUE_DILIGENCE.value: 2,
        ProjectStatus.UNDER_CONTRACT.value: 1,
        ProjectStatus.IN_PROGRESS.value: 12,  # Ancien statut générique
        ProjectStatus.DRAFT.value: 6
    }
    
    if active_projects_count > 0:
        total_months_remaining = sum([
            status_duration_map.get(p.status, 6)
            for p in active_projects_list
        ])
        avg_duration_remaining = total_months_remaining / active_projects_count
    else:
        avg_duration_remaining = 0
    
    # Scoring technique moyen
    projects_with_score = query_base.filter(Project.technical_score.isnot(None)).all()
    if projects_with_score:
        avg_technical_score = sum([p.technical_score for p in projects_with_score]) / len(projects_with_score)
    else:
        avg_technical_score = None
    
    return {
        "success": True,
        "stats": {
            "total_projects": total_projects,
            "active_projects": active_projects_count,
            "equity_available": round(equity_available, 2),
            "avg_duration_remaining_months": round(avg_duration_remaining, 1),
            "technical_score_avg": round(avg_technical_score, 1) if avg_technical_score else None
        },
        "note": "Metrics selon Business Plan - Equity basé sur estimation"
    }
