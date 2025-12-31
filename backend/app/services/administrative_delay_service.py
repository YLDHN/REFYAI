"""
Service de gestion des délais administratifs
Fournit des estimations de délais pour les différentes procédures
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class ProcedureType:
    """Types de procédures administratives"""
    PC = "permis_construire"           # Permis de Construire
    DP = "declaration_prealable"       # Déclaration Préalable
    AT = "autorisation_travaux"        # Autorisation de Travaux
    PA = "permis_amenager"             # Permis d'Aménager
    PD = "permis_demolir"              # Permis de Démolir
    ABF = "avis_abf"                   # Avis Architecte des Bâtiments de France
    DAACT = "declaration_achevement"   # Déclaration d'Achèvement
    CU = "certificat_urbanisme"        # Certificat d'Urbanisme


# Base de données des délais par défaut (en jours)
DEFAULT_ADMINISTRATIVE_DELAYS = {
    # PERMIS DE CONSTRUIRE
    "Paris_permis_construire": {
        "procedure": ProcedureType.PC,
        "avg_delay": 90,
        "min_delay": 60,
        "max_delay": 180,
        "complexity_factor": 1.5,
        "description": "Délai moyen PC à Paris (avec ABF fréquent)"
    },
    "Lyon_permis_construire": {
        "procedure": ProcedureType.PC,
        "avg_delay": 75,
        "min_delay": 45,
        "max_delay": 150,
        "complexity_factor": 1.3,
        "description": "Délai moyen PC à Lyon"
    },
    "Marseille_permis_construire": {
        "procedure": ProcedureType.PC,
        "avg_delay": 70,
        "min_delay": 45,
        "max_delay": 120,
        "complexity_factor": 1.2,
        "description": "Délai moyen PC à Marseille"
    },
    "Bordeaux_permis_construire": {
        "procedure": ProcedureType.PC,
        "avg_delay": 65,
        "min_delay": 40,
        "max_delay": 110,
        "complexity_factor": 1.2,
        "description": "Délai moyen PC à Bordeaux"
    },
    "default_permis_construire": {
        "procedure": ProcedureType.PC,
        "avg_delay": 60,
        "min_delay": 30,
        "max_delay": 90,
        "complexity_factor": 1.0,
        "description": "Délai moyen PC (ville standard)"
    },
    
    # DECLARATION PREALABLE
    "Paris_declaration_prealable": {
        "procedure": ProcedureType.DP,
        "avg_delay": 45,
        "min_delay": 30,
        "max_delay": 90,
        "complexity_factor": 1.3,
        "description": "Délai moyen DP à Paris"
    },
    "default_declaration_prealable": {
        "procedure": ProcedureType.DP,
        "avg_delay": 30,
        "min_delay": 15,
        "max_delay": 60,
        "complexity_factor": 1.0,
        "description": "Délai moyen DP (ville standard)"
    },
    
    # AUTORISATION DE TRAVAUX
    "default_autorisation_travaux": {
        "procedure": ProcedureType.AT,
        "avg_delay": 30,
        "min_delay": 15,
        "max_delay": 60,
        "complexity_factor": 1.0,
        "description": "Délai moyen AT"
    },
    
    # AVIS ABF
    "default_avis_abf": {
        "procedure": ProcedureType.ABF,
        "avg_delay": 45,
        "min_delay": 30,
        "max_delay": 90,
        "complexity_factor": 1.5,
        "description": "Délai avis ABF (ajoute au délai PC/DP)"
    },
    
    # PERMIS DE DEMOLIR
    "default_permis_demolir": {
        "procedure": ProcedureType.PD,
        "avg_delay": 60,
        "min_delay": 30,
        "max_delay": 90,
        "complexity_factor": 1.0,
        "description": "Délai moyen permis de démolir"
    },
    
    # CERTIFICAT D'URBANISME
    "default_certificat_urbanisme": {
        "procedure": ProcedureType.CU,
        "avg_delay": 30,
        "min_delay": 15,
        "max_delay": 45,
        "complexity_factor": 1.0,
        "description": "Délai moyen CU"
    },
    
    # DAACT
    "default_declaration_achevement": {
        "procedure": ProcedureType.DAACT,
        "avg_delay": 90,
        "min_delay": 60,
        "max_delay": 120,
        "complexity_factor": 1.0,
        "description": "Délai moyen visite DAACT"
    }
}


class ComplexityLevel:
    """Niveaux de complexité de projet"""
    SIMPLE = 1.0        # Projet standard, pas de contraintes
    MODERATE = 1.3      # Quelques contraintes (ABF, site classé, etc.)
    COMPLEX = 1.6       # Nombreuses contraintes
    VERY_COMPLEX = 2.0  # Projet exceptionnel (monuments historiques, etc.)


class AdministrativeDelayService:
    """Service de calcul des délais administratifs"""
    
    def __init__(self):
        self.delays_db = DEFAULT_ADMINISTRATIVE_DELAYS
    
    def get_procedure_delay(
        self,
        city: str,
        procedure_type: str,
        complexity: float = ComplexityLevel.SIMPLE,
        has_abf: bool = False
    ) -> Dict:
        """
        Obtenir le délai pour une procédure
        
        Args:
            city: Nom de la ville
            procedure_type: Type de procédure (PC, DP, etc.)
            complexity: Facteur de complexité (1.0 à 2.0)
            has_abf: Si ABF requis (ajoute délai supplémentaire)
        
        Returns:
            Dict avec min/avg/max delays en jours
        """
        # Recherche délai spécifique ville ou défaut
        key = f"{city}_{procedure_type}"
        default_key = f"default_{procedure_type}"
        
        if key in self.delays_db:
            delay_data = self.delays_db[key]
        elif default_key in self.delays_db:
            delay_data = self.delays_db[default_key]
        else:
            return {
                "error": f"Procédure '{procedure_type}' non trouvée",
                "available_procedures": self._get_available_procedures()
            }
        
        # Appliquer facteurs de complexité
        base_complexity = delay_data["complexity_factor"]
        total_complexity = base_complexity * complexity
        
        min_delay = int(delay_data["min_delay"] * total_complexity)
        avg_delay = int(delay_data["avg_delay"] * total_complexity)
        max_delay = int(delay_data["max_delay"] * total_complexity)
        
        # Ajouter délai ABF si nécessaire
        abf_delay = 0
        if has_abf and procedure_type in [ProcedureType.PC, ProcedureType.DP]:
            abf_data = self.delays_db["default_avis_abf"]
            abf_delay = abf_data["avg_delay"]
            min_delay += abf_data["min_delay"]
            avg_delay += abf_data["avg_delay"]
            max_delay += abf_data["max_delay"]
        
        return {
            "city": city,
            "procedure": procedure_type,
            "complexity_factor": round(total_complexity, 2),
            "has_abf": has_abf,
            "delays_days": {
                "min": min_delay,
                "avg": avg_delay,
                "max": max_delay
            },
            "delays_months": {
                "min": round(min_delay / 30, 1),
                "avg": round(avg_delay / 30, 1),
                "max": round(max_delay / 30, 1)
            },
            "abf_additional_days": abf_delay if has_abf else 0,
            "description": delay_data["description"]
        }
    
    def calculate_project_timeline(
        self,
        city: str,
        procedures: List[Dict],
        parallel_execution: bool = False
    ) -> Dict:
        """
        Calculer le planning complet d'un projet
        
        Args:
            city: Ville du projet
            procedures: Liste de {"type": str, "complexity": float, "has_abf": bool}
            parallel_execution: Si certaines procédures peuvent être parallèles
        
        Returns:
            Timeline complète avec dates estimées
        """
        timeline = []
        total_min = 0
        total_avg = 0
        total_max = 0
        
        for proc in procedures:
            delay = self.get_procedure_delay(
                city,
                proc.get("type"),
                proc.get("complexity", ComplexityLevel.SIMPLE),
                proc.get("has_abf", False)
            )
            
            if "error" not in delay:
                timeline.append({
                    "procedure": delay["procedure"],
                    "delays": delay["delays_days"],
                    "description": delay["description"]
                })
                
                if not parallel_execution:
                    total_min += delay["delays_days"]["min"]
                    total_avg += delay["delays_days"]["avg"]
                    total_max += delay["delays_days"]["max"]
                else:
                    # En parallèle, prendre le max
                    total_min = max(total_min, delay["delays_days"]["min"])
                    total_avg = max(total_avg, delay["delays_days"]["avg"])
                    total_max = max(total_max, delay["delays_days"]["max"])
        
        today = datetime.now()
        
        return {
            "project_timeline": {
                "city": city,
                "execution_mode": "parallel" if parallel_execution else "sequential",
                "total_delays_days": {
                    "min": total_min,
                    "avg": total_avg,
                    "max": total_max
                },
                "total_delays_months": {
                    "min": round(total_min / 30, 1),
                    "avg": round(total_avg / 30, 1),
                    "max": round(total_max / 30, 1)
                },
                "estimated_completion": {
                    "optimistic": (today + timedelta(days=total_min)).strftime("%Y-%m-%d"),
                    "realistic": (today + timedelta(days=total_avg)).strftime("%Y-%m-%d"),
                    "pessimistic": (today + timedelta(days=total_max)).strftime("%Y-%m-%d")
                }
            },
            "procedures_detail": timeline,
            "summary": {
                "total_procedures": len(timeline),
                "start_date": today.strftime("%Y-%m-%d")
            }
        }
    
    def estimate_full_project_duration(
        self,
        city: str,
        project_data: Dict
    ) -> Dict:
        """
        Estimation complète durée projet (études + admin + travaux)
        
        Args:
            city: Ville du projet
            project_data: {
                "has_pc": bool,
                "has_dp": bool,
                "has_abf": bool,
                "complexity": float,
                "construction_months": int
            }
        
        Returns:
            Durée totale estimée avec phases
        """
        procedures = []
        
        # Phase 1: Etudes préalables (1-3 mois)
        studies_min = 30
        studies_avg = 60
        studies_max = 90
        
        # Phase 2: Procédures administratives
        if project_data.get("has_pc"):
            procedures.append({
                "type": ProcedureType.PC,
                "complexity": project_data.get("complexity", ComplexityLevel.SIMPLE),
                "has_abf": project_data.get("has_abf", False)
            })
        elif project_data.get("has_dp"):
            procedures.append({
                "type": ProcedureType.DP,
                "complexity": project_data.get("complexity", ComplexityLevel.SIMPLE),
                "has_abf": project_data.get("has_abf", False)
            })
        
        admin_timeline = self.calculate_project_timeline(city, procedures, False)
        admin_delays = admin_timeline["project_timeline"]["total_delays_days"]
        
        # Phase 3: Travaux
        construction_days = project_data.get("construction_months", 6) * 30
        
        # Phase 4: DAACT et réception (2-4 mois)
        daact_data = self.delays_db["default_declaration_achevement"]
        daact_min = daact_data["min_delay"]
        daact_avg = daact_data["avg_delay"]
        daact_max = daact_data["max_delay"]
        
        # Total
        total_min = studies_min + admin_delays["min"] + construction_days + daact_min
        total_avg = studies_avg + admin_delays["avg"] + construction_days + daact_avg
        total_max = studies_max + admin_delays["max"] + construction_days + daact_max
        
        today = datetime.now()
        
        return {
            "full_project_duration": {
                "phases": {
                    "studies": {
                        "min_days": studies_min,
                        "avg_days": studies_avg,
                        "max_days": studies_max,
                        "description": "Etudes préalables et conception"
                    },
                    "administrative": {
                        "min_days": admin_delays["min"],
                        "avg_days": admin_delays["avg"],
                        "max_days": admin_delays["max"],
                        "description": "Procédures administratives"
                    },
                    "construction": {
                        "days": construction_days,
                        "description": "Travaux de construction"
                    },
                    "completion": {
                        "min_days": daact_min,
                        "avg_days": daact_avg,
                        "max_days": daact_max,
                        "description": "DAACT et réception"
                    }
                },
                "total_duration_days": {
                    "min": total_min,
                    "avg": total_avg,
                    "max": total_max
                },
                "total_duration_months": {
                    "min": round(total_min / 30, 1),
                    "avg": round(total_avg / 30, 1),
                    "max": round(total_max / 30, 1)
                },
                "completion_dates": {
                    "optimistic": (today + timedelta(days=total_min)).strftime("%Y-%m-%d"),
                    "realistic": (today + timedelta(days=total_avg)).strftime("%Y-%m-%d"),
                    "pessimistic": (today + timedelta(days=total_max)).strftime("%Y-%m-%d")
                }
            },
            "city": city,
            "complexity": project_data.get("complexity", ComplexityLevel.SIMPLE)
        }
    
    def _get_available_procedures(self) -> List[str]:
        """Liste des procédures disponibles"""
        procedures = set()
        for key in self.delays_db.keys():
            if key.startswith("default_"):
                proc = key.replace("default_", "")
                procedures.add(proc)
        return sorted(list(procedures))
    
    def get_cities_with_data(self) -> List[str]:
        """Liste des villes avec données spécifiques"""
        cities = set()
        for key in self.delays_db.keys():
            if not key.startswith("default_"):
                city = key.split("_")[0]
                cities.add(city)
        return sorted(list(cities))


# Instance globale
administrative_delay_service = AdministrativeDelayService()
