"""
Service de gestion de la timeline des projets
Calcule les phases, la trésorerie et les flux de trésorerie
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__name__)


class TimelineService:
    """Service de calcul et gestion des timelines projet"""
    
    def calculate_project_duration(
        self,
        study_months: int,
        permit_months: int,
        construction_months: int,
        commercialization_months: int,
        execution_mode: str = "sequential"
    ) -> Dict[str, Any]:
        """
        Calcule la durée totale du projet selon le mode d'exécution
        
        Args:
            study_months: Durée phase études
            permit_months: Durée phase permis
            construction_months: Durée phase travaux
            commercialization_months: Durée phase commercialisation
            execution_mode: "sequential" (séquentiel) ou "parallel" (parallèle)
        
        Returns:
            Durée totale et dates calculées
        """
        if execution_mode == "sequential":
            # Tout s'enchaîne
            total_months = (
                study_months + 
                permit_months + 
                construction_months + 
                commercialization_months
            )
        else:
            # Certaines phases peuvent se chevaucher
            # Ex: Commercialisation commence pendant travaux
            overlap_months = min(commercialization_months, construction_months // 2)
            total_months = (
                study_months + 
                permit_months + 
                construction_months + 
                commercialization_months - 
                overlap_months
            )
        
        return {
            "total_months": total_months,
            "total_years": round(total_months / 12, 1),
            "execution_mode": execution_mode
        }
    
    def generate_phase_dates(
        self,
        start_date: datetime,
        study_months: int,
        permit_months: int,
        construction_months: int,
        commercialization_months: int,
        execution_mode: str = "sequential"
    ) -> Dict[str, Dict[str, datetime]]:
        """
        Génère toutes les dates de phases à partir d'une date de début
        
        Returns:
            Dict avec start/end pour chaque phase
        """
        current_date = start_date
        
        phases = {}
        
        # Phase Études
        phases["studies"] = {
            "start": current_date,
            "end": current_date + relativedelta(months=study_months)
        }
        current_date = phases["studies"]["end"]
        
        # Phase Permis
        phases["permit"] = {
            "start": current_date,
            "end": current_date + relativedelta(months=permit_months)
        }
        current_date = phases["permit"]["end"]
        
        # Phase Travaux
        phases["construction"] = {
            "start": current_date,
            "end": current_date + relativedelta(months=construction_months)
        }
        
        # Phase Commercialisation
        if execution_mode == "parallel":
            # Commence à mi-travaux
            comm_start = phases["construction"]["start"] + relativedelta(
                months=construction_months // 2
            )
        else:
            comm_start = phases["construction"]["end"]
        
        phases["commercialization"] = {
            "start": comm_start,
            "end": comm_start + relativedelta(months=commercialization_months)
        }
        
        return phases
    
    def calculate_capex_curve(
        self,
        total_capex: float,
        construction_months: int,
        curve_type: str = "s_curve"
    ) -> List[Dict[str, Any]]:
        """
        Calcule la courbe de décaissement CAPEX mensuelle
        
        Args:
            total_capex: Budget total travaux
            construction_months: Durée travaux en mois
            curve_type: Type de courbe (linear, s_curve, front_loaded, back_loaded)
        
        Returns:
            Liste de décaissements mensuels
        """
        curve = []
        
        if curve_type == "linear":
            # Linéaire : même montant chaque mois
            monthly_capex = total_capex / construction_months
            for month in range(construction_months):
                curve.append({
                    "month": month + 1,
                    "amount": monthly_capex,
                    "cumulative": monthly_capex * (month + 1),
                    "pct_complete": ((month + 1) / construction_months) * 100
                })
        
        elif curve_type == "s_curve":
            # Courbe en S : lent au début, accélère, ralentit à la fin
            # Distribution typique : 10-15-20-25-20-10 pour 6 mois
            import numpy as np
            
            # Fonction sigmoïde pour courbe en S
            x = np.linspace(-3, 3, construction_months)
            sigmoid = 1 / (1 + np.exp(-x))
            
            # Normaliser pour que la somme = total_capex
            weights = np.diff(sigmoid, prepend=0)
            weights = weights / weights.sum()
            
            cumulative = 0
            for month, weight in enumerate(weights):
                amount = total_capex * weight
                cumulative += amount
                curve.append({
                    "month": month + 1,
                    "amount": round(amount, 2),
                    "cumulative": round(cumulative, 2),
                    "pct_complete": round((cumulative / total_capex) * 100, 1)
                })
        
        elif curve_type == "front_loaded":
            # Chargé au début : 40% premier tiers, 35% second, 25% dernier
            third = construction_months // 3
            
            for month in range(construction_months):
                if month < third:
                    pct = 0.40 / third
                elif month < 2 * third:
                    pct = 0.35 / third
                else:
                    pct = 0.25 / (construction_months - 2 * third)
                
                amount = total_capex * pct
                cumulative = sum(c["amount"] for c in curve) + amount
                
                curve.append({
                    "month": month + 1,
                    "amount": round(amount, 2),
                    "cumulative": round(cumulative, 2),
                    "pct_complete": round((cumulative / total_capex) * 100, 1)
                })
        
        elif curve_type == "back_loaded":
            # Chargé en fin : 25% premier tiers, 35% second, 40% dernier
            third = construction_months // 3
            
            for month in range(construction_months):
                if month < third:
                    pct = 0.25 / third
                elif month < 2 * third:
                    pct = 0.35 / third
                else:
                    pct = 0.40 / (construction_months - 2 * third)
                
                amount = total_capex * pct
                cumulative = sum(c["amount"] for c in curve) + amount
                
                curve.append({
                    "month": month + 1,
                    "amount": round(amount, 2),
                    "cumulative": round(cumulative, 2),
                    "pct_complete": round((cumulative / total_capex) * 100, 1)
                })
        
        return curve
    
    def generate_cashflow_schedule(
        self,
        timeline_data: Dict[str, Any],
        financial_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Génère le planning de trésorerie mensuel complet
        
        Args:
            timeline_data: Données de timeline (phases, dates)
            financial_data: Données financières (budgets, loyers)
        
        Returns:
            Planning mensuel avec sorties et entrées
        """
        cashflow = []
        
        # TODO: Implémenter la logique complète de génération de cash-flow
        # en fonction des phases, CAPEX curve, loyers, VEFA, etc.
        
        return cashflow


# Instance globale
timeline_service = TimelineService()
