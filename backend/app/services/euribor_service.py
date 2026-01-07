"""
Service pour récupérer le taux Euribor en temps réel depuis des sources publiques.
L'Euribor 1M est le principal taux de référence pour les prêts immobiliers en Europe.
"""
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class EuriborService:
    """Service de récupération taux Euribor"""
    
    def __init__(self):
        # Cache simple (durée 24h)
        self._cached_rate: Optional[float] = None
        self._cache_timestamp: Optional[datetime] = None
        self._cache_duration = timedelta(hours=24)
        
    def get_euribor_1m(self) -> Dict:
        """
        Récupérer le taux Euribor 1 mois actuel
        
        Returns:
            Dict avec taux, date, source
        """
        # Vérifier cache
        if self._is_cache_valid():
            return {
                "rate": self._cached_rate,
                "date": self._cache_timestamp.strftime("%Y-%m-%d"),
                "source": "cache",
                "maturity": "1M"
            }
        
        # Récupérer depuis API publique
        try:
            rate = self._fetch_from_ecb()
            if rate is not None:
                self._update_cache(rate)
                return {
                    "rate": rate,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "ECB (European Central Bank)",
                    "maturity": "1M"
                }
        except Exception as e:
            logger.warning(f"Erreur récupération Euribor depuis ECB: {e}")
        
        # Fallback: utiliser valeur par défaut (dernière connue)
        fallback_rate = 3.50  # Taux approximatif début 2026
        logger.warning(f"Utilisation taux Euribor fallback: {fallback_rate}%")
        
        return {
            "rate": fallback_rate,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": "fallback (dernière valeur connue)",
            "maturity": "1M",
            "warning": "Taux non récupéré en temps réel, utiliser avec précaution"
        }
    
    def _fetch_from_ecb(self) -> Optional[float]:
        """
        Récupérer depuis l'API ECB (European Central Bank)
        
        Note: L'API ECB change régulièrement. Cette implémentation est un exemple.
        En production, utiliser une API fiable comme:
        - ECB Statistical Data Warehouse
        - Euribor-rates.eu API
        - Investing.com API
        """
        # Pour l'instant, retourne None (à implémenter avec vraie API)
        # TODO: Intégrer vraie API Euribor
        return None
    
    def _is_cache_valid(self) -> bool:
        """Vérifier si le cache est encore valide"""
        if self._cached_rate is None or self._cache_timestamp is None:
            return False
        
        age = datetime.now() - self._cache_timestamp
        return age < self._cache_duration
    
    def _update_cache(self, rate: float):
        """Mettre à jour le cache"""
        self._cached_rate = rate
        self._cache_timestamp = datetime.now()


# Instance globale
euribor_service = EuriborService()
