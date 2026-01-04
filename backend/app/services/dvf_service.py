"""
Service d'intégration DVF (Demandes de Valeurs Foncières)
API officielle data.gouv.fr pour les prix du marché immobilier
"""
from typing import Dict, Any, List, Optional
import httpx
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DVFService:
    """Service d'accès aux données DVF (transactions immobilières)"""
    
    # API officielle DVF - data.gouv.fr via cquest
    BASE_URL = "https://api.cquest.org/dvf"
    
    # Codes INSEE des principales villes
    INSEE_CODES = {
        "Paris": "75056",
        "Lyon": "69123",
        "Marseille": "13055",
        "Toulouse": "31555",
        "Nice": "06088",
        "Nantes": "44109",
        "Montpellier": "34172",
        "Strasbourg": "67482",
        "Bordeaux": "33063",
        "Lille": "59350"
    }
    
    async def get_comparable_sales(
        self,
        commune: str,
        type_local: str = "Maison",
        rayon_km: float = 1.0,
        months_back: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Récupère les ventes comparables DVF via API officielle
        
        Args:
            commune: Nom de la commune ou code INSEE
            type_local: Maison, Appartement, Local commercial, etc.
            rayon_km: Rayon de recherche en km (converti en mètres)
            months_back: Nombre de mois en arrière
        
        Returns:
            Liste des ventes comparables
        """
        # Convertir nom commune en code INSEE si nécessaire
        code_commune = self.INSEE_CODES.get(commune, commune)
        
        date_min = (datetime.now() - timedelta(days=months_back*30)).strftime("%Y-%m-%d")
        
        params = {
            "code_commune": code_commune,
            "type_local": type_local,
            "nature_mutation": "Vente",
            "date_debut": date_min
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.BASE_URL,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("resultats", [])
                
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP DVF API ({e.response.status_code}): {e}")
            return []
        except httpx.RequestError as e:
            logger.error(f"Erreur réseau DVF API: {e}")
            return []
        except Exception as e:
            logger.error(f"Erreur inattendue DVF API: {e}")
            return []
    
    async def calculate_market_value(
        self,
        address: str,
        surface: float,
        commune: str,
        type_bien: str = "appartement"
    ) -> Dict[str, Any]:
        """
        Calcule la valeur de marché basée sur DVF
        
        Returns:
            {
                "prix_median_m2": float,
                "prix_moyen_m2": float,
                "estimation_basse": float,
                "estimation_haute": float,
                "estimation_mediane": float,
                "nombre_comparables": int,
                "comparables": List[Dict]
            }
        """
        comparables = await self.get_comparable_sales(
            commune=commune,
            type_local=type_bien.capitalize()
        )
        
        if not comparables:
            return {
                "error": "Aucune donnée DVF disponible pour cette zone",
                "prix_median_m2": 0,
                "prix_moyen_m2": 0,
                "estimation_basse": 0,
                "estimation_haute": 0,
                "estimation_mediane": 0,
                "nombre_comparables": 0,
                "comparables": []
            }
        
        # Calculer prix au m²
        prix_m2_list = []
        for comp in comparables:
            if comp.get("surface_reelle_bati") and comp.get("valeur_fonciere"):
                prix_m2 = comp["valeur_fonciere"] / comp["surface_reelle_bati"]
                if 500 < prix_m2 < 50000:  # Filtrer les aberrations
                    prix_m2_list.append(prix_m2)
        
        if not prix_m2_list:
            return {
                "error": "Données DVF insuffisantes",
                "nombre_comparables": len(comparables)
            }
        
        prix_m2_list.sort()
        prix_median_m2 = prix_m2_list[len(prix_m2_list) // 2]
        prix_moyen_m2 = sum(prix_m2_list) / len(prix_m2_list)
        
        # Percentiles pour estimation
        p25 = prix_m2_list[len(prix_m2_list) // 4]
        p75 = prix_m2_list[3 * len(prix_m2_list) // 4]
        
        return {
            "prix_median_m2": round(prix_median_m2, 2),
            "prix_moyen_m2": round(prix_moyen_m2, 2),
            "estimation_basse": round(p25 * surface, 2),
            "estimation_haute": round(p75 * surface, 2),
            "estimation_mediane": round(prix_median_m2 * surface, 2),
            "nombre_comparables": len(prix_m2_list),
            "comparables": self._format_comparables(comparables[:10])  # Top 10
        }
    
    async def analyze_market_trend(
        self,
        commune: str,
        type_bien: str = "appartement"
    ) -> Dict[str, Any]:
        """
        Analyse la tendance du marché
        
        Returns:
            {
                "trend": "hausse" | "baisse" | "stable",
                "evolution_12m": float (% de variation),
                "prix_median_actuel": float,
                "prix_median_12m": float
            }
        """
        # Données 12 derniers mois
        recent = await self.get_comparable_sales(
            commune=commune,
            type_local=type_bien.capitalize(),
            months_back=12
        )
        
        # Données 12-24 mois
        old = await self.get_comparable_sales(
            commune=commune,
            type_local=type_bien.capitalize(),
            months_back=24
        )
        
        recent_prices = self._extract_prices_m2(recent)
        old_prices = self._extract_prices_m2(old[:len(old)//2])  # Première moitié = données anciennes
        
        if not recent_prices or not old_prices:
            return {"error": "Données insuffisantes pour analyse tendance"}
        
        prix_recent = sum(recent_prices) / len(recent_prices)
        prix_old = sum(old_prices) / len(old_prices)
        
        evolution = ((prix_recent - prix_old) / prix_old) * 100
        
        if evolution > 3:
            trend = "hausse"
        elif evolution < -3:
            trend = "baisse"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "evolution_12m": round(evolution, 2),
            "prix_median_actuel": round(prix_recent, 2),
            "prix_median_12m": round(prix_old, 2),
            "interpretation": self._interpret_trend(trend, evolution)
        }
    
    def _extract_prices_m2(self, comparables: List[Dict]) -> List[float]:
        """Extrait les prix au m² valides"""
        prix = []
        for comp in comparables:
            if comp.get("surface_reelle_bati") and comp.get("valeur_fonciere"):
                prix_m2 = comp["valeur_fonciere"] / comp["surface_reelle_bati"]
                if 500 < prix_m2 < 50000:
                    prix.append(prix_m2)
        return prix
    
    def _format_comparables(self, comparables: List[Dict]) -> List[Dict]:
        """Formate les comparables pour affichage"""
        formatted = []
        for comp in comparables:
            formatted.append({
                "date_mutation": comp.get("date_mutation"),
                "adresse": f"{comp.get('numero_voie', '')} {comp.get('type_voie', '')} {comp.get('voie', '')}",
                "prix": comp.get("valeur_fonciere"),
                "surface": comp.get("surface_reelle_bati"),
                "prix_m2": round(comp.get("valeur_fonciere", 0) / comp.get("surface_reelle_bati", 1), 2) if comp.get("surface_reelle_bati") else 0,
                "type": comp.get("type_local"),
                "nombre_pieces": comp.get("nombre_pieces_principales")
            })
        return formatted
    
    def _interpret_trend(self, trend: str, evolution: float) -> str:
        """Interprète la tendance pour conseil métier"""
        if trend == "hausse":
            return f"Marché en hausse de {abs(evolution):.1f}% sur 12 mois. Opportunité d'investissement si TRI > 8%. Attention au risque de bulle."
        elif trend == "baisse":
            return f"Marché en baisse de {abs(evolution):.1f}% sur 12 mois. Opportunité d'achat mais prudence sur la revente. Privilégier stratégie locative longue."
        else:
            return f"Marché stable (±{abs(evolution):.1f}%). Conditions normales d'investissement."


class MarketAnalysisService:
    """Service d'analyse de marché immobilier"""
    
    def __init__(self):
        self.dvf_service = DVFService()
    
    async def full_market_analysis(
        self,
        project_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyse complète du marché pour un projet
        
        Returns:
            Rapport d'analyse avec prix, tendances et recommandations
        """
        commune = project_data.get("commune") or project_data.get("city")
        surface = project_data.get("surface") or 100
        type_bien = project_data.get("type_bien") or "appartement"
        
        # Valeur de marché
        market_value = await self.dvf_service.calculate_market_value(
            address=project_data.get("address", ""),
            surface=surface,
            commune=commune,
            type_bien=type_bien
        )
        
        # Tendance marché
        trend = await self.dvf_service.analyze_market_trend(
            commune=commune,
            type_bien=type_bien
        )
        
        # Analyse de compétitivité
        purchase_price = project_data.get("purchase_price", 0)
        estimated_value = market_value.get("estimation_mediane", 0)
        
        discount = 0
        if purchase_price and estimated_value:
            discount = ((estimated_value - purchase_price) / estimated_value) * 100
        
        return {
            "market_value": market_value,
            "market_trend": trend,
            "competitiveness": {
                "purchase_price": purchase_price,
                "estimated_market_value": estimated_value,
                "discount_percentage": round(discount, 2),
                "is_good_deal": discount > 10,
                "recommendation": self._generate_recommendation(discount, trend)
            },
            "exit_strategy": self._recommend_exit_strategy(trend, discount)
        }
    
    def _generate_recommendation(self, discount: float, trend: Dict) -> str:
        """Génère une recommandation d'achat"""
        if discount > 20:
            return "Très bonne affaire ! Prix d'achat 20%+ sous le marché."
        elif discount > 10:
            return "Bonne opportunité. Décote intéressante par rapport au marché."
        elif discount > 0:
            return "Prix dans le marché. Rentabilité à analyser selon travaux."
        elif discount > -10:
            return "Prix légèrement élevé. Négocier ou vérifier le potentiel."
        else:
            return "⚠️ Prix très au-dessus du marché. Risque de perte à la revente."
    
    def _recommend_exit_strategy(self, trend: Dict, discount: float) -> Dict[str, Any]:
        """Recommande une stratégie de sortie"""
        if trend.get("trend") == "hausse" and discount > 10:
            return {
                "recommended": "revente_court_terme",
                "reasoning": "Marché haussier + bon prix d'achat = profiter de la plus-value rapidement",
                "timeline": "18-36 mois",
                "expected_upside": "15-25%"
            }
        elif trend.get("trend") == "baisse":
            return {
                "recommended": "location_longue",
                "reasoning": "Marché baissier = privilégier revenus locatifs et attendre reprise",
                "timeline": "5-10 ans",
                "expected_upside": "Rendement locatif + appréciation future"
            }
        else:
            return {
                "recommended": "mixte",
                "reasoning": "Marché stable = location puis revente selon opportunités",
                "timeline": "3-5 ans",
                "expected_upside": "TRI optimal 8-12%"
            }
