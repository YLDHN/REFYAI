from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List
from app.core.database import get_db
from app.models import Project, ProjectStatus, ProjectType
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/projects", tags=["projects"])

# Schémas Pydantic
class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    project_type: ProjectType
    purchase_price: float | None = None
    renovation_budget: float | None = None
    estimated_value: float | None = None

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    project_type: ProjectType | None = None
    status: ProjectStatus | None = None
    purchase_price: float | None = None
    renovation_budget: float | None = None
    estimated_value: float | None = None

class ProjectResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str | None
    address: str | None
    city: str | None
    postal_code: str | None
    project_type: ProjectType | None
    status: ProjectStatus
    purchase_price: float | None
    renovation_budget: float | None
    estimated_value: float | None
    technical_score: float | None
    risk_score: float | None
    created_at: datetime
    updated_at: datetime | None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """Créer un nouveau projet"""
    
    # TODO: Récupérer l'ID de l'utilisateur connecté depuis le token
    user_id = 1
    
    project = Project(
        user_id=user_id,
        **project_data.model_dump()
    )
    
    db.add(project)
    await db.commit()
    await db.refresh(project)
    
    return project

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    status: ProjectStatus | None = None,
    db: AsyncSession = Depends(get_db)
):
    """Lister tous les projets"""
    
    # TODO: Filtrer par user_id
    query = select(Project)
    
    if status:
        query = query.where(Project.status == status)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    projects = result.scalars().all()
    
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Récupérer un projet par ID"""
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Mettre à jour un projet"""
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    
    # Mettre à jour les champs
    for key, value in project_data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    
    await db.commit()
    await db.refresh(project)
    
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Supprimer un projet"""
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    
    await db.delete(project)
    await db.commit()
    
    return None
