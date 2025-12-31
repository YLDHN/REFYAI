"""
Service de questionnaire de localisation pour filtrage PLU précis
"""
from typing import Dict, Any, List
from app.core.database import AsyncSession

class LocationQuestionnaireService:
    """Service pour le questionnaire de localisation guidé"""
    
    QUESTIONS = [
        {
            "id": "commune",
            "question": "Quelle est la commune du projet ?",
            "type": "text",
            "required": True,
            "hint": "Ex: Paris, Lyon, Marseille..."
        },
        {
            "id": "adresse",
            "question": "Adresse précise du bien ?",
            "type": "text",
            "required": True,
            "hint": "Ex: 45 Avenue Foch"
        },
        {
            "id": "parcelle_cadastrale",
            "question": "Référence cadastrale ?",
            "type": "text",
            "required": False,
            "hint": "Ex: AB 123"
        },
        {
            "id": "zone_plu",
            "question": "Zone PLU (si connue) ?",
            "type": "select",
            "options": ["UA", "UB", "UC", "UD", "AU", "A", "N", "Inconnue"],
            "required": False
        },
        {
            "id": "surface_terrain",
            "question": "Surface du terrain (m²) ?",
            "type": "number",
            "required": True
        },
        {
            "id": "surface_construite",
            "question": "Surface construite existante (m²) ?",
            "type": "number",
            "required": False
        },
        {
            "id": "hauteur_batiment",
            "question": "Hauteur du bâtiment (m) ?",
            "type": "number",
            "required": False
        },
        {
            "id": "nombre_niveaux",
            "question": "Nombre de niveaux ?",
            "type": "number",
            "required": False
        },
        {
            "id": "monuments_historiques",
            "question": "Périmètre de protection des Monuments Historiques ?",
            "type": "boolean",
            "required": True
        },
        {
            "id": "abf_avis",
            "question": "Soumis à l'avis de l'Architecte des Bâtiments de France (ABF) ?",
            "type": "boolean",
            "required": True
        },
        {
            "id": "nature_travaux",
            "question": "Nature des travaux envisagés ?",
            "type": "multiselect",
            "options": [
                "Extension",
                "Surélévation",
                "Changement de destination",
                "Rénovation intérieure",
                "Rénovation façade",
                "Division en lots",
                "Création de parking"
            ],
            "required": True
        },
        {
            "id": "destination_finale",
            "question": "Destination finale du bien ?",
            "type": "select",
            "options": [
                "Habitation",
                "Bureaux",
                "Commerce",
                "Hôtel",
                "Résidence services",
                "Mixte"
            ],
            "required": True
        }
    ]
    
    def get_questions(self) -> List[Dict[str, Any]]:
        """Retourne la liste complète des questions"""
        return self.QUESTIONS
    
    def validate_answers(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valide les réponses du questionnaire
        
        Returns:
            {
                "valid": bool,
                "errors": list,
                "warnings": list
            }
        """
        errors = []
        warnings = []
        
        # Vérifier les champs requis
        for question in self.QUESTIONS:
            if question["required"] and question["id"] not in answers:
                errors.append(f"Le champ '{question['question']}' est requis")
        
        # Vérifications métier
        if "surface_terrain" in answers and "surface_construite" in answers:
            if answers["surface_construite"] > answers["surface_terrain"] * 2:
                warnings.append("La surface construite semble très élevée par rapport au terrain (COS > 2)")
        
        if answers.get("monuments_historiques") and not answers.get("abf_avis"):
            warnings.append("Attention: périmètre Monument Historique détecté, l'ABF sera probablement sollicité")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def extract_plu_filters(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrait les filtres PLU pertinents à partir des réponses
        
        Returns:
            Critères de recherche PLU optimisés
        """
        filters = {
            "commune": answers.get("commune"),
            "zone": answers.get("zone_plu"),
            "keywords": []
        }
        
        # Mots-clés basés sur la destination
        destination = answers.get("destination_finale")
        if destination == "Commerce":
            filters["keywords"].extend(["commerce", "ERP", "établissement recevant du public"])
        elif destination == "Bureaux":
            filters["keywords"].extend(["bureaux", "tertiaire", "décret tertiaire"])
        elif destination == "Hôtel":
            filters["keywords"].extend(["hôtel", "ERP", "sécurité incendie", "accessibilité PMR"])
        
        # Mots-clés basés sur les travaux
        travaux = answers.get("nature_travaux", [])
        if "Extension" in travaux or "Surélévation" in travaux:
            filters["keywords"].extend(["emprise au sol", "CES", "COS", "gabarit", "hauteur"])
        if "Changement de destination" in travaux:
            filters["keywords"].extend(["changement de destination", "autorisation d'urbanisme"])
        if "Division en lots" in travaux:
            filters["keywords"].extend(["division", "lotissement", "surface minimale"])
        
        # ABF et MH
        if answers.get("monuments_historiques") or answers.get("abf_avis"):
            filters["keywords"].extend(["ABF", "architecte des bâtiments de france", "monuments historiques", "ZPPAUP", "AVAP"])
        
        return filters
