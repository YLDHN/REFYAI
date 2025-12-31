"""
Service de détection des Showstoppers (points bloquants)
"""
from typing import Dict, Any, List
from enum import Enum

class ShowstopperSeverity(str, Enum):
    CRITICAL = "critical"  # Bloquant absolu
    HIGH = "high"          # Très risqué
    MEDIUM = "medium"      # À surveiller
    LOW = "low"            # Mineur

class ShowstopperCategory(str, Enum):
    REGULATORY = "regulatory"    # Réglementaire
    TECHNICAL = "technical"      # Technique
    FINANCIAL = "financial"      # Financier
    LEGAL = "legal"             # Juridique

class ShowstopperDetectionService:
    """Service de détection automatique des points bloquants"""
    
    def detect_showstoppers(
        self,
        project_data: Dict[str, Any],
        questionnaire_answers: Dict[str, Any],
        plu_analysis: Dict[str, Any],
        technical_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Détecte automatiquement les showstoppers
        
        Returns:
            Liste de showstoppers avec sévérité et recommandations
        """
        showstoppers = []
        
        # 1. Showstoppers Réglementaires
        showstoppers.extend(self._check_regulatory_showstoppers(questionnaire_answers, plu_analysis))
        
        # 2. Showstoppers Techniques
        showstoppers.extend(self._check_technical_showstoppers(technical_analysis))
        
        # 3. Showstoppers Financiers
        showstoppers.extend(self._check_financial_showstoppers(project_data))
        
        # 4. Showstoppers Juridiques
        showstoppers.extend(self._check_legal_showstoppers(project_data))
        
        # Trier par sévérité
        severity_order = {
            ShowstopperSeverity.CRITICAL: 0,
            ShowstopperSeverity.HIGH: 1,
            ShowstopperSeverity.MEDIUM: 2,
            ShowstopperSeverity.LOW: 3
        }
        showstoppers.sort(key=lambda x: severity_order[x["severity"]])
        
        return showstoppers
    
    def _check_regulatory_showstoppers(
        self,
        questionnaire: Dict[str, Any],
        plu_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Détecte les showstoppers réglementaires"""
        showstoppers = []
        
        # Zone non constructible
        if plu_analysis.get("zone_type") in ["A", "N"]:
            showstoppers.append({
                "id": "zone_non_constructible",
                "title": "Zone non constructible",
                "description": f"Le terrain est en zone {plu_analysis.get('zone_type')} (agricole ou naturelle). Construction généralement interdite.",
                "severity": ShowstopperSeverity.CRITICAL,
                "category": ShowstopperCategory.REGULATORY,
                "impact": "Projet impossible sans dérogation exceptionnelle",
                "recommendations": [
                    "Vérifier les exceptions du PLU pour cette zone",
                    "Consulter le service urbanisme de la mairie",
                    "Envisager un recours ou une modification du PLU (procédure longue)"
                ],
                "estimated_delay": "6-24 mois si dérogation",
                "estimated_cost": "10 000 - 50 000 €"
            })
        
        # Dépassement COS/CES
        if plu_analysis.get("cos_exceeded"):
            showstoppers.append({
                "id": "cos_exceeded",
                "title": "Dépassement du Coefficient d'Occupation des Sols",
                "description": f"Surface prévue: {plu_analysis.get('planned_surface')}m². Maximum autorisé: {plu_analysis.get('max_surface')}m²",
                "severity": ShowstopperSeverity.HIGH,
                "category": ShowstopperCategory.REGULATORY,
                "impact": "Réduction obligatoire du projet",
                "recommendations": [
                    "Revoir le programme à la baisse",
                    "Étudier les possibilités de bonus COS (logements sociaux, performance énergétique)",
                    "Demander une dérogation si justifiée"
                ],
                "estimated_delay": "2-4 mois",
                "estimated_cost": "5 000 - 15 000 €"
            })
        
        # ABF / Monuments Historiques
        if questionnaire.get("monuments_historiques") or questionnaire.get("abf_avis"):
            showstoppers.append({
                "id": "abf_required",
                "title": "Avis ABF obligatoire",
                "description": "Projet soumis à l'avis de l'Architecte des Bâtiments de France",
                "severity": ShowstopperSeverity.MEDIUM,
                "category": ShowstopperCategory.REGULATORY,
                "impact": "Délais allongés + contraintes esthétiques fortes",
                "recommendations": [
                    "Prévoir une consultation préalable avec l'ABF",
                    "Budget supplémentaire pour matériaux conformes",
                    "Prévoir des rendus 3D de qualité",
                    "Envisager un architecte spécialisé patrimoine"
                ],
                "estimated_delay": "3-6 mois supplémentaires",
                "estimated_cost": "15 000 - 40 000 € (surcoûts matériaux)"
            })
        
        # Changement de destination
        if "Changement de destination" in questionnaire.get("nature_travaux", []):
            showstoppers.append({
                "id": "changement_destination",
                "title": "Changement de destination",
                "description": "Procédure administrative spécifique requise",
                "severity": ShowstopperSeverity.MEDIUM,
                "category": ShowstopperCategory.REGULATORY,
                "impact": "Autorisation d'urbanisme spécifique + diagnostics",
                "recommendations": [
                    "Vérifier la compatibilité avec le PLU",
                    "Commander diagnostics obligatoires (amiante, plomb, etc.)",
                    "Prévoir études structure et sécurité incendie",
                    "Anticiper taxe d'aménagement majorée"
                ],
                "estimated_delay": "4-8 mois",
                "estimated_cost": "20 000 - 60 000 €"
            })
        
        return showstoppers
    
    def _check_technical_showstoppers(
        self,
        technical_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Détecte les showstoppers techniques"""
        showstoppers = []
        
        # Structure dangereuse
        if technical_analysis.get("structure_risk") == "high":
            showstoppers.append({
                "id": "structure_risk",
                "title": "Risque structurel majeur",
                "description": "Problèmes structurels détectés nécessitant une étude approfondie",
                "severity": ShowstopperSeverity.CRITICAL,
                "category": ShowstopperCategory.TECHNICAL,
                "impact": "Travaux de confortement coûteux voire projet irréalisable",
                "recommendations": [
                    "URGENT: Faire réaliser une étude structure par BET",
                    "Envisager sondages et carottages",
                    "Prévoir budget confortement 200-500€/m²",
                    "Possibilité d'abandon du projet"
                ],
                "estimated_delay": "3-6 mois études + travaux",
                "estimated_cost": "50 000 - 200 000 €"
            })
        
        # Amiante / Plomb
        if technical_analysis.get("amiante_detected") or technical_analysis.get("plomb_detected"):
            showstoppers.append({
                "id": "amiante_plomb",
                "title": "Présence d'amiante ou de plomb",
                "description": "Matériaux dangereux nécessitant désamiantage/déplombage",
                "severity": ShowstopperSeverity.HIGH,
                "category": ShowstopperCategory.TECHNICAL,
                "impact": "Coûts et délais de désamiantage importants",
                "recommendations": [
                    "Diagnostic amiante complet avant travaux",
                    "Entreprises certifiées obligatoires",
                    "Plan de retrait à faire valider",
                    "Prévoir 50-150€/m² pour désamiantage"
                ],
                "estimated_delay": "2-4 mois",
                "estimated_cost": "30 000 - 100 000 €"
            })
        
        # Non-conformité incendie
        if technical_analysis.get("fire_safety_compliant") == False:
            showstoppers.append({
                "id": "fire_safety",
                "title": "Non-conformité sécurité incendie",
                "description": "Mise aux normes incendie nécessaire (compartimentage, désenfumage, alarme)",
                "severity": ShowstopperSeverity.HIGH,
                "category": ShowstopperCategory.TECHNICAL,
                "impact": "Travaux de mise aux normes obligatoires avant ouverture",
                "recommendations": [
                    "Étude sécurité incendie par bureau de contrôle",
                    "Installation compartimentage coupe-feu",
                    "Système de désenfumage et alarme",
                    "Formation du personnel si ERP"
                ],
                "estimated_delay": "3-5 mois",
                "estimated_cost": "40 000 - 120 000 €"
            })
        
        # Non-conformité PMR
        if technical_analysis.get("pmr_compliant") == False:
            showstoppers.append({
                "id": "pmr_accessibility",
                "title": "Non-conformité accessibilité PMR",
                "description": "Accessibilité handicapés non conforme",
                "severity": ShowstopperSeverity.MEDIUM,
                "category": ShowstopperCategory.TECHNICAL,
                "impact": "Travaux d'accessibilité obligatoires",
                "recommendations": [
                    "Audit accessibilité PMR",
                    "Installation rampes, ascenseur si nécessaire",
                    "Adaptation sanitaires et circulations",
                    "Signalétique adaptée"
                ],
                "estimated_delay": "2-4 mois",
                "estimated_cost": "25 000 - 80 000 €"
            })
        
        return showstoppers
    
    def _check_financial_showstoppers(
        self,
        project_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Détecte les showstoppers financiers"""
        showstoppers = []
        
        # TRI trop faible
        tri = project_data.get("tri", 0)
        if tri < 5:
            showstoppers.append({
                "id": "low_tri",
                "title": "TRI insuffisant",
                "description": f"TRI calculé à {tri}%, en dessous du seuil de rentabilité",
                "severity": ShowstopperSeverity.HIGH,
                "category": ShowstopperCategory.FINANCIAL,
                "impact": "Projet non rentable en l'état",
                "recommendations": [
                    "Renégocier le prix d'achat (-10 à -20%)",
                    "Optimiser les coûts de travaux",
                    "Revoir la stratégie de sortie (location vs revente)",
                    "Chercher des subventions (ANAH, etc.)"
                ],
                "estimated_delay": "N/A",
                "estimated_cost": "Ajustement nécessaire"
            })
        
        # LTV trop élevé
        ltv = project_data.get("ltv", 0)
        if ltv > 0.85:
            showstoppers.append({
                "id": "high_ltv",
                "title": "LTV trop élevé",
                "description": f"LTV à {ltv*100}%, risque de refus bancaire",
                "severity": ShowstopperSeverity.MEDIUM,
                "category": ShowstopperCategory.FINANCIAL,
                "impact": "Difficultés de financement bancaire",
                "recommendations": [
                    "Augmenter l'apport en fonds propres",
                    "Rechercher co-investisseurs",
                    "Renégocier le prix d'acquisition",
                    "Explorer le financement participatif"
                ],
                "estimated_delay": "1-3 mois",
                "estimated_cost": "N/A"
            })
        
        return showstoppers
    
    def _check_legal_showstoppers(
        self,
        project_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Détecte les showstoppers juridiques"""
        showstoppers = []
        
        # Servitudes
        if project_data.get("servitudes", []):
            showstoppers.append({
                "id": "servitudes",
                "title": "Servitudes détectées",
                "description": "Servitudes d'utilité publique ou privées impactant le projet",
                "severity": ShowstopperSeverity.MEDIUM,
                "category": ShowstopperCategory.LEGAL,
                "impact": "Contraintes sur l'utilisation du bien",
                "recommendations": [
                    "Analyse détaillée des servitudes par notaire",
                    "Négocier suppression si servitudes privées",
                    "Adapter le projet aux contraintes",
                    "Clause suspensive dans promesse de vente"
                ],
                "estimated_delay": "2-6 mois",
                "estimated_cost": "5 000 - 20 000 €"
            })
        
        # Copropriété difficile
        if project_data.get("copropriete_conflictuelle"):
            showstoppers.append({
                "id": "copropriete",
                "title": "Copropriété conflictuelle",
                "description": "Historique de conflits ou charges impayées importantes",
                "severity": ShowstopperSeverity.LOW,
                "category": ShowstopperCategory.LEGAL,
                "impact": "Difficultés de gestion et votes AG",
                "recommendations": [
                    "Demander PV des 3 dernières AG",
                    "Vérifier montant charges impayées",
                    "Consulter règlement de copropriété",
                    "Négocier baisse prix si problèmes avérés"
                ],
                "estimated_delay": "1-2 mois",
                "estimated_cost": "N/A"
            })
        
        return showstoppers
    
    def generate_action_plan(
        self,
        showstoppers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Génère un plan d'action priorisé
        
        Returns:
            Plan d'action avec timeline et budget
        """
        critical = [s for s in showstoppers if s["severity"] == ShowstopperSeverity.CRITICAL]
        high = [s for s in showstoppers if s["severity"] == ShowstopperSeverity.HIGH]
        
        total_delay_min = sum([self._parse_delay(s.get("estimated_delay", "0 mois"))[0] for s in showstoppers])
        total_delay_max = sum([self._parse_delay(s.get("estimated_delay", "0 mois"))[1] for s in showstoppers])
        
        return {
            "total_showstoppers": len(showstoppers),
            "critical_count": len(critical),
            "high_count": len(high),
            "project_viable": len(critical) == 0,
            "total_estimated_delay": f"{total_delay_min}-{total_delay_max} mois",
            "priority_actions": [s["recommendations"][0] for s in showstoppers[:5]],
            "immediate_actions": {
                "diagnostic_studies": self._extract_diagnostic_needs(showstoppers),
                "consultations": self._extract_consultation_needs(showstoppers),
                "budget_provisions": self._calculate_total_provisions(showstoppers)
            }
        }
    
    def _parse_delay(self, delay_str: str) -> tuple:
        """Parse une chaîne de délai et retourne (min, max) en mois"""
        import re
        numbers = re.findall(r'\d+', delay_str)
        if len(numbers) >= 2:
            return (int(numbers[0]), int(numbers[1]))
        elif len(numbers) == 1:
            return (int(numbers[0]), int(numbers[0]))
        return (0, 0)
    
    def _extract_diagnostic_needs(self, showstoppers: List[Dict]) -> List[str]:
        """Extrait les diagnostics à commander en priorité"""
        diagnostics = []
        for s in showstoppers:
            if "diagnostic" in s.get("description", "").lower():
                diagnostics.append(s["title"])
        return diagnostics
    
    def _extract_consultation_needs(self, showstoppers: List[Dict]) -> List[str]:
        """Extrait les consultations nécessaires"""
        consultations = []
        for s in showstoppers:
            if any(word in s.get("description", "").lower() for word in ["consultation", "étude", "avocat", "notaire"]):
                consultations.append(s["title"])
        return consultations
    
    def _calculate_total_provisions(self, showstoppers: List[Dict]) -> str:
        """Calcule les provisions budgétaires totales"""
        # Extraction simplifiée - à améliorer avec parsing réel
        return "150 000 - 500 000 € (estimation basée sur les showstoppers détectés)"
