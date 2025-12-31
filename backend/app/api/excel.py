from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models import Project
from app.services import excel_service, financial_service
from io import BytesIO

router = APIRouter(prefix="/excel", tags=["excel"])

@router.get("/{project_id}/generate")
async def generate_business_plan(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Générer le Business Plan Excel pour un projet"""
    
    # Récupérer le projet
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Projet non trouvé"
        )
    
    # Préparer les données du projet
    project_data = {
        "name": project.name,
        "address": project.address,
        "city": project.city,
        "project_type": project.project_type.value if project.project_type else "N/A"
    }
    
    # Calculer les données financières si disponibles
    if project.purchase_price and project.renovation_budget:
        financial_data = financial_service.calculate_full_analysis(
            purchase_price=project.purchase_price,
            renovation_budget=project.renovation_budget,
            notary_fees=project.purchase_price * 0.08,  # 8% de frais de notaire par défaut
            loan_amount=project.purchase_price * 0.8,  # 80% de LTV par défaut
            interest_rate=0.04,  # 4% par défaut
            loan_duration=20,  # 20 ans par défaut
            monthly_rent=0,
            resale_price=project.estimated_value or 0,
            project_type=project.project_type.value if project.project_type else "rental"
        )
    else:
        financial_data = {
            "tri": 0,
            "van": 0,
            "ltv": 0,
            "ltc": 0,
            "dscr": 0,
            "roi": 0,
            "purchase_price": project.purchase_price or 0,
            "renovation_budget": project.renovation_budget or 0,
            "notary_fees": 0,
            "interest_rate": 0.04,
            "loan_duration": 20
        }
    
    # Générer le fichier Excel
    try:
        excel_buffer = excel_service.generate_business_plan(
            project_data=project_data,
            financial_data=financial_data
        )
        
        # Retourner le fichier
        return Response(
            content=excel_buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=business_plan_{project.name.replace(' ', '_')}.xlsx"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération: {str(e)}"
        )
