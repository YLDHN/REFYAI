"""
Service de calcul du taux d'intérêt avec algorithme de risque
Basé sur Euribor + marge selon profil de risque
"""
from typing import Dict, Any
from datetime import datetime
import httpx
import logging

logger = logging.getLogger(__name__)

class InterestRateService:
    """Service de calcul algorithmique des taux d'intérêt"""
    
    # Taux Euribor par défaut (à mettre à jour via API)
    DEFAULT_EURIBOR_3M = 3.65  # Au 31/12/2025
    DEFAULT_EURIBOR_12M = 3.45
    
    # Marges de base selon profil
    BASE_MARGIN = {
        "excellent": 0.80,   # Fonds PE AAA
        "bon": 1.20,         # Fonds value-add établis
        "moyen": 1.80,       # Promoteurs moyens
        "risque": 2.50       # Nouveaux entrants
    }
    
    async def get_current_euribor(self, maturity: str = "12m") -> float:
        """
        Récupère le taux Euribor actuel via API ECB (Banque Centrale Européenne)
        
        Args:
            maturity: "3m", "6m" ou "12m"
        
        Returns:
            Taux Euribor en %
        """
        try:
            # API ECB (European Central Bank) - GRATUITE
            maturity_codes = {
                "3m": "EURIBOR3MD_",
                "6m": "EURIBOR6MD_",
                "12m": "EURIBOR12MD_"
            }
            
            code = maturity_codes.get(maturity, "EURIBOR12MD_")
            
            async with httpx.AsyncClient() as client:
                url = f"https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.RT.MM.{code}.HSTA"
                params = {
                    "format": "jsondata",
                    "lastNObservations": 1
                }
                
                response = await client.get(url, params=params, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    # Extraire le taux de la réponse ECB
                    try:
                        rate = data["dataSets"][0]["series"]["0:0:0:0:0:0:0"]["observations"]["0"][0]
                        return float(rate)
                    except (KeyError, IndexError, TypeError):
                        pass
                        
        except Exception as e:
            logger.error(f"Erreur récupération Euribor depuis ECB: {e}")
        
        # Fallback sur valeur par défaut
        return self.DEFAULT_EURIBOR_12M if maturity == "12m" else self.DEFAULT_EURIBOR_3M
    
    def calculate_risk_score(
        self,
        project_data: Dict[str, Any],
        company_data: Dict[str, Any],
        market_trend: str = "stable",
        technical_issues: list = None
    ) -> float:
        """
        Calcule le score de risque du projet
        
        Args:
            project_data: Données du projet
            company_data: Données de l'entreprise  
            market_trend: Tendance du marché ("hausse", "stable", "baisse")
            technical_issues: Liste des problèmes techniques
        
        Returns:
            Score de risque (0-100)
        """
        if technical_issues is None:
            technical_issues = []
            
        score = 100.0
        factors = {}
        
        # 1. Risque géographique (-0 à -15 points)
        location_risk = self._assess_location_risk(project_data.get("city", ""))
        score -= location_risk
        factors["location_risk"] = location_risk
        
        # 2. Risque LTV (-0 à -20 points)
        ltv = project_data.get("ltv", 0)
        ltv_risk = max(0, (ltv - 0.65) * 40) if ltv > 0.65 else 0
        score -= ltv_risk
        factors["ltv_risk"] = ltv_risk
        
        # 3. Risque TRI (-0 à -15 points)
        tri = project_data.get("tri", 0)
        tri_risk = max(0, (10 - tri) * 1.5) if tri < 10 else 0
        score -= tri_risk
        factors["tri_risk"] = tri_risk
        
        # 4. Risque réglementaire (-0 à -10 points)
        showstoppers_count = project_data.get("showstoppers_count", 0)
        regulatory_risk = min(10, showstoppers_count * 3)
        score -= regulatory_risk
        factors["regulatory_risk"] = regulatory_risk
        
        # 5. Risque expérience entreprise (-0 à -15 points)
        experience_risk = self._assess_company_experience(company_data)
        score -= experience_risk
        factors["experience_risk"] = experience_risk
        
        # 6. Risque marché (-0 à -10 points)
        market_risk = 10 if market_trend == "baisse" else (5 if market_trend == "stable" else 0)
        score -= market_risk
        factors["market_risk"] = market_risk
        
        # 7. Risque technique (-0 à -15 points)
        technical_risk = min(15, len(technical_issues) * 5)
        score -= technical_risk
        factors["technical_risk"] = technical_risk
        
        score = max(0, min(100, score))
        
        return round(score, 2)
    
    async def calculate_interest_rate(
        self,
        project_data: Dict[str, Any],
        company_data: Dict[str, Any],
        loan_duration_months: int = 24,
        market_trend: str = "stable",
        technical_issues: list = None
    ) -> Dict[str, Any]:
        """
        Calcule le taux d'intérêt personnalisé
        
        Args:
            project_data: Données du projet
            company_data: Données de l'entreprise
            loan_duration_months: Durée du prêt en mois
            market_trend: Tendance du marché
            technical_issues: Liste des problèmes techniques
        
        Returns:
            {
                "euribor": float,
                "margin": float,
                "interest_rate": float,
                "risk_score": float,
                "category": str,
                "monthly_rate": float
            }
        """
        if technical_issues is None:
            technical_issues = []
            
        # 1. Récupérer Euribor
        maturity = "12m" if loan_duration_months >= 12 else "3m"
        euribor = await self.get_current_euribor(maturity)
        
        # 2. Calculer score de risque
        risk_score = self.calculate_risk_score(
            project_data, 
            company_data, 
            market_trend,
            technical_issues
        )
        
        # 3. Déterminer catégorie et marge de base
        if risk_score >= 85:
            category = "excellent"
        elif risk_score >= 70:
            category = "bon"
        elif risk_score >= 50:
            category = "moyen"
        else:
            category = "risque"
            
        base_margin = self.BASE_MARGIN[category]
        
        # 4. Ajuster la marge selon facteurs spécifiques
        adjusted_margin = base_margin
        
        # Ajustements fins
        if project_data.get("ltv", 0) > 80:
            adjusted_margin += 0.3
        if project_data.get("tri", 0) < 8:
            adjusted_margin += 0.2
        
        # 5. Taux final
        interest_rate = euribor + adjusted_margin
        
        # Plancher et plafond
        interest_rate = max(3.0, min(8.0, interest_rate))
        
        return {
            "euribor": round(euribor, 2),
            "margin": round(adjusted_margin, 2),
            "interest_rate": round(interest_rate, 2),
            "risk_score": round(risk_score, 2),
            "category": category,
            "monthly_rate": round(interest_rate / 12, 4),
            "duration_months": loan_duration_months
        }
    
    def _assess_location_risk(self, city: str) -> float:
        """Évalue le risque géographique"""
        # Villes tier 1 (faible risque)
        tier1_cities = ["paris", "lyon", "marseille", "toulouse", "bordeaux", "nantes", "nice", "strasbourg"]
        
        city_lower = city.lower()
        if any(t1 in city_lower for t1 in tier1_cities):
            return 0.0
        else:
            return 8.0  # Tier 2-3: risque moyen
    
    def _assess_company_experience(self, company_data: Dict[str, Any]) -> float:
        """Évalue l'expérience de l'entreprise"""
        years_experience = company_data.get("years_experience", 0)
        projects_completed = company_data.get("projects_completed", 0)
        
        if years_experience >= 10 and projects_completed >= 20:
            return 0.0
        elif years_experience >= 5 and projects_completed >= 10:
            return 5.0
        elif years_experience >= 2 and projects_completed >= 3:
            return 10.0
        else:
            return 15.0
    
    def _adjust_margin(
        self,
        base_margin: float,
        risk_assessment: Dict,
        project_data: Dict,
        company_data: Dict
    ) -> float:
        """Ajuste la marge selon facteurs additionnels"""
        margin = base_margin
        
        # Bonus si TRI très élevé
        tri = project_data.get("tri", 0)
        if tri > 15:
            margin -= 0.20
        
        # Pénalité si LTV > 80%
        ltv = project_data.get("ltv", 0)
        if ltv > 0.80:
            margin += 0.30
        
        # Bonus fidélité client
        if company_data.get("client_existant"):
            margin -= 0.15
        
        # Bonus garanties additionnelles
        if company_data.get("garanties_supplementaires"):
            margin -= 0.25
        
        return max(0.5, margin)  # Marge minimum 0.5%
    
    def _interpret_score(self, score: float) -> str:
        """Interprète le score de risque"""
        if score >= 85:
            return "Profil excellent. Risque très faible. Conditions de financement optimales."
        elif score >= 70:
            return "Bon profil. Risque modéré. Financement favorable."
        elif score >= 50:
            return "Profil moyen. Risque standard. Conditions de marché."
        else:
            return "Profil risqué. Financement difficile ou taux élevés. Améliorer le projet."
    
    def _generate_rate_recommendation(self, rate: float) -> str:
        """Génère une recommandation sur le taux"""
        if rate < 4.0:
            return "Taux très compétitif. Excellent contexte de financement."
        elif rate < 5.0:
            return "Taux favorable. Conditions normales de marché."
        elif rate < 6.0:
            return "Taux correct mais amélioration possible. Négocier ou optimiser le projet."
        else:
            return "Taux élevé. Revoir la structure financière ou renforcer les fonds propres."


class LoanStructuringService:
    """Service de structuration de financement"""
    
    def __init__(self):
        self.rate_service = InterestRateService()
    
    async def optimize_loan_structure(
        self,
        project_data: Dict[str, Any],
        company_data: Dict[str, Any],
        target_ltv: float = 0.75
    ) -> Dict[str, Any]:
        """
        Optimise la structure de financement
        
        Returns:
            Meilleure structure dette/equity avec taux optimisés
        """
        total_cost = (
            project_data.get("purchase_price", 0) +
            project_data.get("renovation_budget", 0) +
            project_data.get("fees", 0)
        )
        
        # Calcul dette optimale
        optimal_debt = total_cost * target_ltv
        optimal_equity = total_cost - optimal_debt
        
        # Taux d'intérêt
        rate_info = await self.rate_service.calculate_interest_rate(
            project_data,
            company_data
        )
        
        # Mensualités
        monthly_rate = rate_info["monthly_rate"] / 100
        duration_months = 24
        monthly_payment = optimal_debt * monthly_rate / (1 - (1 + monthly_rate) ** -duration_months)
        
        return {
            "total_cost": total_cost,
            "optimal_debt": round(optimal_debt, 2),
            "optimal_equity": round(optimal_equity, 2),
            "ltv": target_ltv,
            "interest_rate": rate_info,
            "monthly_payment": round(monthly_payment, 2),
            "total_interest": round(monthly_payment * duration_months - optimal_debt, 2),
            "recommendation": "Structure optimisée selon profil de risque et marché actuel"
        }
