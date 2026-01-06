"""
Routes API pour analyse conformité documentaire
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.services.compliance_service import compliance_service, ProjectTypology

router = APIRouter(prefix="/documents", tags=["Documents Compliance"])


@router.get("/missing/{project_id}")
async def get_missing_documents(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    📄 Analyse documents manquants pour un projet
    
    Retourne:
    - Liste documents manquants par priorité
    - Score de complétude
    - Documents déjà présents
    - Alertes critiques
    - Next steps recommandés
    
    Exemple:
        GET /api/v1/documents/missing/123
    """
    result = await compliance_service.get_missing_documents(project_id, db)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@router.get("/required/{typologie}")
async def get_required_documents_by_typology(typologie: ProjectTypology):
    """
    📋 Liste documents requis pour une typologie
    
    Params:
        typologie: NEUF, RENOVATION, CONVERSION, MDB, VEFA, CONSTRUCTION
    
    Returns:
        Liste complète documents avec priorités
    
    Exemple:
        GET /api/v1/documents/required/RENOVATION
    """
    required_docs = compliance_service.get_required_docs_by_typology(typologie)
    
    # Grouper par catégorie
    by_category = {}
    for doc in required_docs:
        category = doc["category"]
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(doc)
    
    return {
        "success": True,
        "typologie": typologie.value,
        "total_documents": len(required_docs),
        "by_category": by_category,
        "by_priority": {
            "CRITICAL": [d for d in required_docs if d["priority"] == "CRITICAL"],
            "HIGH": [d for d in required_docs if d["priority"] == "HIGH"],
            "MEDIUM": [d for d in required_docs if d["priority"] == "MEDIUM"],
            "LOW": [d for d in required_docs if d["priority"] == "LOW"]
        }
    }
