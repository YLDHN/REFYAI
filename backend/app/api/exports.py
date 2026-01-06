"""
Routes API pour génération dossier banque PDF
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.services.bank_package_service import bank_package_service

router = APIRouter(prefix="/exports", tags=["PDF Exports"])


@router.post("/bank-package/{project_id}")
async def generate_bank_package(
    project_id: int,
    include_documents: bool = True,
    db: Session = Depends(get_db)
):
    """
    📄 Génère dossier banque complet en PDF
    
    Contenu:
    1. Page de garde avec synthèse financière
    2. Résumé exécutif du projet
    3. Documents uploadés (si include_documents=true)
    
    Params:
        project_id: ID du projet
        include_documents: Inclure docs uploadés (défaut: true)
    
    Returns:
        Métadonnées PDF généré
    
    Exemple:
        POST /api/v1/exports/bank-package/123?include_documents=true
    """
    result = await bank_package_service.assemble_bank_package(
        project_id=project_id,
        db=db,
        include_documents=include_documents
    )
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@router.get("/bank-package/download/{filename}")
async def download_bank_package(filename: str):
    """
    ⬇️ Télécharge PDF dossier banque
    
    Params:
        filename: Nom fichier (retourné par /bank-package)
    
    Returns:
        Fichier PDF en téléchargement
    
    Exemple:
        GET /api/v1/exports/bank-package/download/dossier_banque_projet_123_20250102_143000.pdf
    """
    import os
    file_path = os.path.join("./exports/bank_packages", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )
