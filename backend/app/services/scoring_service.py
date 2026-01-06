"""
Service de scoring technique projet (/100)
Analyse risques urbanistiques, techniques, financiers
"""
from typing import Dict, List, Optional
from enum import Enum
from sqlalchemy.orm import Session
from app.models.project import Project


class RiskLevel(str, Enum):
    """Niveaux de risque"""
    CRITICAL = "CRITICAL"  # -25 points
    MAJOR = "MAJOR"  # -10 points
    MINOR = "MINOR"  # -5 points


class RiskCategory(str, Enum):
    """Catégories de risque"""
    URBANISME = "URBANISME"
    TECHNIQUE = "TECHNIQUE"
    FINANCIER = "FINANCIER"
    JURIDIQUE = "JURIDIQUE"
    ENVIRONNEMENTAL = "ENVIRONNEMENTAL"


class Risk:
    """Modèle risque détecté"""
    def __init__(
        self,
        key: str,
        label: str,
        category: RiskCategory,
        level: RiskLevel,
        penalty: int,
        description: str,
        mitigation: str = ""
    ):
        self.key = key
        self.label = label
        self.category = category
        self.level = level
        self.penalty = penalty
        self.description = description
        self.mitigation = mitigation


class TechnicalScoringService:
    """Service calcul score technique projet"""
    
    # === RÉFÉRENTIEL RISQUES ===
    
    # Pénalités par niveau
    PENALTIES = {
        RiskLevel.CRITICAL: -25,
        RiskLevel.MAJOR: -10,
        RiskLevel.MINOR: -5
    }
    
    # Règles de détection risques
    RISK_RULES = [
        # === URBANISME ===
        {
            "key": "abf_perimetre",
            "label": "Périmètre ABF (Architecte Bâtiments de France)",
            "category": RiskCategory.URBANISME,
            "level": RiskLevel.MAJOR,
            "check": lambda p: p.get("abf_zone", False),
            "description": "Projet en périmètre ABF : délais +6 mois, contraintes esthétiques fortes",
            "mitigation": "Prévoir 6 mois délais supplémentaires + architecte spécialisé patrimoine"
        },
        {
            "key": "secteur_sauvegarde",
            "label": "Secteur sauvegardé",
            "category": RiskCategory.URBANISME,
            "level": RiskLevel.CRITICAL,
            "check": lambda p: p.get("secteur_sauvegarde", False),
            "description": "Secteur sauvegardé : autorisations très restrictives",
            "mitigation": "Étude patrimoine préalable + autorisation spéciale préfecture"
        },
        {
            "key": "monument_historique_proximite",
            "label": "Proximité monument historique < 500m",
            "category": RiskCategory.URBANISME,
            "level": RiskLevel.MINOR,
            "check": lambda p: p.get("distance_monument_historique", 999) < 500,
            "description": "Contraintes visuelles possibles",
            "mitigation": "Consultation ABF recommandée"
        },
        {
            "key": "plu_zone_contrainte",
            "label": "Zone PLU à contraintes (N, A, Np)",
            "category": RiskCategory.URBANISME,
            "level": RiskLevel.MAJOR,
            "check": lambda p: p.get("plu_zone", "U") in ["N", "A", "Np"],
            "description": "Zone naturelle ou agricole : constructibilité limitée",
            "mitigation": "Vérifier dérogations possibles avec urbanisme mairie"
        },
        {
            "key": "coefficient_emprise_sol_depasse",
            "label": "CES (Coefficient Emprise Sol) dépassé",
            "category": RiskCategory.URBANISME,
            "level": RiskLevel.CRITICAL,
            "check": lambda p: p.get("ces_calcule", 0) > p.get("ces_max_autorise", 1),
            "description": "Surface construite dépasse CES autorisé",
            "mitigation": "Réduire surface projet ou demander dérogation"
        },
        
        # === TECHNIQUE ===
        {
            "key": "amiante_detecte",
            "label": "Présence amiante",
            "category": RiskCategory.TECHNIQUE,
            "level": RiskLevel.MAJOR,
            "check": lambda p: p.get("amiante_present", False),
            "description": "Désamiantage obligatoire : +15% budget, délais +2 mois",
            "mitigation": "Budget désamiantage : 30-80€/m2 + entreprise certifiée"
        },
        {
            "key": "plomb_detecte",
            "label": "Présence plomb",
            "category": RiskCategory.TECHNIQUE,
            "level": RiskLevel.MINOR,
            "check": lambda p: p.get("plomb_present", False),
            "description": "Travaux plomb : techniques spécifiques requises",
            "mitigation": "Confinement chantier + évacuation déchets spéciaux"
        },
        {
            "key": "structure_fragile",
            "label": "Structure porteuse fragile",
            "category": RiskCategory.TECHNIQUE,
            "level": RiskLevel.CRITICAL,
            "check": lambda p: p.get("structure_etat", "bon") == "fragile",
            "description": "Risque effondrement : renforcement structure majeur",
            "mitigation": "Bureau études structure + travaux confortement"
        },
        {
            "key": "dpe_g_passoire",
            "label": "DPE G (Passoire énergétique)",
            "category": RiskCategory.TECHNIQUE,
            "level": RiskLevel.MAJOR,
            "check": lambda p: p.get("dpe_classe", "D") == "G",
            "description": "Interdiction location dès 2025 : rénovation énergétique obligatoire",
            "mitigation": "Budget isolation + chauffage : 200-400€/m2"
        },
        {
            "key": "electricite_obsolete",
            "label": "Installation électrique obsolète",
            "category": RiskCategory.TECHNIQUE,
            "level": RiskLevel.MINOR,
            "check": lambda p: p.get("electricite_conforme", True) == False,
            "description": "Mise aux normes électriques requise",
            "mitigation": "Budget remise aux normes : 100-150€/m2"
        },
        
        # === FINANCIER ===
        {
            "key": "ltv_trop_eleve",
            "label": "LTV > 80% (Risque bancaire)",
            "category": RiskCategory.FINANCIER,
            "level": RiskLevel.MAJOR,
            "check": lambda p: p.get("ltv", 0) > 0.80,
            "description": "LTV élevé : difficultés financement bancaire",
            "mitigation": "Augmenter apport ou réduire montant emprunt"
        },
        {
            "key": "dscr_insuffisant",
            "label": "DSCR < 1.2 (Couverture dette insuffisante)",
            "category": RiskCategory.FINANCIER,
            "level": RiskLevel.CRITICAL,
            "check": lambda p: p.get("dscr", 2.0) < 1.2,
            "description": "Revenus insuffisants pour couvrir dette",
            "mitigation": "Réduire endettement ou augmenter loyers"
        },
        {
            "key": "tri_faible",
            "label": "TRI < 8% (Rentabilité faible)",
            "category": RiskCategory.FINANCIER,
            "level": RiskLevel.MINOR,
            "check": lambda p: p.get("tri", 0.15) < 0.08,
            "description": "TRI inférieur au seuil investisseur standard",
            "mitigation": "Optimiser coûts ou augmenter prix sortie"
        },
        {
            "key": "capex_budgete_faible",
            "label": "CAPEX < 70% médiane marché",
            "category": RiskCategory.FINANCIER,
            "level": RiskLevel.MAJOR,
            "check": lambda p: (
                p.get("capex_budgete", 0) < p.get("capex_median_marche", 0) * 0.70
                if p.get("capex_median_marche", 0) > 0 else False
            ),
            "description": "Budget travaux sous-évalué : risque dépassement",
            "mitigation": "Réévaluer budget avec 20% contingence"
        },
        
        # === JURIDIQUE ===
        {
            "key": "copropriete_contentieux",
            "label": "Copropriété en contentieux",
            "category": RiskCategory.JURIDIQUE,
            "level": RiskLevel.CRITICAL,
            "check": lambda p: p.get("copro_contentieux", False),
            "description": "Procédures judiciaires en cours dans copropriété",
            "mitigation": "Attendre résolution ou négocier décote prix"
        },
        {
            "key": "servitudes_contraignantes",
            "label": "Servitudes contraignantes présentes",
            "category": RiskCategory.JURIDIQUE,
            "level": RiskLevel.MINOR,
            "check": lambda p: p.get("servitudes_count", 0) > 2,
            "description": "Servitudes multiples limitant usage bien",
            "mitigation": "Analyse notaire + vérification levée servitudes"
        },
        
        # === ENVIRONNEMENTAL ===
        {
            "key": "zone_inondable",
            "label": "Zone inondable PPRI",
            "category": RiskCategory.ENVIRONNEMENTAL,
            "level": RiskLevel.CRITICAL,
            "check": lambda p: p.get("zone_inondable", False),
            "description": "PPRI : surprime assurance + contraintes construction",
            "mitigation": "Surélévation plancher + assurance spécifique"
        },
        {
            "key": "pollution_sol",
            "label": "Pollution sol détectée",
            "category": RiskCategory.ENVIRONNEMENTAL,
            "level": RiskLevel.CRITICAL,
            "check": lambda p: p.get("pollution_sol", False),
            "description": "Dépollution obligatoire : coûts majeurs",
            "mitigation": "Étude sol phase 2 + budget dépollution"
        },
        {
            "key": "radon_zone_3",
            "label": "Zone radon prioritaire (Zone 3)",
            "category": RiskCategory.ENVIRONNEMENTAL,
            "level": RiskLevel.MINOR,
            "check": lambda p: p.get("radon_zone", 1) == 3,
            "description": "Mesures radon + ventilation renforcée",
            "mitigation": "VMC double flux + mesure radon post-travaux"
        }
    ]
    
    def calculate_technical_score(
        self,
        project_data: Dict
    ) -> Dict:
        """
        Calcule score technique sur /100
        
        Args:
            project_data: Dict avec données projet (LTV, DSCR, TRI, etc.)
        
        Returns:
            Score + détails risques détectés
        """
        
        score = 100  # Score de départ
        detected_risks = []
        
        # Parcourir règles de détection
        for rule in self.RISK_RULES:
            try:
                # Tester condition
                if rule["check"](project_data):
                    # Risque détecté
                    penalty = self.PENALTIES[rule["level"]]
                    score += penalty  # Ajouter pénalité (négative)
                    
                    detected_risks.append({
                        "key": rule["key"],
                        "label": rule["label"],
                        "category": rule["category"].value,
                        "level": rule["level"].value,
                        "penalty": penalty,
                        "description": rule["description"],
                        "mitigation": rule["mitigation"]
                    })
            except Exception as e:
                # Ignorer si donnée manquante
                pass
        
        # Score minimum = 0
        score = max(0, score)
        
        # Classement global
        if score >= 80:
            rating = "EXCELLENT"
            color = "green"
        elif score >= 60:
            rating = "BON"
            color = "lightgreen"
        elif score >= 40:
            rating = "MOYEN"
            color = "orange"
        elif score >= 20:
            rating = "FAIBLE"
            color = "red"
        else:
            rating = "TRÈS FAIBLE"
            color = "darkred"
        
        # Grouper par catégorie
        risks_by_category = {}
        for risk in detected_risks:
            cat = risk["category"]
            if cat not in risks_by_category:
                risks_by_category[cat] = []
            risks_by_category[cat].append(risk)
        
        # Grouper par niveau
        risks_by_level = {
            "CRITICAL": [r for r in detected_risks if r["level"] == "CRITICAL"],
            "MAJOR": [r for r in detected_risks if r["level"] == "MAJOR"],
            "MINOR": [r for r in detected_risks if r["level"] == "MINOR"]
        }
        
        return {
            "success": True,
            "score": score,
            "rating": rating,
            "color": color,
            "max_score": 100,
            "total_risks": len(detected_risks),
            "risks": {
                "all": detected_risks,
                "by_category": risks_by_category,
                "by_level": risks_by_level
            },
            "penalties_breakdown": {
                "CRITICAL": sum(r["penalty"] for r in detected_risks if r["level"] == "CRITICAL"),
                "MAJOR": sum(r["penalty"] for r in detected_risks if r["level"] == "MAJOR"),
                "MINOR": sum(r["penalty"] for r in detected_risks if r["level"] == "MINOR")
            },
            "recommendations": self._get_recommendations(score, detected_risks)
        }
    
    def _get_recommendations(self, score: int, risks: List[Dict]) -> List[str]:
        """Génère recommandations basées sur score"""
        reco = []
        
        if score < 40:
            reco.append("⚠️ PROJET À HAUT RISQUE : Revoir viabilité ou prévoir mitigation majeure")
        
        critical_risks = [r for r in risks if r["level"] == "CRITICAL"]
        if critical_risks:
            reco.append(f"🚨 {len(critical_risks)} risques CRITIQUES à traiter en priorité")
        
        if any(r["category"] == "URBANISME" for r in risks):
            reco.append("📋 Consulter urbaniste/avocat droit public pour contraintes administratives")
        
        if any(r["category"] == "TECHNIQUE" for r in risks):
            reco.append("🔧 Audits techniques approfondis requis (structure, amiante, etc.)")
        
        if any(r["category"] == "FINANCIER" for r in risks):
            reco.append("💰 Retravailler montage financier (LTV, DSCR, rentabilité)")
        
        if score >= 80:
            reco.append("✅ Projet solide ! Peu de risques majeurs identifiés")
        
        return reco


# Instance globale
scoring_service = TechnicalScoringService()
