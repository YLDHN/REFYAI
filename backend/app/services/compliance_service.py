"""
Service de conformité documentaire
Analyse documents manquants selon typologie projet
"""
from typing import Dict, List, Optional
from enum import Enum
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.document import Document


class ProjectTypology(str, Enum):
    """Types de projets immobiliers"""
    NEUF = "NEUF"
    RENOVATION = "RENOVATION"
    CONVERSION = "CONVERSION"
    MDB = "MDB"
    VEFA = "VEFA"
    CONSTRUCTION = "CONSTRUCTION"


class DocumentPriority(str, Enum):
    """Priorités documents"""
    CRITICAL = "CRITICAL"  # Obligatoire avant financement
    HIGH = "HIGH"  # Nécessaire pour dossier banque
    MEDIUM = "MEDIUM"  # Recommandé
    LOW = "LOW"  # Optionnel


class DocumentCategory(str, Enum):
    """Catégories documents"""
    LEGAL = "LEGAL"
    TECHNICAL = "TECHNICAL"
    URBANISME = "URBANISME"
    FINANCIAL = "FINANCIAL"
    ENVIRONMENTAL = "ENVIRONMENTAL"


class RequiredDocument:
    """Modèle document requis"""
    def __init__(
        self,
        key: str,
        label: str,
        category: DocumentCategory,
        priority: DocumentPriority,
        typologies: List[ProjectTypology],
        description: str = "",
        validity_months: Optional[int] = None
    ):
        self.key = key
        self.label = label
        self.category = category
        self.priority = priority
        self.typologies = typologies
        self.description = description
        self.validity_months = validity_months


class DocumentComplianceService:
    """Service analyse conformité documentaire"""
    
    # === RÉFÉRENTIEL DOCUMENTS ===
    REQUIRED_DOCUMENTS = [
        # === LEGAL ===
        RequiredDocument(
            key="titre_propriete",
            label="Titre de propriété",
            category=DocumentCategory.LEGAL,
            priority=DocumentPriority.CRITICAL,
            typologies=[ProjectTypology.NEUF, ProjectTypology.RENOVATION, ProjectTypology.MDB],
            description="Acte notarié de propriété ou promesse de vente signée"
        ),
        RequiredDocument(
            key="etat_hypothecaire",
            label="État hypothécaire",
            category=DocumentCategory.LEGAL,
            priority=DocumentPriority.CRITICAL,
            typologies=[ProjectTypology.NEUF, ProjectTypology.RENOVATION, ProjectTypology.MDB],
            description="État des inscriptions hypothécaires < 3 mois",
            validity_months=3
        ),
        RequiredDocument(
            key="reglement_copropriete",
            label="Règlement de copropriété",
            category=DocumentCategory.LEGAL,
            priority=DocumentPriority.HIGH,
            typologies=[ProjectTypology.RENOVATION, ProjectTypology.MDB],
            description="Règlement + état descriptif de division"
        ),
        RequiredDocument(
            key="pv_ag_copro",
            label="PV AG copropriété (3 dernières)",
            category=DocumentCategory.LEGAL,
            priority=DocumentPriority.MEDIUM,
            typologies=[ProjectTypology.RENOVATION, ProjectTypology.MDB],
            description="Procès-verbaux assemblées générales"
        ),
        
        # === TECHNIQUE ===
        RequiredDocument(
            key="dpe",
            label="DPE (Diagnostic Performance Énergétique)",
            category=DocumentCategory.TECHNICAL,
            priority=DocumentPriority.CRITICAL,
            typologies=[ProjectTypology.RENOVATION, ProjectTypology.MDB],
            description="DPE valide < 10 ans",
            validity_months=120
        ),
        RequiredDocument(
            key="diagnostic_amiante",
            label="Diagnostic Amiante",
            category=DocumentCategory.TECHNICAL,
            priority=DocumentPriority.CRITICAL,
            typologies=[ProjectTypology.RENOVATION, ProjectTypology.MDB],
            description="Obligatoire si construction avant 1997"
        ),
        RequiredDocument(
            key="diagnostic_plomb",
            label="Diagnostic Plomb (CREP)",
            category=DocumentCategory.TECHNICAL,
            priority=DocumentPriority.CRITICAL,
            typologies=[ProjectTypology.RENOVATION, ProjectTypology.MDB],
            description="Obligatoire si construction avant 1949"
        ),
        RequiredDocument(
            key="diagnostic_termites",
            label="Diagnostic Termites",
            category=DocumentCategory.TECHNICAL,
            priority=DocumentPriority.HIGH,
            typologies=[ProjectTypology.RENOVATION, ProjectTypology.MDB],
            description="Si zone déclarée à risque",
            validity_months=6
        ),
        RequiredDocument(
            key="diagnostic_electricite",
            label="Diagnostic Électricité",
            category=DocumentCategory.TECHNICAL,
            priority=DocumentPriority.HIGH,
            typologies=[ProjectTypology.RENOVATION, ProjectTypology.MDB],
            description="Si installation > 15 ans",
            validity_months=36
        ),
        RequiredDocument(
            key="diagnostic_gaz",
            label="Diagnostic Gaz",
            category=DocumentCategory.TECHNICAL,
            priority=DocumentPriority.HIGH,
            typologies=[ProjectTypology.RENOVATION, ProjectTypology.MDB],
            description="Si installation > 15 ans",
            validity_months=36
        ),
        RequiredDocument(
            key="mesurage_loi_carrez",
            label="Mesurage Loi Carrez",
            category=DocumentCategory.TECHNICAL,
            priority=DocumentPriority.CRITICAL,
            typologies=[ProjectTypology.RENOVATION, ProjectTypology.MDB],
            description="Superficie privative en copropriété"
        ),
        
        # === URBANISME ===
        RequiredDocument(
            key="permis_construire",
            label="Permis de construire",
            category=DocumentCategory.URBANISME,
            priority=DocumentPriority.CRITICAL,
            typologies=[ProjectTypology.NEUF, ProjectTypology.CONSTRUCTION, ProjectTypology.CONVERSION],
            description="PC purgé de recours + attestation non-recours"
        ),
        RequiredDocument(
            key="declaration_prealable",
            label="Déclaration préalable",
            category=DocumentCategory.URBANISME,
            priority=DocumentPriority.CRITICAL,
            typologies=[ProjectTypology.RENOVATION],
            description="Si travaux modifiant aspect extérieur"
        ),
        RequiredDocument(
            key="certificat_urbanisme",
            label="Certificat d'urbanisme",
            category=DocumentCategory.URBANISME,
            priority=DocumentPriority.HIGH,
            typologies=[ProjectTypology.NEUF, ProjectTypology.CONSTRUCTION],
            description="CU opérationnel < 18 mois",
            validity_months=18
        ),
        RequiredDocument(
            key="plan_local_urbanisme",
            label="PLU / Règlement de zone",
            category=DocumentCategory.URBANISME,
            priority=DocumentPriority.HIGH,
            typologies=[ProjectTypology.NEUF, ProjectTypology.CONSTRUCTION, ProjectTypology.CONVERSION],
            description="Extrait PLU + règlement applicable"
        ),
        RequiredDocument(
            key="servitudes_utilite_publique",
            label="Servitudes d'utilité publique",
            category=DocumentCategory.URBANISME,
            priority=DocumentPriority.MEDIUM,
            typologies=[ProjectTypology.NEUF, ProjectTypology.CONSTRUCTION],
            description="Liste SUP affectant parcelle"
        ),
        
        # === FINANCIER ===
        RequiredDocument(
            key="business_plan",
            label="Business Plan détaillé",
            category=DocumentCategory.FINANCIAL,
            priority=DocumentPriority.CRITICAL,
            typologies=[ProjectTypology.NEUF, ProjectTypology.RENOVATION, ProjectTypology.CONVERSION],
            description="Excel avec TRI, VAN, cash-flows"
        ),
        RequiredDocument(
            key="budget_travaux",
            label="Budget travaux détaillé",
            category=DocumentCategory.FINANCIAL,
            priority=DocumentPriority.CRITICAL,
            typologies=[ProjectTypology.RENOVATION, ProjectTypology.CONVERSION],
            description="Devis artisans ou métré TCE"
        ),
        RequiredDocument(
            key="etude_commercialisation",
            label="Étude de commercialisation",
            category=DocumentCategory.FINANCIAL,
            priority=DocumentPriority.HIGH,
            typologies=[ProjectTypology.NEUF, ProjectTypology.VEFA],
            description="Prix m2, délais, comparables"
        ),
        
        # === ENVIRONNEMENTAL ===
        RequiredDocument(
            key="etude_sol_g2",
            label="Étude de sol G2",
            category=DocumentCategory.ENVIRONMENTAL,
            priority=DocumentPriority.CRITICAL,
            typologies=[ProjectTypology.NEUF, ProjectTypology.CONSTRUCTION],
            description="Étude géotechnique conception"
        ),
        RequiredDocument(
            key="zonage_inondation",
            label="Zonage risque inondation",
            category=DocumentCategory.ENVIRONMENTAL,
            priority=DocumentPriority.HIGH,
            typologies=[ProjectTypology.NEUF, ProjectTypology.CONSTRUCTION],
            description="Extrait Géorisques + PPRI"
        ),
        RequiredDocument(
            key="radon",
            label="Mesure Radon",
            category=DocumentCategory.ENVIRONMENTAL,
            priority=DocumentPriority.MEDIUM,
            typologies=[ProjectTypology.RENOVATION, ProjectTypology.MDB],
            description="Si zone 3 (prioritaire)"
        ),
    ]
    
    async def get_missing_documents(
        self,
        project_id: int,
        db: Session
    ) -> Dict:
        """
        Analyse documents manquants pour un projet
        
        Args:
            project_id: ID projet
            db: Session SQLAlchemy
        
        Returns:
            Dict avec liste documents manquants + analyse
        """
        
        # Récupérer projet
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {"error": "Projet introuvable"}
        
        # Déterminer typologie
        typologie = ProjectTypology(project.typologie) if project.typologie else ProjectTypology.RENOVATION
        
        # Documents requis pour cette typologie
        required_docs = [
            doc for doc in self.REQUIRED_DOCUMENTS
            if typologie in doc.typologies
        ]
        
        # Documents déjà uploadés
        uploaded_docs = db.query(Document).filter(
            Document.project_id == project_id
        ).all()
        
        uploaded_keys = {doc.document_type for doc in uploaded_docs}
        
        # Documents manquants
        missing_docs = []
        present_docs = []
        
        for req_doc in required_docs:
            if req_doc.key not in uploaded_keys:
                missing_docs.append({
                    "key": req_doc.key,
                    "label": req_doc.label,
                    "category": req_doc.category.value,
                    "priority": req_doc.priority.value,
                    "description": req_doc.description,
                    "validity_months": req_doc.validity_months
                })
            else:
                present_docs.append({
                    "key": req_doc.key,
                    "label": req_doc.label,
                    "category": req_doc.category.value
                })
        
        # Calcul score complétude
        total_required = len(required_docs)
        total_present = len(present_docs)
        completion_rate = (total_present / total_required * 100) if total_required > 0 else 0
        
        # Documents CRITICAL manquants
        critical_missing = [
            doc for doc in missing_docs
            if doc["priority"] == DocumentPriority.CRITICAL.value
        ]
        
        # Statut global
        if len(critical_missing) == 0 and completion_rate == 100:
            status = "COMPLETE"
        elif len(critical_missing) == 0:
            status = "ACCEPTABLE"
        else:
            status = "INCOMPLETE"
        
        return {
            "success": True,
            "project_id": project_id,
            "typologie": typologie.value,
            "status": status,
            "completion": {
                "rate": round(completion_rate, 1),
                "present": total_present,
                "required": total_required,
                "missing": len(missing_docs)
            },
            "documents": {
                "missing": missing_docs,
                "present": present_docs
            },
            "alerts": {
                "critical_missing": len(critical_missing),
                "high_missing": len([d for d in missing_docs if d["priority"] == "HIGH"]),
                "blocking": len(critical_missing) > 0
            },
            "next_steps": self._get_next_steps(missing_docs, critical_missing)
        }
    
    def _get_next_steps(self, missing_docs: List[Dict], critical_missing: List[Dict]) -> List[str]:
        """Génère recommandations next steps"""
        steps = []
        
        if len(critical_missing) > 0:
            steps.append(f"🚨 URGENT : {len(critical_missing)} documents CRITIQUES manquants")
            steps.append(f"→ Priorité : {', '.join([d['label'] for d in critical_missing[:3]])}")
        
        if any(d['category'] == 'TECHNICAL' for d in missing_docs):
            steps.append("📋 Commander diagnostics techniques auprès diagnostiqueur certifié")
        
        if any(d['category'] == 'URBANISME' for d in missing_docs):
            steps.append("🏛️ Consulter service urbanisme mairie pour documents administratifs")
        
        if any(d['category'] == 'FINANCIAL' for d in missing_docs):
            steps.append("💰 Finaliser business plan et budgets pour présentation banque")
        
        if len(missing_docs) == 0:
            steps.append("✅ Dossier complet ! Prêt pour présentation banque")
        
        return steps
    
    def get_required_docs_by_typology(self, typologie: ProjectTypology) -> List[Dict]:
        """Retourne liste documents requis pour une typologie"""
        required = [
            {
                "key": doc.key,
                "label": doc.label,
                "category": doc.category.value,
                "priority": doc.priority.value,
                "description": doc.description,
                "validity_months": doc.validity_months
            }
            for doc in self.REQUIRED_DOCUMENTS
            if typologie in doc.typologies
        ]
        
        return required


# Instance globale
compliance_service = DocumentComplianceService()
