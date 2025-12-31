from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class DocumentType(str, enum.Enum):
    PLU = "plu"
    DIAGNOSTIC = "diagnostic"
    CADASTRE = "cadastre"
    PHOTOS = "photos"
    PLANS = "plans"
    OTHER = "other"

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Informations du document
    filename = Column(String, nullable=False)
    original_filename = Column(String)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String)
    
    # Type et catégorie
    document_type = Column(Enum(DocumentType))
    
    # Analyse IA
    is_analyzed = Column(Integer, default=0)  # Boolean
    analysis_result = Column(String)  # JSON en texte
    
    # Métadonnées
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    # project = relationship("Project", back_populates="documents")
