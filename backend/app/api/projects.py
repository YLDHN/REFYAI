from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models import Project, ProjectStatus, ProjectType, User
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
    project_type: str | None = "rental"  # rental, resale, mixed - avec défaut
    
    # Nouveaux champs
    strategy: str | None = None  # core, core_plus, value_add
    bp_duration: int | None = None
    asset_type: str | None = None  # residential, office, logistics, retail, mixed
    surface: float | None = None
    
    # Financier de base
    purchase_price: float | None = None
    renovation_budget: float | None = None
    estimated_value: float | None = None
    
    # Données locatives
    lease_start_date: str | None = None
    walb: float | None = None
    walt: float | None = None
    current_rent: float | None = None
    market_rent: float | None = None
    occupancy_rate: float | None = None
    lease_state: dict | None = None
    
    # Acquisition
    acquisition_price: float | None = None
    notary_fees: float | None = None
    due_diligence_cost: float | None = None
    acquisition_yield: float | None = None
    
    # CAPEX et renouvellement
    rent_renewal_assumptions: dict | None = None
    capex_details: dict | None = None
    
    # Financement
    financing_amount: float | None = None
    ltv: float | None = None
    interest_rate: float | None = None
    loan_duration: int | None = None

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    project_type: str | None = None
    status: str | None = None
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
    project_type: str | None
    status: str
    
    # Nouveaux champs
    strategy: str | None = None
    bp_duration: int | None = None
    asset_type: str | None = None
    surface: float | None = None
    
    # Financier
    purchase_price: float | None
    renovation_budget: float | None
    estimated_value: float | None
    
    # Locatif
    current_rent: float | None = None
    market_rent: float | None = None
    occupancy_rate: float | None = None
    walb: float | None = None
    walt: float | None = None
    acquisition_yield: float | None = None
    
    # Acquisition
    acquisition_price: float | None = None
    notary_fees: float | None = None
    due_diligence_cost: float | None = None
    
    # CAPEX
    capex_details: dict | None = None
    
    # Financement
    financing_amount: float | None = None
    ltv: float | None = None
    interest_rate: float | None = None
    loan_duration: int | None = None
    
    # Scores
    technical_score: float | None
    risk_score: float | None
    created_at: datetime
    updated_at: datetime | None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Créer un nouveau projet"""
    
    # Convertir les données en dict
    data = project_data.model_dump()
    
    # Forcer la conversion des valeurs en minuscules pour les enums
    if 'project_type' in data and data['project_type']:
        data['project_type'] = data['project_type'].lower()
    if 'status' in data and data['status']:
        data['status'] = data['status'].lower()
    
    project = Project(
        user_id=current_user.id,
        **data
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
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lister tous les projets de l'utilisateur connecté"""
    
    # Filtrer par utilisateur
    query = select(Project).where(Project.user_id == current_user.id)
    
    if status:
        query = query.where(Project.status == status)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    projects = result.scalars().all()
    
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupérer un projet par ID"""
    
    result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.user_id == current_user.id
        )
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
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mettre à jour un projet"""
    
    result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.user_id == current_user.id
        )
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
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Supprimer un projet"""
    
    result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.user_id == current_user.id
        )
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


@router.get("/{project_id}/technical-score")
async def get_technical_score(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Calcule le score technique d'un projet"""
    from app.services.capex_service import CapexService
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    
    service = CapexService()
    score = service.calculate_technical_score(
        construction_year=project.construction_year or 2000,
        last_renovation_year=None,
        structural_issues=False,
        accessibility_compliant=True
    )
    
    # Déterminer grade
    if score >= 80:
        grade = "A"
    elif score >= 60:
        grade = "B"
    elif score >= 40:
        grade = "C"
    else:
        grade = "D"
    
    return {
        "score": score,
        "grade": grade,
        "penalties": []
    }


@router.post("/{project_id}/capex/suggest")
async def suggest_capex(
    project_id: int,
    request_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """Suggère un montant CAPEX pour un projet"""
    from app.services.capex_service import CapexService
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    
    service = CapexService()
    suggestion = service.suggest_capex_budget(
        surface_m2=project.surface or 1000,
        typologie=request_data.get("typologie", "RENOVATION"),
        city_tier=request_data.get("city_tier", "TIER_1")
    )
    
    return {
        "suggested_amount": suggestion["suggested_budget"],
        "confidence": suggestion.get("confidence", "MEDIUM"),
        "breakdown": suggestion.get("breakdown", {})
    }


@router.get("/{project_id}/documents/missing")
async def get_missing_documents(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Liste les documents manquants pour un projet"""
    from app.services.document_service import DocumentService
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    
    service = DocumentService()
    missing = service.check_missing_documents(
        project_type=project.project_type or "rental",
        uploaded_docs=[]
    )
    
    return missing


@router.post("/{project_id}/business-plan/generate")
async def generate_business_plan(
    project_id: int,
    request_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """Génère un business plan pour un projet"""
    from app.services.financial_service import FinancialService
    
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    
    service = FinancialService()
    
    # Calculer IRR
    cash_flows = [-request_data.get("capex_total", 500000)]
    monthly_rent = request_data.get("monthly_rent", 10000)
    for _ in range(10):
        cash_flows.append(monthly_rent * 12)
    
    irr = service.calculate_irr(cash_flows)
    multiple = 2.5  # Placeholder
    
    return {
        "irr": irr,
        "multiple": multiple,
        "ltv": 0.65,
        "dscr": 1.3
    }
