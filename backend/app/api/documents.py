from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models import Document, DocumentType, Project
from app.services import ai_service
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
import shutil
import uuid
from app.core.config import settings

router = APIRouter(prefix="/documents", tags=["documents"])

# Créer le dossier uploads s'il n'existe pas
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

# Schémas
class DocumentResponse(BaseModel):
    id: int
    project_id: int
    filename: str
    original_filename: str | None
    file_size: int | None
    mime_type: str | None
    document_type: DocumentType | None
    is_analyzed: int
    analysis_result: str | None
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/{project_id}/upload", response_model=DocumentResponse)
async def upload_document(
    project_id: int,
    file: UploadFile = File(...),
    document_type: DocumentType = DocumentType.OTHER,
    db: AsyncSession = Depends(get_db)
):
    """Upload un document pour un projet"""
    
    # Vérifier que le projet existe
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )
    
    # Vérifier la taille du fichier
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Fichier trop volumineux (max {settings.MAX_UPLOAD_SIZE / (1024*1024)}MB)"
        )
    
    # Générer un nom de fichier unique
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = Path(settings.UPLOAD_DIR) / unique_filename
    
    # Sauvegarder le fichier
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Créer l'entrée en base de données
    document = Document(
        project_id=project_id,
        filename=unique_filename,
        original_filename=file.filename,
        file_path=str(file_path),
        file_size=file_size,
        mime_type=file.content_type,
        document_type=document_type,
        is_analyzed=0
    )
    
    db.add(document)
    await db.commit()
    await db.refresh(document)
    
    return document

@router.get("/{project_id}", response_model=list[DocumentResponse])
async def list_documents(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Lister les documents d'un projet"""
    
    result = await db.execute(
        select(Document).where(Document.project_id == project_id)
    )
    documents = result.scalars().all()
    
    return documents

@router.post("/{document_id}/analyze")
async def analyze_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Analyser un document avec l'IA"""
    
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé"
        )
    
    # Extraire le texte du document
    try:
        from app.services.document_extraction_service import document_extraction_service
        
        with open(document.file_path, "rb") as f:
            file_bytes = f.read()
        
        document_text = document_extraction_service.extract_text(
            file_bytes, 
            document.mime_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'extraction du texte: {str(e)}"
        )
    
    # Analyser avec l'IA
    analysis = await ai_service.analyze_document(
        text=document_text,
        document_type=document.document_type.value if document.document_type else "default"
    )
    
    # Mettre à jour le document
    document.is_analyzed = 1
    document.analysis_result = str(analysis)
    
    await db.commit()
    
    return {
        "message": "Document analysé avec succès",
        "analysis": analysis
    }

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Supprimer un document"""
    
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé"
        )
    
    # Supprimer le fichier physique
    file_path = Path(document.file_path)
    if file_path.exists():
        file_path.unlink()
    
    # Supprimer de la base de données
    await db.delete(document)
    await db.commit()
    
    return None
