"""
Service de calcul du taux d'intérêt avec algorithme de risque
Basé sur Euribor + marge selon profil de risque
"""
from typing import Dict, Any
from datetime import datetime
import httpx

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
            print(f"Erreur récupération Euribor depuis ECB: {e}")
        
        # Fallback sur valeur par défaut
        return self.DEFAULT_EURIBOR_12M if maturity == "12m" else self.DEFAULT_EURIBOR_3M
    
    def calculate_risk_score(
        self,
        project_data: Dict[str, Any],
        company_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calcule le score de risque du projet
        
        Returns:
            {
                "score": float (0-100),
                "category": str,
                "factors": Dict[str, float]
            }
        """
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
        showstoppers = project_data.get("showstoppers", [])
        regulatory_risk = min(10, len(showstoppers) * 3)
        score -= regulatory_risk
        factors["regulatory_risk"] = regulatory_risk
        
        # 5. Risque expérience entreprise (-0 à -15 points)
        experience_risk = self._assess_company_experience(company_data)
        score -= experience_risk
        factors["experience_risk"] = experience_risk
        
        # 6. Risque marché (-0 à -10 points)
        market_trend = project_data.get("market_trend", {}).get("trend", "stable")
        market_risk = 10 if market_trend == "baisse" else (5 if market_trend == "stable" else 0)
        score -= market_risk
        factors["market_risk"] = market_risk
        
        # 7. Risque technique (-0 à -15 points)
        technical_issues = project_data.get("technical_analysis", {}).get("major_issues", [])
        technical_risk = min(15, len(technical_issues) * 5)
        score -= technical_risk
        factors["technical_risk"] = technical_risk
        
        score = max(0, min(100, score))
        
        # Catégorisation
        if score >= 85:
            category = "excellent"
        elif score >= 70:
            category = "bon"
        elif score >= 50:
            category = "moyen"
        else:
            category = "risque"
        
        return {
            "score": round(score, 2),
            "category": category,
            "factors": factors,
            "interpretation": self._interpret_score(score)
        }
    
    async def calculate_interest_rate(
        self,
        project_data: Dict[str, Any],
        company_data: Dict[str, Any],
        loan_duration_months: int = 24
    ) -> Dict[str, Any]:
        """
        Calcule le taux d'intérêt personnalisé
        
        Returns:
            {
                "euribor_base": float,
                "risk_margin": float,
                "final_rate": float,
                "risk_score": Dict,
                "monthly_rate": float
            }
        """
        # 1. Récupérer Euribor
        maturity = "12m" if loan_duration_months >= 12 else "3m"
        euribor = await self.get_current_euribor(maturity)
        
        # 2. Calculer score de risque
        risk_assessment = self.calculate_risk_score(project_data, company_data)
        
        # 3. Déterminer marge de base
        base_margin = self.BASE_MARGIN[risk_assessment["category"]]
        
        # 4. Ajuster la marge selon facteurs spécifiques
        adjusted_margin = self._adjust_margin(
            base_margin,
            risk_assessment,
            project_data,
            company_data
        )
        
        # 5. Taux final
        final_rate = euribor + adjusted_margin
        
        # Plancher et plafond
        final_rate = max(3.0, min(8.0, final_rate))
        
        return {
            "euribor_base": round(euribor, 2),
            "base_margin": round(base_margin, 2),
            "adjusted_margin": round(adjusted_margin, 2),
            "final_rate": round(final_rate, 2),
            "monthly_rate": round(final_rate / 12, 4),
            "risk_score": risk_assessment,
            "duration_months": loan_duration_months,
            "recommendation": self._generate_rate_recommendation(final_rate)
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
