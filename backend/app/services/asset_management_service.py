"""
Service de gestion d'Asset Management
Gère les franchises de loyer (Rent Free), Tenant Improvements et indexation
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__name__)


class IndexationType:
    """Types d'indexation des loyers"""
    ICC = "ICC"  # Indice du Coût de la Construction
    ILAT = "ILAT"  # Indice des Loyers des Activités Tertiaires
    ILC = "ILC"  # Indice des Loyers Commerciaux
    FIXED = "FIXED"  # Fixe (%)
    
    # Valeurs historiques moyennes
    HISTORICAL_RATES = {
        "ICC": 0.025,  # 2.5% annuel moyen
        "ILAT": 0.020,  # 2.0% annuel moyen
        "ILC": 0.022,  # 2.2% annuel moyen
    }


class AssetManagementService:
    """Service de gestion Asset Management avancée"""
    
    def calculate_rent_schedule_with_rent_free(
        self,
        annual_rent: float,
        lease_start_date: datetime,
        lease_duration_years: int,
        rent_free_months: int = 0,
        tenant_improvements: float = 0,
        indexation_type: str = "ILAT",
        indexation_rate: Optional[float] = None,
        indexation_start_year: int = 2
    ) -> Dict[str, Any]:
        """
        Calcule le planning de loyers avec :
        - Franchise de loyer (Rent Free)
        - Tenant Improvements (contribution propriétaire)
        - Indexation annuelle
        
        Args:
            annual_rent: Loyer annuel de base
            lease_start_date: Date début bail
            lease_duration_years: Durée bail en années
            rent_free_months: Nombre de mois de franchise
            tenant_improvements: Montant des travaux preneur payés par le bailleur
            indexation_type: Type d'indexation (ICC, ILAT, ILC, FIXED)
            indexation_rate: Taux d'indexation (si None, utilise taux historique)
            indexation_start_year: Année de début indexation (généralement année 2)
        
        Returns:
            Planning de trésorerie détaillé
        """
        
        # Validation
        if annual_rent <= 0:
            raise ValueError("Le loyer annuel doit être positif")
        
        if rent_free_months < 0:
            raise ValueError("Les mois de franchise ne peuvent pas être négatifs")
        
        if rent_free_months >= lease_duration_years * 12:
            raise ValueError("La franchise ne peut pas dépasser la durée du bail")
        
        # Taux d'indexation
        if indexation_rate is None:
            if indexation_type == "FIXED":
                indexation_rate = 0.02  # 2% par défaut
            else:
                indexation_rate = IndexationType.HISTORICAL_RATES.get(
                    indexation_type, 0.02
                )
        
        # Loyer mensuel de base
        monthly_rent = annual_rent / 12
        
        # Planning mensuel
        schedule = []
        current_date = lease_start_date
        current_annual_rent = annual_rent
        
        for month in range(1, (lease_duration_years * 12) + 1):
            year = (month - 1) // 12 + 1
            month_in_year = ((month - 1) % 12) + 1
            
            # Application de l'indexation (généralement à chaque anniversaire)
            if month > 1 and month_in_year == 1 and year >= indexation_start_year:
                current_annual_rent *= (1 + indexation_rate)
                current_monthly_rent = current_annual_rent / 12
            else:
                current_monthly_rent = current_annual_rent / 12
            
            # Franchise de loyer
            is_rent_free = month <= rent_free_months
            
            rent_payment = 0 if is_rent_free else current_monthly_rent
            
            schedule.append({
                "month": month,
                "date": current_date.strftime("%Y-%m-%d"),
                "year": year,
                "month_in_year": month_in_year,
                "rent_payment": round(rent_payment, 2),
                "is_rent_free": is_rent_free,
                "annual_rent": round(current_annual_rent, 2),
                "indexation_applied": month > 1 and month_in_year == 1 and year >= indexation_start_year,
                "cumulative_rent": round(sum(s["rent_payment"] for s in schedule) + rent_payment, 2)
            })
            
            current_date += relativedelta(months=1)
        
        # Calculs de synthèse
        total_rent_received = sum(s["rent_payment"] for s in schedule)
        rent_free_period_cost = monthly_rent * rent_free_months
        total_cost_to_landlord = rent_free_period_cost + tenant_improvements
        
        # Impact sur le rendement
        effective_annual_rent = total_rent_received / lease_duration_years
        yield_impact = (effective_annual_rent / annual_rent) - 1
        
        return {
            "lease_parameters": {
                "annual_rent_initial": annual_rent,
                "monthly_rent_initial": monthly_rent,
                "lease_start_date": lease_start_date.strftime("%Y-%m-%d"),
                "lease_duration_years": lease_duration_years,
                "lease_end_date": (lease_start_date + relativedelta(years=lease_duration_years)).strftime("%Y-%m-%d"),
                "rent_free_months": rent_free_months,
                "tenant_improvements": tenant_improvements,
                "indexation_type": indexation_type,
                "indexation_rate": indexation_rate,
                "indexation_rate_pct": f"{indexation_rate * 100:.2f}%"
            },
            "financial_impact": {
                "total_rent_received": round(total_rent_received, 2),
                "rent_free_cost": round(rent_free_period_cost, 2),
                "tenant_improvements_cost": tenant_improvements,
                "total_cost_to_landlord": round(total_cost_to_landlord, 2),
                "effective_annual_rent": round(effective_annual_rent, 2),
                "yield_impact_pct": f"{yield_impact * 100:.2f}%",
                "break_even_month": self._calculate_break_even(
                    schedule, total_cost_to_landlord
                )
            },
            "schedule": schedule
        }
    
    def _calculate_break_even(
        self,
        schedule: List[Dict],
        initial_cost: float
    ) -> Optional[int]:
        """Calcule le mois où les loyers couvrent les coûts initiaux"""
        cumulative = 0
        for entry in schedule:
            cumulative += entry["rent_payment"]
            if cumulative >= initial_cost:
                return entry["month"]
        return None
    
    def calculate_indexation_projection(
        self,
        initial_rent: float,
        years: int,
        indexation_type: str = "ILAT",
        custom_rate: Optional[float] = None,
        scenarios: List[str] = ["pessimistic", "base", "optimistic"]
    ) -> Dict[str, Any]:
        """
        Projection de l'évolution du loyer selon différents scénarios d'indexation
        
        Args:
            initial_rent: Loyer initial
            years: Nombre d'années de projection
            indexation_type: Type d'indice
            custom_rate: Taux personnalisé (remplace taux historique)
            scenarios: Liste de scénarios à calculer
        
        Returns:
            Projections multi-scénarios
        """
        
        # Taux de base
        if custom_rate is not None:
            base_rate = custom_rate
        else:
            base_rate = IndexationType.HISTORICAL_RATES.get(indexation_type, 0.02)
        
        # Définition des scénarios
        scenario_rates = {
            "pessimistic": base_rate * 0.5,  # 50% du taux historique
            "base": base_rate,
            "optimistic": base_rate * 1.5   # 150% du taux historique
        }
        
        results = {}
        
        for scenario in scenarios:
            rate = scenario_rates.get(scenario, base_rate)
            projection = []
            current_rent = initial_rent
            
            for year in range(1, years + 1):
                if year > 1:
                    current_rent *= (1 + rate)
                
                projection.append({
                    "year": year,
                    "annual_rent": round(current_rent, 2),
                    "indexation_rate": rate,
                    "increase_vs_initial": round(current_rent - initial_rent, 2),
                    "increase_pct": f"{((current_rent / initial_rent) - 1) * 100:.2f}%"
                })
            
            results[scenario] = {
                "indexation_rate": rate,
                "indexation_rate_pct": f"{rate * 100:.2f}%",
                "projection": projection,
                "final_rent": round(current_rent, 2),
                "total_increase": round(current_rent - initial_rent, 2),
                "cumulative_rent": round(sum(p["annual_rent"] for p in projection), 2)
            }
        
        return {
            "initial_rent": initial_rent,
            "projection_years": years,
            "indexation_type": indexation_type,
            "scenarios": results
        }
    
    def calculate_rent_free_value(
        self,
        monthly_rent: float,
        rent_free_months: int,
        discount_rate: float = 0.05
    ) -> Dict[str, Any]:
        """
        Calcule la valeur actualisée d'une franchise de loyer
        
        Utile pour :
        - Négociation des termes du bail
        - Valorisation de l'avantage locataire
        - Décision make/buy pour le bailleur
        
        Args:
            monthly_rent: Loyer mensuel
            rent_free_months: Durée de la franchise
            discount_rate: Taux d'actualisation
        
        Returns:
            Valeur nominale et actualisée
        """
        
        nominal_value = monthly_rent * rent_free_months
        
        # Valeur actualisée (les mois de franchise sont au début)
        present_value = 0
        monthly_discount_rate = discount_rate / 12
        
        for month in range(1, rent_free_months + 1):
            present_value += monthly_rent / ((1 + monthly_discount_rate) ** month)
        
        return {
            "monthly_rent": monthly_rent,
            "rent_free_months": rent_free_months,
            "nominal_value": round(nominal_value, 2),
            "present_value": round(present_value, 2),
            "discount_rate": discount_rate,
            "discount_rate_pct": f"{discount_rate * 100:.2f}%",
            "value_difference": round(nominal_value - present_value, 2),
            "interpretation": f"La franchise de {rent_free_months} mois représente {nominal_value:,.0f}€ nominaux, "
                             f"soit {present_value:,.0f}€ en valeur actuelle."
        }
    
    def optimize_tenant_improvements(
        self,
        monthly_rent: float,
        tenant_improvements_options: List[Dict[str, float]],
        lease_duration_years: int
    ) -> Dict[str, Any]:
        """
        Analyse coût/bénéfice des tenant improvements
        
        Compare différentes options de contribution aux travaux locataire
        
        Args:
            monthly_rent: Loyer mensuel
            tenant_improvements_options: [{"cost": 50000, "rent_increase": 500}, ...]
            lease_duration_years: Durée du bail
        
        Returns:
            Analyse de rentabilité pour chaque option
        """
        
        annual_rent = monthly_rent * 12
        total_lease_rent = annual_rent * lease_duration_years
        
        results = []
        
        for i, option in enumerate(tenant_improvements_options):
            cost = option.get("cost", 0)
            rent_increase = option.get("rent_increase", 0)  # Mensuel
            
            # Gain annuel
            annual_gain = rent_increase * 12
            total_gain = annual_gain * lease_duration_years
            
            # ROI
            net_gain = total_gain - cost
            roi = (net_gain / cost) * 100 if cost > 0 else 0
            
            # Payback
            payback_years = cost / annual_gain if annual_gain > 0 else None
            
            results.append({
                "option": i + 1,
                "investment": cost,
                "monthly_rent_increase": rent_increase,
                "annual_rent_increase": annual_gain,
                "total_additional_rent": round(total_gain, 2),
                "net_gain": round(net_gain, 2),
                "roi_pct": f"{roi:.2f}%",
                "payback_years": round(payback_years, 2) if payback_years else "N/A",
                "is_profitable": net_gain > 0,
                "profitability_ratio": round(total_gain / cost, 2) if cost > 0 else 0
            })
        
        # Meilleure option
        profitable_options = [r for r in results if r["is_profitable"]]
        best_option = max(profitable_options, key=lambda x: x["net_gain"]) if profitable_options else None
        
        return {
            "monthly_rent_base": monthly_rent,
            "lease_duration_years": lease_duration_years,
            "total_lease_rent_base": round(total_lease_rent, 2),
            "options_analysis": results,
            "recommendation": {
                "best_option": best_option["option"] if best_option else None,
                "best_net_gain": best_option["net_gain"] if best_option else 0,
                "best_roi": best_option["roi_pct"] if best_option else "0%"
            } if best_option else {"message": "Aucune option rentable"}
        }


# Instance globale
asset_management_service = AssetManagementService()
