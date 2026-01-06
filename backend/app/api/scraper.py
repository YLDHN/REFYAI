from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.models.project import Project
from app.workers.tasks import scrape_all_project_data

router = APIRouter(prefix="/scraper", tags=["scraper"])


class ScraperRequest(BaseModel):
    """Requête de lancement de scraping"""
    project_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@router.post("/start/{project_id}")
async def start_project_scraping(
    project_id: int,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Lancer le scraping complet pour un projet
    
    Lance en arrière-plan :
    - Cadastre (parcelle, surface)
    - PLU (zonage, règlement)
    - Zones inondables (si coordonnées GPS fournies)
    
    Retourne immédiatement un task_id pour suivre l'avancement
    """
    # Vérifier que le projet existe
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projet {project_id} introuvable"
        )
    
    if not project.address or not project.city or not project.postal_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le projet doit avoir une adresse complète pour le scraping"
        )
    
    # Lancer la tâche Celery
    task = scrape_all_project_data.apply_async(
        args=[
            project_id,
            project.address,
            project.city,
            project.postal_code,
            latitude,
            longitude
        ]
    )
    
    return {
        "project_id": project_id,
        "task_id": task.id,
        "status": "started",
        "message": "Scraping lancé en arrière-plan",
        "estimated_duration_seconds": 60,
        "check_status_url": f"/api/v1/scraper/status/{task.id}"
    }


@router.get("/status/{task_id}")
async def get_scraping_status(task_id: str):
    """
    Vérifier le statut d'une tâche de scraping
    
    États possibles :
    - PENDING : En attente
    - STARTED : Démarré
    - SUCCESS : Terminé avec succès
    - FAILURE : Échec
    - RETRY : Nouvelle tentative
    """
    from celery.result import AsyncResult
    
    task = AsyncResult(task_id)
    
    response = {
        "task_id": task_id,
        "status": task.state,
        "current": task.info.get("current", 0) if isinstance(task.info, dict) else 0,
        "total": task.info.get("total", 100) if isinstance(task.info, dict) else 100
    }
    
    if task.state == "SUCCESS":
        response["result"] = task.result
        response["completed_at"] = datetime.now().isoformat()
    elif task.state == "FAILURE":
        response["error"] = str(task.info)
    
    return response


@router.get("/health")
async def check_workers_health():
    """
    Vérifier que les workers Celery sont actifs
    """
    try:
        from celery_app import celery_app
        
        # Inspecter les workers
        inspect = celery_app.control.inspect()
        active = inspect.active()
        stats = inspect.stats()
        
        if not active:
            return {
                "status": "unhealthy",
                "message": "Aucun worker Celery actif",
                "workers": 0
            }
        
        return {
            "status": "healthy",
            "workers": len(active),
            "active_tasks": sum(len(tasks) for tasks in active.values()),
            "worker_stats": stats
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
