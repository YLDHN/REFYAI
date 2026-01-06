from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.core.database import Base


class PhaseType(str, enum.Enum):
    """Types de phases du projet"""
    STUDIES = "studies"  # Études & conception
    PERMIT = "permit"  # Obtention permis
    CONSTRUCTION = "construction"  # Travaux
    COMMERCIALIZATION = "commercialization"  # Commercialisation
    
    def __str__(self):
        return self.value


class CurveType(str, enum.Enum):
    """Type de courbe de décaissement CAPEX"""
    LINEAR = "linear"  # Linéaire
    S_CURVE = "s_curve"  # Courbe en S (classique)
    FRONT_LOADED = "front_loaded"  # Chargé au début
    BACK_LOADED = "back_loaded"  # Chargé en fin
    
    def __str__(self):
        return self.value


class ProjectTimeline(Base):
    """
    Timeline complète d'un projet avec phases distinctes
    Permet de caler la trésorerie sur le calendrier réel
    """
    __tablename__ = "project_timelines"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, unique=True)
    
    # === PHASE ÉTUDES & CONCEPTION ===
    # Dépenses intellectuelles : Archi, BE, études de sol, etc.
    study_phase_start = Column(DateTime(timezone=True))
    study_phase_end = Column(DateTime(timezone=True))
    study_phase_budget = Column(Float, default=0)  # Budget études
    
    # === PHASE PERMIS ===
    # Instruction administrative, délais ABF, etc.
    permit_phase_start = Column(DateTime(timezone=True))
    permit_phase_end = Column(DateTime(timezone=True))
    permit_application_date = Column(DateTime(timezone=True))  # Date dépôt PC
    permit_expected_approval = Column(DateTime(timezone=True))  # Date prévisionnelle
    permit_fees = Column(Float, default=0)  # Taxes urbanisme
    
    # === PHASE TRAVAUX ===
    # Décaissement CAPEX principal
    construction_phase_start = Column(DateTime(timezone=True))
    construction_phase_end = Column(DateTime(timezone=True))
    construction_budget = Column(Float, default=0)  # CAPEX travaux
    capex_curve_type = Column(String, default="s_curve")  # Type de courbe
    
    # Jalons travaux (optionnel)
    construction_milestones = Column(JSON)  # [{name, date, budget_pct}]
    
    # === PHASE COMMERCIALISATION ===
    # Rentrées d'argent : VEFA, Location, Revente
    commercialization_phase_start = Column(DateTime(timezone=True))
    commercialization_phase_end = Column(DateTime(timezone=True))
    
    # Type de commercialisation
    commercialization_type = Column(String)  # "VEFA", "RENTAL", "RESALE", "MIXED"
    
    # Pour VEFA : Planning de réservations
    vefa_reservations_schedule = Column(JSON)  # [{month, pct_sold, cash_in}]
    
    # Pour Location : Date mise en location
    rental_start_date = Column(DateTime(timezone=True))
    
    # Pour Revente : Date de sortie
    resale_date = Column(DateTime(timezone=True))
    
    # === DATES CLÉS CALCULÉES ===
    # Calculées automatiquement
    project_start_date = Column(DateTime(timezone=True))  # = study_phase_start
    project_end_date = Column(DateTime(timezone=True))  # Date de sortie finale
    total_duration_months = Column(Integer)  # Durée totale en mois
    
    # === TRÉSORERIE ===
    # Cash-flow mensuel pré-calculé pour performances
    cashflow_schedule = Column(JSON)  # [{month, capex_out, revenue_in, net}]
    
    # === MÉTADONNÉES ===
    execution_mode = Column(String, default="sequential")  # "sequential" ou "parallel"
    notes = Column(String)  # Notes libres
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    # project = relationship("Project", back_populates="timeline")
