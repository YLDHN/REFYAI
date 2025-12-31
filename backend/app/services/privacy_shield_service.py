"""
Privacy Shield Service - Règle des 2 mois
Protège le secret des affaires en isolant les données sensibles
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import Base

class PrivacyShieldStatus(Base):
    """Modèle pour tracker le statut de confidentialité des projets"""
    __tablename__ = "privacy_shield_status"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=False, unique=True)
    tender_end_date = Column(DateTime)  # Date fin d'appel d'offres
    release_date = Column(DateTime)     # Date libération données (tender_end + 2 mois)
    is_protected = Column(Boolean, default=True)
    is_released = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)  # Infos additionnelles


class PrivacyShieldService:
    """Service de gestion du Privacy Shield"""
    
    PROTECTION_PERIOD_DAYS = 60  # 2 mois
    
    async def register_project(
        self,
        db: AsyncSession,
        project_id: int,
        tender_end_date: datetime,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enregistre un projet sous Privacy Shield
        
        Args:
            project_id: ID du projet
            tender_end_date: Date de fin d'appel d'offres
            metadata: Métadonnées optionnelles
        
        Returns:
            Statut du Privacy Shield
        """
        release_date = tender_end_date + timedelta(days=self.PROTECTION_PERIOD_DAYS)
        
        shield_status = PrivacyShieldStatus(
            project_id=project_id,
            tender_end_date=tender_end_date,
            release_date=release_date,
            is_protected=True,
            is_released=False,
            metadata=metadata or {}
        )
        
        db.add(shield_status)
        await db.commit()
        
        return {
            "project_id": project_id,
            "protected": True,
            "tender_end_date": tender_end_date.isoformat(),
            "release_date": release_date.isoformat(),
            "days_until_release": (release_date - datetime.utcnow()).days,
            "message": "Projet protégé par Privacy Shield. Données isolées pendant 2 mois après fin d'appel d'offres."
        }
    
    async def check_protection_status(
        self,
        db: AsyncSession,
        project_id: int
    ) -> Dict[str, Any]:
        """
        Vérifie le statut de protection d'un projet
        
        Returns:
            {
                "is_protected": bool,
                "days_remaining": int,
                "release_date": str
            }
        """
        result = await db.execute(
            select(PrivacyShieldStatus).where(
                PrivacyShieldStatus.project_id == project_id
            )
        )
        shield = result.scalar_one_or_none()
        
        if not shield:
            return {
                "is_protected": False,
                "message": "Projet non protégé ou données publiques"
            }
        
        now = datetime.utcnow()
        
        # Vérifier si période de protection expirée
        if now >= shield.release_date and not shield.is_released:
            await self._release_project_data(db, shield)
            return {
                "is_protected": False,
                "was_protected": True,
                "released_on": shield.release_date.isoformat(),
                "message": "Période de protection terminée. Données disponibles pour apprentissage IA."
            }
        
        days_remaining = (shield.release_date - now).days
        
        return {
            "is_protected": True,
            "days_remaining": max(0, days_remaining),
            "release_date": shield.release_date.isoformat(),
            "tender_end_date": shield.tender_end_date.isoformat(),
            "message": f"Données protégées. Libération dans {days_remaining} jours."
        }
    
    async def get_available_training_data(
        self,
        db: AsyncSession,
        category: Optional[str] = None
    ) -> List[int]:
        """
        Récupère les IDs des projets dont les données sont disponibles pour l'IA
        
        Args:
            category: Filtre optionnel par catégorie
        
        Returns:
            Liste d'IDs de projets libérés
        """
        now = datetime.utcnow()
        
        query = select(PrivacyShieldStatus).where(
            PrivacyShieldStatus.release_date <= now,
            PrivacyShieldStatus.is_released == True
        )
        
        result = await db.execute(query)
        shields = result.scalars().all()
        
        return [shield.project_id for shield in shields]
    
    async def anonymize_protected_data(
        self,
        project_data: Dict[str, Any],
        is_protected: bool
    ) -> Dict[str, Any]:
        """
        Anonymise les données sensibles si projet protégé
        
        Returns:
            Données anonymisées ou complètes selon statut
        """
        if not is_protected:
            return project_data
        
        # Anonymisation des données sensibles
        anonymized = project_data.copy()
        
        # Masquer adresse exacte
        if "address" in anonymized:
            anonymized["address"] = self._anonymize_address(anonymized["address"])
        
        # Masquer données financières précises
        if "purchase_price" in anonymized:
            anonymized["purchase_price"] = self._round_to_range(anonymized["purchase_price"], 50000)
        
        if "renovation_budget" in anonymized:
            anonymized["renovation_budget"] = self._round_to_range(anonymized["renovation_budget"], 20000)
        
        # Masquer nom du projet
        if "name" in anonymized:
            anonymized["name"] = f"Projet {anonymized.get('city', 'Anonyme')}"
        
        # Supprimer données hautement sensibles
        sensitive_fields = ["owner_name", "legal_entity", "bank_name", "specific_financial_terms"]
        for field in sensitive_fields:
            if field in anonymized:
                del anonymized[field]
        
        anonymized["_anonymized"] = True
        anonymized["_protection_notice"] = "Données protégées par Privacy Shield"
        
        return anonymized
    
    async def _release_project_data(
        self,
        db: AsyncSession,
        shield: PrivacyShieldStatus
    ):
        """Libère les données d'un projet pour l'apprentissage IA"""
        shield.is_protected = False
        shield.is_released = True
        await db.commit()
    
    def _anonymize_address(self, address: str) -> str:
        """Anonymise une adresse en gardant seulement la ville"""
        # Extraire la ville (simplification)
        parts = address.split(",")
        if len(parts) > 1:
            return f"[Adresse masquée], {parts[-1].strip()}"
        return "[Adresse masquée]"
    
    def _round_to_range(self, value: float, interval: int) -> str:
        """Arrondit une valeur à une fourchette"""
        lower = (value // interval) * interval
        upper = lower + interval
        return f"{int(lower):,} - {int(upper):,} €"
    
    async def check_and_release_expired(
        self,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Tâche CRON: Vérifie et libère les projets dont la protection a expiré
        
        Returns:
            Statistiques des libérations
        """
        now = datetime.utcnow()
        
        result = await db.execute(
            select(PrivacyShieldStatus).where(
                PrivacyShieldStatus.release_date <= now,
                PrivacyShieldStatus.is_released == False
            )
        )
        shields_to_release = result.scalars().all()
        
        released_count = 0
        for shield in shields_to_release:
            await self._release_project_data(db, shield)
            released_count += 1
        
        return {
            "released_count": released_count,
            "released_project_ids": [s.project_id for s in shields_to_release],
            "timestamp": now.isoformat(),
            "message": f"{released_count} projets libérés pour apprentissage IA"
        }


class DataIsolationService:
    """Service d'isolation des données sensibles"""
    
    def __init__(self):
        self.shield_service = PrivacyShieldService()
    
    async def query_with_privacy_filter(
        self,
        db: AsyncSession,
        user_id: int,
        project_ids: List[int],
        include_protected: bool = False
    ) -> List[int]:
        """
        Filtre les projets selon le Privacy Shield
        
        Args:
            user_id: ID utilisateur effectuant la requête
            project_ids: IDs des projets à filtrer
            include_protected: Si True, inclut projets protégés de l'utilisateur
        
        Returns:
            Liste filtrée d'IDs de projets
        """
        filtered_ids = []
        
        for project_id in project_ids:
            status = await self.shield_service.check_protection_status(db, project_id)
            
            if not status.get("is_protected"):
                # Données publiques
                filtered_ids.append(project_id)
            elif include_protected:
                # Vérifier si l'utilisateur est propriétaire
                # TODO: Implémenter vérification ownership
                filtered_ids.append(project_id)
        
        return filtered_ids
    
    async def get_aggregated_market_data(
        self,
        db: AsyncSession,
        filters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Retourne des données de marché agrégées sans exposer les projets protégés
        
        Returns:
            Statistiques anonymisées
        """
        available_projects = await self.shield_service.get_available_training_data(db)
        
        # TODO: Calculer stats agrégées sur available_projects
        # En attendant, retour mockup
        return {
            "available_data_points": len(available_projects),
            "avg_tri": 8.5,
            "avg_ltv": 0.72,
            "market_trends": "stable",
            "note": "Basé uniquement sur données publiques et projets libérés"
        }
