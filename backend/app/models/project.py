from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

import enum
from app.core.database import Base

class ProjectStatus(str, enum.Enum):
    """Status du projet selon Business Plan (8 états)"""
    ANALYZING = "analyzing"  # En cours d'analyse
    NEGOTIATING = "negotiating"  # En cours de négo
    OFFER_SENT = "offer_sent"  # Offre envoyée
    FINANCING_SEARCH = "financing_search"  # Financement à chercher
    DUE_DILIGENCE = "due_diligence"  # Due diligence
    UNDER_CONTRACT = "under_contract"  # Sous promesse
    ACQUIRED = "acquired"  # Acquis
    REJECTED = "rejected"  # Refusé
    
    # Anciens statuts conservés pour compatibilité
    DRAFT = "draft"  # Brouillon (mapping → analyzing)
    IN_PROGRESS = "in_progress"  # En cours (mapping → negotiating)
    COMPLETED = "completed"  # Terminé (mapping → acquired)
    ARCHIVED = "archived"  # Archivé
    
    def __str__(self):
        return self.value

class ProjectType(str, enum.Enum):
    RENTAL = "rental"  # Locatif
    RESALE = "resale"  # Revente
    MIXED = "mixed"    # Mixte
    
    def __str__(self):
        return self.value

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
    project_type = Column(String)
    status = Column(String, default="draft")
    
    # Nouveaux champs client
    strategy = Column(String)  # core, core_plus, value_add
    bp_duration = Column(Integer)  # Durée BP en années
    asset_type = Column(String)  # residential, office, logistics, retail, mixed
    surface = Column(Float)  # Surface en m²
    
    # Données financières de base
    purchase_price = Column(Float)
    renovation_budget = Column(Float)
    estimated_value = Column(Float)
    
    # Données locatives
    lease_start_date = Column(DateTime(timezone=True))
    walb = Column(Float)  # Weighted Average Lease Break
    walt = Column(Float)  # Weighted Average Lease Term
    current_rent = Column(Float)  # Loyer en place annuel
    market_rent = Column(Float)  # VLM
    occupancy_rate = Column(Float)  # Taux d'occupation %
    lease_state = Column(JSON)  # État locatif détaillé
    
    # === ASSET MANAGEMENT (NOUVEAU) ===
    # Franchise de loyer (Rent Free)
    rent_free_months = Column(Integer, default=0)  # Nombre de mois sans loyer
    
    # Tenant Improvements (Travaux preneur)
    tenant_improvements = Column(Float, default=0)  # Contribution bailleur aux travaux locataire
    
    # Indexation des loyers
    indexation_type = Column(String, default="ILAT")  # ICC, ILAT, ILC, FIXED
    indexation_rate = Column(Float)  # Taux d'indexation annuel (si None, utilise historique)
    indexation_start_year = Column(Integer, default=2)  # Année de début indexation
    last_indexation_date = Column(DateTime(timezone=True))  # Dernière indexation appliquée
    
    # Data acquisition
    acquisition_price = Column(Float)
    notary_fees = Column(Float)
    due_diligence_cost = Column(Float)
    acquisition_yield = Column(Float)
    
    # Renouvellement et CAPEX
    rent_renewal_assumptions = Column(JSON)
    capex_details = Column(JSON)
    budget_total = Column(Float)  # Budget total (acquisition + travaux + frais) - BP
    
    # Financement
    financing_amount = Column(Float)
    ltv = Column(Float)
    interest_rate = Column(Float)
    loan_duration = Column(Integer)
    
    # Analyses (JSON pour flexibilité)
    regulatory_analysis = Column(JSON)
    technical_analysis = Column(JSON)
    financial_analysis = Column(JSON)
    
    # Scores
    technical_score = Column(Float)
    risk_score = Column(Float)
    
    # Métadonnées
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    # user = relationship("User", back_populates="projects")
    # documents = relationship("Document", back_populates="project")
