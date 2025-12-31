"""
Service de gestion des coûts CAPEX (travaux)
Fournit des estimations de coûts pour les différents postes de travaux
"""
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime


class CAPEXCategory:
    """Catégories de coûts CAPEX"""
    STRUCTURE = "structure"
    FACADE = "facade"
    TOITURE = "toiture"
    MENUISERIES = "menuiseries"
    PLOMBERIE = "plomberie"
    ELECTRICITE = "electricite"
    CHAUFFAGE = "chauffage"
    ISOLATION = "isolation"
    CLOISONS = "cloisons"
    REVETEMENTS = "revetements"
    CUISINE = "cuisine"
    SALLE_BAIN = "salle_bain"
    ASCENSEUR = "ascenseur"
    SECURITE_INCENDIE = "securite_incendie"
    PMR = "pmr"
    VRD = "vrd"  # Voirie et Réseaux Divers
    ETUDES = "etudes"
    HONORAIRES = "honoraires"
    ASSURANCES = "assurances"


class CityTier:
    """Niveau de ville pour adaptation des coûts"""
    TIER_1 = 1  # Paris, Lyon, Marseille, Bordeaux
    TIER_2 = 2  # Grandes villes régionales
    TIER_3 = 3  # Province


# Base de données de coûts par défaut (€/unité)
DEFAULT_CAPEX_COSTS = {
    # STRUCTURE
    "structure_reprise_fondations": {"unit": "m3", "min": 800, "avg": 1200, "max": 2000, "tier": 1},
    "structure_reprise_planchers": {"unit": "m2", "min": 150, "avg": 250, "max": 400, "tier": 1},
    "structure_renfort_poutres": {"unit": "ml", "min": 200, "avg": 350, "max": 600, "tier": 1},
    
    # FACADE
    "facade_ravalement_simple": {"unit": "m2", "min": 40, "avg": 60, "max": 90, "tier": 1},
    "facade_ravalement_pierre": {"unit": "m2", "min": 80, "avg": 120, "max": 180, "tier": 1},
    "facade_isolation_exterieure": {"unit": "m2", "min": 100, "avg": 150, "max": 220, "tier": 1},
    
    # TOITURE
    "toiture_refection_complete": {"unit": "m2", "min": 100, "avg": 150, "max": 250, "tier": 1},
    "toiture_isolation": {"unit": "m2", "min": 40, "avg": 60, "max": 90, "tier": 1},
    "toiture_charpente": {"unit": "m2", "min": 150, "avg": 250, "max": 400, "tier": 1},
    
    # MENUISERIES
    "menuiseries_fenetres_pvc": {"unit": "unite", "min": 300, "avg": 500, "max": 800, "tier": 1},
    "menuiseries_fenetres_alu": {"unit": "unite", "min": 500, "avg": 800, "max": 1200, "tier": 1},
    "menuiseries_portes_entree": {"unit": "unite", "min": 800, "avg": 1500, "max": 2500, "tier": 1},
    
    # PLOMBERIE
    "plomberie_renovation_complete": {"unit": "m2", "min": 80, "avg": 120, "max": 180, "tier": 1},
    "plomberie_salle_bain": {"unit": "unite", "min": 3000, "avg": 5000, "max": 8000, "tier": 1},
    
    # ELECTRICITE
    "electricite_renovation_complete": {"unit": "m2", "min": 80, "avg": 110, "max": 150, "tier": 1},
    "electricite_mise_aux_normes": {"unit": "m2", "min": 50, "avg": 75, "max": 100, "tier": 1},
    
    # CHAUFFAGE
    "chauffage_chaudiere_gaz": {"unit": "unite", "min": 3000, "avg": 5000, "max": 8000, "tier": 1},
    "chauffage_pompe_chaleur": {"unit": "unite", "min": 8000, "avg": 12000, "max": 18000, "tier": 1},
    "chauffage_radiateurs": {"unit": "unite", "min": 400, "avg": 600, "max": 900, "tier": 1},
    
    # ISOLATION
    "isolation_murs_interieurs": {"unit": "m2", "min": 30, "avg": 45, "max": 70, "tier": 1},
    "isolation_combles": {"unit": "m2", "min": 25, "avg": 40, "max": 60, "tier": 1},
    
    # CLOISONS
    "cloisons_placo": {"unit": "m2", "min": 35, "avg": 50, "max": 75, "tier": 1},
    "cloisons_beton": {"unit": "m2", "min": 80, "avg": 120, "max": 180, "tier": 1},
    
    # REVETEMENTS
    "revetements_peinture": {"unit": "m2", "min": 15, "avg": 25, "max": 40, "tier": 1},
    "revetements_carrelage": {"unit": "m2", "min": 40, "avg": 70, "max": 120, "tier": 1},
    "revetements_parquet": {"unit": "m2", "min": 50, "avg": 80, "max": 140, "tier": 1},
    
    # CUISINE
    "cuisine_equipee_standard": {"unit": "ml", "min": 500, "avg": 800, "max": 1500, "tier": 1},
    "cuisine_equipee_haut_gamme": {"unit": "ml", "min": 1500, "avg": 2500, "max": 4000, "tier": 1},
    
    # SALLE DE BAIN
    "salle_bain_complete_standard": {"unit": "unite", "min": 5000, "avg": 8000, "max": 12000, "tier": 1},
    "salle_bain_complete_haut_gamme": {"unit": "unite", "min": 12000, "avg": 18000, "max": 30000, "tier": 1},
    
    # ASCENSEUR
    "ascenseur_installation": {"unit": "unite", "min": 40000, "avg": 60000, "max": 90000, "tier": 1},
    "ascenseur_modernisation": {"unit": "unite", "min": 20000, "avg": 30000, "max": 45000, "tier": 1},
    
    # SECURITE INCENDIE
    "securite_desenfumage": {"unit": "unite", "min": 2000, "avg": 4000, "max": 8000, "tier": 1},
    "securite_detecteurs": {"unit": "unite", "min": 150, "avg": 250, "max": 400, "tier": 1},
    "securite_extinction": {"unit": "m2", "min": 30, "avg": 50, "max": 80, "tier": 1},
    "securite_porte_coupe_feu": {"unit": "unite", "min": 800, "avg": 1200, "max": 2000, "tier": 1},
    
    # PMR (Accessibilité)
    "pmr_rampe_acces": {"unit": "unite", "min": 2000, "avg": 4000, "max": 8000, "tier": 1},
    "pmr_ascenseur_specifique": {"unit": "unite", "min": 50000, "avg": 70000, "max": 100000, "tier": 1},
    "pmr_sanitaires_adaptes": {"unit": "unite", "min": 3000, "avg": 5000, "max": 8000, "tier": 1},
    "pmr_portes_elargies": {"unit": "unite", "min": 500, "avg": 800, "max": 1200, "tier": 1},
    
    # VRD
    "vrd_raccordement_eau": {"unit": "ml", "min": 100, "avg": 150, "max": 250, "tier": 1},
    "vrd_assainissement": {"unit": "ml", "min": 120, "avg": 180, "max": 300, "tier": 1},
    "vrd_voirie": {"unit": "m2", "min": 50, "avg": 80, "max": 120, "tier": 1},
    
    # ETUDES ET HONORAIRES
    "etudes_structure": {"unit": "forfait", "min": 3000, "avg": 5000, "max": 10000, "tier": 1},
    "etudes_thermique": {"unit": "forfait", "min": 1500, "avg": 2500, "max": 4000, "tier": 1},
    "etudes_acoustique": {"unit": "forfait", "min": 2000, "avg": 3000, "max": 5000, "tier": 1},
    "honoraires_architecte": {"unit": "pourcentage", "min": 8, "avg": 12, "max": 15, "tier": 1},
    "honoraires_bureaux_etudes": {"unit": "pourcentage", "min": 2, "avg": 4, "max": 6, "tier": 1},
    
    # ASSURANCES
    "assurances_dommages_ouvrage": {"unit": "pourcentage", "min": 2, "avg": 3, "max": 4, "tier": 1},
}


class CAPEXService:
    """Service de calcul des coûts CAPEX"""
    
    def __init__(self):
        self.costs_db = DEFAULT_CAPEX_COSTS
    
    def get_cost_estimate(
        self,
        item_key: str,
        quantity: float,
        city_tier: int = CityTier.TIER_1
    ) -> Dict:
        """
        Obtenir l'estimation de coût pour un poste
        
        Args:
            item_key: Clé du poste (ex: "facade_ravalement_simple")
            quantity: Quantité (m2, ml, unités, etc.)
            city_tier: Niveau ville (1=Paris, 2=Grandes villes, 3=Province)
        
        Returns:
            Dict avec min/avg/max costs
        """
        if item_key not in self.costs_db:
            return {
                "error": f"Poste '{item_key}' non trouvé",
                "available_items": list(self.costs_db.keys())
            }
        
        cost_data = self.costs_db[item_key]
        
        # Ajustement selon tier de ville
        tier_multiplier = self._get_tier_multiplier(city_tier)
        
        min_total = cost_data["min"] * quantity * tier_multiplier
        avg_total = cost_data["avg"] * quantity * tier_multiplier
        max_total = cost_data["max"] * quantity * tier_multiplier
        
        return {
            "item": item_key,
            "unit": cost_data["unit"],
            "quantity": quantity,
            "city_tier": city_tier,
            "unit_prices": {
                "min": round(cost_data["min"] * tier_multiplier, 2),
                "avg": round(cost_data["avg"] * tier_multiplier, 2),
                "max": round(cost_data["max"] * tier_multiplier, 2)
            },
            "total_costs": {
                "min": round(min_total, 2),
                "avg": round(avg_total, 2),
                "max": round(max_total, 2)
            }
        }
    
    def calculate_project_capex(
        self,
        items: List[Dict],
        city_tier: int = CityTier.TIER_1,
        contingency_rate: float = 0.10
    ) -> Dict:
        """
        Calculer le CAPEX total d'un projet
        
        Args:
            items: Liste de dict {"key": str, "quantity": float}
            city_tier: Niveau ville
            contingency_rate: Taux d'aléas (défaut 10%)
        
        Returns:
            Analyse CAPEX complète avec détails par poste
        """
        estimates = []
        total_min = 0
        total_avg = 0
        total_max = 0
        
        for item in items:
            estimate = self.get_cost_estimate(
                item["key"],
                item["quantity"],
                city_tier
            )
            
            if "error" not in estimate:
                estimates.append(estimate)
                total_min += estimate["total_costs"]["min"]
                total_avg += estimate["total_costs"]["avg"]
                total_max += estimate["total_costs"]["max"]
        
        # Ajouter aléas
        contingency_min = total_min * contingency_rate
        contingency_avg = total_avg * contingency_rate
        contingency_max = total_max * contingency_rate
        
        return {
            "project_capex": {
                "base_costs": {
                    "min": round(total_min, 2),
                    "avg": round(total_avg, 2),
                    "max": round(total_max, 2)
                },
                "contingency": {
                    "rate": contingency_rate,
                    "amount_min": round(contingency_min, 2),
                    "amount_avg": round(contingency_avg, 2),
                    "amount_max": round(contingency_max, 2)
                },
                "total_with_contingency": {
                    "min": round(total_min + contingency_min, 2),
                    "avg": round(total_avg + contingency_avg, 2),
                    "max": round(total_max + contingency_max, 2)
                }
            },
            "items_detail": estimates,
            "summary": {
                "total_items": len(estimates),
                "city_tier": city_tier,
                "contingency_rate": contingency_rate
            }
        }
    
    def get_all_categories(self) -> Dict[str, List[str]]:
        """Obtenir toutes les catégories et postes disponibles"""
        categories = {}
        
        for key in self.costs_db.keys():
            category = key.split("_")[0]
            if category not in categories:
                categories[category] = []
            categories[category].append(key)
        
        return categories
    
    def _get_tier_multiplier(self, tier: int) -> float:
        """Obtenir le multiplicateur de coût selon le tier"""
        multipliers = {
            CityTier.TIER_1: 1.0,   # Paris, Lyon, etc. (référence)
            CityTier.TIER_2: 0.85,  # -15% grandes villes
            CityTier.TIER_3: 0.70   # -30% province
        }
        return multipliers.get(tier, 1.0)
    
    def estimate_renovation_budget(
        self,
        surface: float,
        renovation_level: str,
        city_tier: int = CityTier.TIER_1
    ) -> Dict:
        """
        Estimation rapide budget rénovation au m2
        
        Args:
            surface: Surface en m2
            renovation_level: "light", "medium", "heavy", "complete"
            city_tier: Niveau ville
        
        Returns:
            Estimation budget avec détails
        """
        # Coûts au m2 selon niveau de rénovation
        costs_per_m2 = {
            "light": {"min": 300, "avg": 450, "max": 600},      # Rafraîchissement
            "medium": {"min": 600, "avg": 900, "max": 1200},    # Rénovation partielle
            "heavy": {"min": 1200, "avg": 1600, "max": 2000},   # Rénovation lourde
            "complete": {"min": 2000, "avg": 2500, "max": 3500} # Rénovation complète
        }
        
        if renovation_level not in costs_per_m2:
            return {"error": f"Niveau '{renovation_level}' invalide. Valeurs: light, medium, heavy, complete"}
        
        tier_multiplier = self._get_tier_multiplier(city_tier)
        level_costs = costs_per_m2[renovation_level]
        
        return {
            "renovation_level": renovation_level,
            "surface_m2": surface,
            "city_tier": city_tier,
            "cost_per_m2": {
                "min": round(level_costs["min"] * tier_multiplier, 2),
                "avg": round(level_costs["avg"] * tier_multiplier, 2),
                "max": round(level_costs["max"] * tier_multiplier, 2)
            },
            "total_budget": {
                "min": round(level_costs["min"] * tier_multiplier * surface, 2),
                "avg": round(level_costs["avg"] * tier_multiplier * surface, 2),
                "max": round(level_costs["max"] * tier_multiplier * surface, 2)
            },
            "description": self._get_renovation_description(renovation_level)
        }
    
    def _get_renovation_description(self, level: str) -> str:
        """Description du niveau de rénovation"""
        descriptions = {
            "light": "Rafraîchissement: peinture, revêtements, petites réparations",
            "medium": "Rénovation partielle: cuisine, SdB, électricité, plomberie",
            "heavy": "Rénovation lourde: redistribution, structure, façade, toiture",
            "complete": "Rénovation complète: à neuf avec mise aux normes totale"
        }
        return descriptions.get(level, "")


# Instance globale
capex_service = CAPEXService()
