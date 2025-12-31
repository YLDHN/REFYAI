from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class ProjectType(str, enum.Enum):
    RENTAL = "rental"  # Locatif
    RESALE = "resale"  # Revente
    MIXED = "mixed"    # Mixte

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Informations générales
    name = Column(String, nullable=False)
    description = Column(String)
    address = Column(String)
    city = Column(String)
    postal_code = Column(String)
    
    # Type et statut
    project_type = Column(Enum(ProjectType))
    status = Column(Enum(ProjectStatus), default=ProjectStatus.DRAFT)
    
    # Données financières
    purchase_price = Column(Float)
    renovation_budget = Column(Float)
    estimated_value = Column(Float)
    
    # Analyses (JSON pour flexibilité)
    regulatory_analysis = Column(JSON)  # Analyse PLU, urbanisme
    technical_analysis = Column(JSON)   # Analyse technique, risques
    financial_analysis = Column(JSON)   # TRI, LTV, DSCR, etc.
    
    # Scores
    technical_score = Column(Float)
    risk_score = Column(Float)
    
    # Métadonnées
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    # user = relationship("User", back_populates="projects")
    # documents = relationship("Document", back_populates="project")
