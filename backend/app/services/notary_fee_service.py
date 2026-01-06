"""
Service de calcul intelligent des frais de notaire
Adaptation automatique selon profil acheteur et ancienneté du bien
"""
from typing import Dict, Any, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class BuyerProfile(str, Enum):
    """Profils d'acheteurs avec régimes fiscaux différents"""
    NEUF = "NEUF"  # Achat en VEFA ou < 5 ans après achèvement
    MDB = "MDB"  # Marchand de Biens (professionnel)
    INVESTOR = "INVESTOR"  # Investisseur classique (> 5 ans)
    
    def __str__(self):
        return self.value


class NotaryFeeService:
    """
    Service de calcul des frais de notaire avec intelligence fiscale
    
    Règles métier :
    - NEUF (VEFA ou < 5 ans) : ~2.5% (droits réduits)
    - MDB < 5 ans : ~3% (TVA sur marge possible)
    - MDB > 5 ans : ~3% MAIS ALERTE FISCALE (risque de requalification)
    - INVESTOR > 5 ans : ~7.5% (droits pleins)
    """
    
    # Taux de base par profil
    RATE_NEUF = 0.025  # 2.5% - Droits de mutation réduits
    RATE_MDB_VALID = 0.030  # 3% - Régime TVA sur marge valide
    RATE_INVESTOR_OLD = 0.075  # 7.5% - Droits de mutation pleins
    
    # Seuils
    AGE_THRESHOLD_YEARS = 5  # Limite pour régime réduit
    
    def calculate_notary_fees(
        self,
        purchase_price: float,
        buyer_profile: str,
        building_age_years: Optional[int] = None,
        construction_completion_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calcule les frais de notaire avec alertes fiscales
        
        Args:
            purchase_price: Prix d'achat HT ou TTC
            buyer_profile: "NEUF", "MDB", "INVESTOR"
            building_age_years: Ancienneté du bien (en années depuis achèvement)
            construction_completion_date: Date d'achèvement (pour calcul précis)
        
        Returns:
            {
                "purchase_price": float,
                "notary_fee_rate": float,
                "notary_fee_amount": float,
                "total_acquisition_cost": float,
                "buyer_profile": str,
                "building_age_years": int,
                "regime": str,  # "DROITS_REDUITS", "TVA_MARGE", "DROITS_PLEINS"
                "alert": str | None,  # Alerte fiscale éventuelle
                "alert_severity": str | None,  # "INFO", "WARNING", "CRITICAL"
                "breakdown": Dict  # Détail des frais
            }
        """
        
        # Validation
        if purchase_price <= 0:
            raise ValueError("Le prix d'achat doit être positif")
        
        if buyer_profile not in ["NEUF", "MDB", "INVESTOR"]:
            raise ValueError(f"Profil invalide: {buyer_profile}. Attendu: NEUF, MDB ou INVESTOR")
        
        # Initialisation
        result = {
            "purchase_price": purchase_price,
            "buyer_profile": buyer_profile,
            "building_age_years": building_age_years,
            "alert": None,
            "alert_severity": None
        }
        
        # === CAS 1 : NEUF (VEFA ou immeuble récent) ===
        if buyer_profile == "NEUF":
            rate = self.RATE_NEUF
            result["regime"] = "DROITS_REDUITS"
            result["notary_fee_rate"] = rate
            result["notary_fee_amount"] = purchase_price * rate
            result["breakdown"] = self._breakdown_neuf(purchase_price)
            
            # Info : Vérifier que bien < 5 ans
            if building_age_years and building_age_years > self.AGE_THRESHOLD_YEARS:
                result["alert"] = (
                    f"⚠️ ATTENTION : Bien de {building_age_years} ans mais profil NEUF. "
                    f"Vérifier éligibilité aux droits réduits (< 5 ans après achèvement requis)."
                )
                result["alert_severity"] = "WARNING"
        
        # === CAS 2 : MARCHAND DE BIENS (MDB) ===
        elif buyer_profile == "MDB":
            if building_age_years is None:
                # Pas d'info sur l'âge : appliquer taux standard avec avertissement
                rate = self.RATE_MDB_VALID
                result["regime"] = "TVA_MARGE"
                result["alert"] = (
                    "ℹ️ INFO : Âge du bien non fourni. Taux MDB appliqué (3%). "
                    "Vérifier éligibilité au régime TVA sur marge."
                )
                result["alert_severity"] = "INFO"
            
            elif building_age_years <= self.AGE_THRESHOLD_YEARS:
                # MDB valide : bien récent
                rate = self.RATE_MDB_VALID
                result["regime"] = "TVA_MARGE"
                result["alert"] = None
            
            else:
                # MDB sur bien ancien : ALERTE CRITIQUE
                rate = self.RATE_MDB_VALID
                result["regime"] = "TVA_MARGE_RISQUE"
                
                # Calcul du risque fiscal
                rate_difference = self.RATE_INVESTOR_OLD - self.RATE_MDB_VALID
                potential_additional_cost = purchase_price * rate_difference
                
                result["alert"] = (
                    f"🚨 RISQUE FISCAL MAJEUR : Bien de {building_age_years} ans avec profil MDB.\n"
                    f"Le régime TVA sur marge n'est valable que pour les biens < {self.AGE_THRESHOLD_YEARS} ans.\n"
                    f"Risque de requalification par l'administration fiscale :\n"
                    f"  - Taux appliqué : {rate * 100:.1f}%\n"
                    f"  - Taux si requalification : {self.RATE_INVESTOR_OLD * 100:.1f}%\n"
                    f"  - Rattrapage fiscal potentiel : {potential_additional_cost:,.0f} €\n"
                    f"RECOMMANDATION : Provisionner {potential_additional_cost:,.0f} € ou passer en profil INVESTOR."
                )
                result["alert_severity"] = "CRITICAL"
                result["potential_additional_cost"] = potential_additional_cost
                result["recommended_rate"] = self.RATE_INVESTOR_OLD
            
            result["notary_fee_rate"] = rate
            result["notary_fee_amount"] = purchase_price * rate
            result["breakdown"] = self._breakdown_mdb(purchase_price)
        
        # === CAS 3 : INVESTISSEUR (Régime classique) ===
        elif buyer_profile == "INVESTOR":
            rate = self.RATE_INVESTOR_OLD
            result["regime"] = "DROITS_PLEINS"
            result["notary_fee_rate"] = rate
            result["notary_fee_amount"] = purchase_price * rate
            result["breakdown"] = self._breakdown_investor(purchase_price)
            
            # Info : Si bien récent, possibilité de droits réduits
            if building_age_years and building_age_years <= self.AGE_THRESHOLD_YEARS:
                savings = purchase_price * (self.RATE_INVESTOR_OLD - self.RATE_NEUF)
                result["alert"] = (
                    f"💡 OPTIMISATION : Bien de {building_age_years} ans éligible aux droits réduits.\n"
                    f"Économie potentielle : {savings:,.0f} € en passant en profil NEUF.\n"
                    f"Vérifier les conditions d'éligibilité avec le notaire."
                )
                result["alert_severity"] = "INFO"
        
        # Coût total acquisition
        result["total_acquisition_cost"] = purchase_price + result["notary_fee_amount"]
        
        # Logs
        logger.info(
            f"Calcul frais notaire : {purchase_price:,.0f}€ x {rate*100:.2f}% = {result['notary_fee_amount']:,.0f}€ "
            f"(Profil: {buyer_profile}, Âge: {building_age_years} ans)"
        )
        
        if result["alert"]:
            logger.warning(f"Alerte fiscale [{result['alert_severity']}] : {result['alert']}")
        
        return result
    
    def _breakdown_neuf(self, price: float) -> Dict[str, float]:
        """Décomposition des frais pour NEUF"""
        return {
            "droits_enregistrement": price * 0.00715,  # 0.715% (réduit)
            "taxe_publicite_fonciere": 0,  # Exonéré en VEFA
            "emoluments_notaire": price * 0.01,  # ~1%
            "debours_formalites": price * 0.00785,  # ~0.785%
            "contribution_securite_immobiliere": 0.1 * price * 0.00715,  # 0.1% des droits
            "tva_emoluments": price * 0.01 * 0.20  # TVA 20% sur émoluments
        }
    
    def _breakdown_mdb(self, price: float) -> Dict[str, float]:
        """Décomposition des frais pour MDB"""
        return {
            "droits_enregistrement": price * 0.0125,  # ~1.25% (TVA sur marge)
            "taxe_publicite_fonciere": price * 0.001,
            "emoluments_notaire": price * 0.0095,
            "debours_formalites": price * 0.0065,
            "contribution_securite_immobiliere": 0.1 * price * 0.0125,
            "tva_emoluments": price * 0.0095 * 0.20
        }
    
    def _breakdown_investor(self, price: float) -> Dict[str, float]:
        """Décomposition des frais pour INVESTOR"""
        return {
            "droits_enregistrement": price * 0.05814,  # 5.814% (département + commune)
            "taxe_publicite_fonciere": price * 0.00715,  # 0.715%
            "emoluments_notaire": price * 0.00825,  # ~0.825% (dégressif)
            "debours_formalites": price * 0.00146,
            "contribution_securite_immobiliere": 0.1 * price * 0.05814,
            "frais_divers": 500  # Forfait
        }
    
    def compare_profiles(
        self,
        purchase_price: float,
        building_age_years: int
    ) -> Dict[str, Any]:
        """
        Compare les frais selon différents profils pour aide à la décision
        
        Args:
            purchase_price: Prix d'achat
            building_age_years: Ancienneté du bien
        
        Returns:
            Comparaison des 3 profils avec recommandation
        """
        results = {}
        
        for profile in ["NEUF", "MDB", "INVESTOR"]:
            results[profile] = self.calculate_notary_fees(
                purchase_price=purchase_price,
                buyer_profile=profile,
                building_age_years=building_age_years
            )
        
        # Recommandation
        if building_age_years <= self.AGE_THRESHOLD_YEARS:
            recommended = "NEUF"
            reason = f"Bien de {building_age_years} ans éligible aux droits réduits"
        else:
            recommended = "INVESTOR"
            reason = f"Bien de {building_age_years} ans : régime standard requis"
        
        return {
            "purchase_price": purchase_price,
            "building_age_years": building_age_years,
            "profiles": results,
            "recommended_profile": recommended,
            "recommendation_reason": reason,
            "savings_vs_standard": (
                results["INVESTOR"]["notary_fee_amount"] - 
                results[recommended]["notary_fee_amount"]
            )
        }


# Instance globale
notary_fee_service = NotaryFeeService()
