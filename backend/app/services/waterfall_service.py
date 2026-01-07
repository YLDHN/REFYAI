"""
Service de calcul de Waterfall Distribution avec Promote
Pour la distribution de profits entre LP (Limited Partners) et GP (General Partners)
"""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class WaterfallService:
    """
    Service de calcul de distribution waterfall avec paliers de promote
    
    Logique typique d'un fonds immobilier :
    - Palier 1 : 100% au LP jusqu'au Hurdle Rate (ex: 10% TRI)
    - Palier 2 : Catch-up au GP pour rattraper sa part
    - Palier 3 : Split (ex: 80% LP / 20% GP) au-delà du Hurdle
    
    Ou structure simplifiée :
    - < Hurdle : 100% LP / 0% GP
    - > Hurdle : 80% LP / 20% GP (Promote)
    """
    
    def calculate_waterfall_simple(
        self,
        lp_contrib: float,
        gp_investment: float = 0,
        profit: float = 0,
        hurdle_rate: float = 0.10,
        lp_share_below_hurdle: float = 1.0,
        lp_share_above_hurdle: float = 0.80,
        gp_share_above_hurdle: float = 0.20
    ) -> Dict[str, Any]:
        """
        Calcule une distribution waterfall simplifiée (2 paliers)
        
        Args:
            lp_contrib: Capital investi par le LP
            gp_investment: Capital investi par le GP (default: 0)
            profit: Profit total à distribuer
            hurdle_rate: Taux de rendement seuil (ex: 0.10 = 10%)
            lp_share_below_hurdle: Part LP en dessous du hurdle (défaut: 100%)
            lp_share_above_hurdle: Part LP au-dessus du hurdle (défaut: 80%)
            gp_share_above_hurdle: Part GP au-dessus du hurdle (défaut: 20%)
        
        Returns:
            Distribution détaillée LP/GP avec calculs
        """
        
        total_profit = profit
        equity_invested = lp_contrib + gp_investment
        
        # Validation
        if total_profit < 0:
            return {"success": False, "error": "Le profit total ne peut pas être négatif"}
        
        if equity_invested <= 0:
            return {"success": False, "error": "Le capital investi doit être positif"}
        
        if lp_share_below_hurdle + (1 - lp_share_below_hurdle) != 1.0:
            raise ValueError("Les parts doivent totaliser 100%")
        
        if lp_share_above_hurdle + gp_share_above_hurdle != 1.0:
            return {"success": False, "error": "Les parts au-dessus du hurdle doivent totaliser 100%"}
        
        # Calcul du TRI réalisé (approximation simple)
        # TRI = (Total Distribué / Capital) - 1
        total_distributed = equity_invested + total_profit
        actual_return_multiple = total_distributed / equity_invested
        actual_irr = actual_return_multiple - 1  # Simplification
        
        # Montant correspondant au Hurdle
        hurdle_profit = equity_invested * hurdle_rate
        
        result = {
            "success": True,
            "equity_invested": equity_invested,
            "total_profit": total_profit,
            "total_distributed": total_distributed,
            "hurdle_rate": hurdle_rate,
            "hurdle_rate_pct": f"{hurdle_rate * 100:.1f}%",
            "actual_irr": actual_irr,
            "actual_irr_pct": f"{actual_irr * 100:.2f}%",
            "hurdle_achieved": actual_irr >= hurdle_rate,
            "distribution": {}
        }
        
        # === CAS 1 : Profit inférieur au Hurdle ===
        if total_profit <= hurdle_profit:
            # 100% au LP (ou selon lp_share_below_hurdle)
            lp_distribution = equity_invested + (total_profit * lp_share_below_hurdle)
            gp_distribution = total_profit * (1 - lp_share_below_hurdle)
            
            result["lp_share"] = total_profit * lp_share_below_hurdle
            result["gp_share"] = gp_distribution
            result["distribution"] = {
                "scenario": "BELOW_HURDLE",
                "description": f"Profit inférieur au Hurdle de {hurdle_rate*100:.1f}%",
                "LP": {
                    "capital_return": equity_invested,
                    "profit_share": total_profit * lp_share_below_hurdle,
                    "total": lp_distribution,
                    "irr": (lp_distribution / equity_invested) - 1
                },
                "GP": {
                    "capital_return": 0,
                    "profit_share": gp_distribution,
                    "total": gp_distribution,
                    "promote": 0
                },
                "tiers": [
                    {
                        "tier": 1,
                        "description": "Return of Capital + Profit (below hurdle)",
                        "amount": total_profit,
                        "lp_share": total_profit * lp_share_below_hurdle,
                        "gp_share": total_profit * (1 - lp_share_below_hurdle)
                    }
                ]
            }
        
        # === CAS 2 : Profit supérieur au Hurdle ===
        else:
            # Montant en dessous du hurdle
            below_hurdle_profit = hurdle_profit
            
            # Montant au-dessus du hurdle
            above_hurdle_profit = total_profit - hurdle_profit
            
            # Distribution palier 1 (jusqu'au hurdle)
            lp_tier1 = equity_invested + (below_hurdle_profit * lp_share_below_hurdle)
            gp_tier1 = below_hurdle_profit * (1 - lp_share_below_hurdle)
            
            # Distribution palier 2 (au-dessus du hurdle avec promote)
            lp_tier2 = above_hurdle_profit * lp_share_above_hurdle
            gp_tier2 = above_hurdle_profit * gp_share_above_hurdle
            
            # Totaux
            lp_total_profit = (below_hurdle_profit * lp_share_below_hurdle) + lp_tier2
            gp_total_profit = gp_tier1 + gp_tier2
            lp_total = lp_tier1 + lp_tier2
            gp_total = gp_total_profit
            
            result["lp_share"] = lp_total_profit
            result["gp_share"] = gp_total_profit
            
            result["distribution"] = {
                "scenario": "ABOVE_HURDLE",
                "description": f"Profit supérieur au Hurdle de {hurdle_rate*100:.1f}% - Promote activé",
                "LP": {
                    "capital_return": equity_invested,
                    "tier1_profit": below_hurdle_profit * lp_share_below_hurdle,
                    "tier2_profit": lp_tier2,
                    "total_profit": lp_total_profit,
                    "total": lp_total,
                    "irr": (lp_total / equity_invested) - 1,
                    "irr_pct": f"{((lp_total / equity_invested) - 1) * 100:.2f}%"
                },
                "GP": {
                    "capital_return": 0,
                    "tier1_profit": gp_tier1,
                    "tier2_profit_promote": gp_tier2,
                    "total_profit": gp_tier1 + gp_tier2,
                    "total": gp_total,
                    "promote": gp_tier2,
                    "promote_pct": f"{gp_share_above_hurdle * 100:.1f}%"
                },
                "tiers": [
                    {
                        "tier": 1,
                        "description": f"Return of Capital + Profit jusqu'à {hurdle_rate*100:.1f}% IRR",
                        "amount": below_hurdle_profit,
                        "lp_share": below_hurdle_profit * lp_share_below_hurdle,
                        "gp_share": gp_tier1,
                        "lp_pct": f"{lp_share_below_hurdle * 100:.0f}%",
                        "gp_pct": f"{(1 - lp_share_below_hurdle) * 100:.0f}%"
                    },
                    {
                        "tier": 2,
                        "description": f"Profit au-dessus de {hurdle_rate*100:.1f}% IRR (Promote)",
                        "amount": above_hurdle_profit,
                        "lp_share": lp_tier2,
                        "gp_share": gp_tier2,
                        "lp_pct": f"{lp_share_above_hurdle * 100:.0f}%",
                        "gp_pct": f"{gp_share_above_hurdle * 100:.0f}%"
                    }
                ]
            }
        
        # Vérification
        total_check = (
            result["distribution"]["LP"]["total"] + 
            result["distribution"]["GP"]["total"]
        )
        
        if abs(total_check - total_distributed) > 0.01:
            logger.warning(
                f"Erreur de distribution waterfall: {total_check} != {total_distributed}"
            )
        
        return result
    
    def calculate_waterfall_advanced(
        self,
        total_profit: float,
        equity_invested: float,
        tiers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calcule une distribution waterfall avec paliers multiples personnalisés
        
        Args:
            total_profit: Profit total à distribuer
            equity_invested: Capital investi
            tiers: Liste de paliers [
                {
                    "threshold_irr": 0.08,  # Seuil IRR
                    "lp_share": 1.0,
                    "gp_share": 0.0
                },
                {
                    "threshold_irr": 0.15,
                    "lp_share": 0.80,
                    "gp_share": 0.20
                },
                ...
            ]
        
        Returns:
            Distribution détaillée par palier
        """
        
        # Trier les paliers par seuil croissant
        sorted_tiers = sorted(tiers, key=lambda x: x["threshold_irr"])
        
        # Calcul IRR réalisé
        total_distributed = equity_invested + total_profit
        actual_irr = (total_distributed / equity_invested) - 1
        
        distributions = []
        remaining_profit = total_profit
        lp_total = equity_invested  # Capital de base
        gp_total = 0
        
        for i, tier in enumerate(sorted_tiers):
            threshold_irr = tier["threshold_irr"]
            lp_share = tier["lp_share"]
            gp_share = tier["gp_share"]
            
            # Profit correspondant à ce seuil
            threshold_profit = equity_invested * threshold_irr
            
            # Profit déjà distribué dans les paliers précédents
            previous_profit = sum(d["amount"] for d in distributions)
            
            # Profit disponible pour ce palier
            profit_for_tier = min(
                threshold_profit - previous_profit,
                remaining_profit
            )
            
            if profit_for_tier > 0:
                lp_tier = profit_for_tier * lp_share
                gp_tier = profit_for_tier * gp_share
                
                distributions.append({
                    "tier": i + 1,
                    "threshold_irr": threshold_irr,
                    "threshold_irr_pct": f"{threshold_irr * 100:.1f}%",
                    "amount": profit_for_tier,
                    "lp_share": lp_tier,
                    "gp_share": gp_tier,
                    "lp_pct": f"{lp_share * 100:.0f}%",
                    "gp_pct": f"{gp_share * 100:.0f}%"
                })
                
                lp_total += lp_tier
                gp_total += gp_tier
                remaining_profit -= profit_for_tier
            
            # Si on a atteint le seuil de ce palier et qu'il reste du profit
            if remaining_profit > 0 and i == len(sorted_tiers) - 1:
                # Appliquer le dernier palier au reste
                lp_tier = remaining_profit * lp_share
                gp_tier = remaining_profit * gp_share
                
                distributions.append({
                    "tier": i + 2,
                    "threshold_irr": None,
                    "threshold_irr_pct": f">{threshold_irr * 100:.1f}%",
                    "amount": remaining_profit,
                    "lp_share": lp_tier,
                    "gp_share": gp_tier,
                    "lp_pct": f"{lp_share * 100:.0f}%",
                    "gp_pct": f"{gp_share * 100:.0f}%"
                })
                
                lp_total += lp_tier
                gp_total += gp_tier
                remaining_profit = 0
                break
        
        return {
            "equity_invested": equity_invested,
            "total_profit": total_profit,
            "total_distributed": total_distributed,
            "actual_irr": actual_irr,
            "actual_irr_pct": f"{actual_irr * 100:.2f}%",
            "distribution": {
                "LP": {
                    "total": lp_total,
                    "irr": (lp_total / equity_invested) - 1
                },
                "GP": {
                    "total": gp_total,
                    "total_promote": gp_total
                },
                "tiers": distributions
            }
        }
    
    def calculate_promote_sensitivity(
        self,
        equity_invested: float,
        profit_range: List[float],
        hurdle_rate: float = 0.10,
        promote_share: float = 0.20
    ) -> List[Dict[str, Any]]:
        """
        Analyse de sensibilité : impact du profit sur la distribution
        
        Utile pour visualiser l'effet du promote selon différents scénarios
        """
        
        results = []
        
        for profit in profit_range:
            waterfall = self.calculate_waterfall_simple(
                lp_contrib=equity_invested,
                gp_investment=0,
                profit=profit,
                hurdle_rate=hurdle_rate,
                gp_share_above_hurdle=promote_share
            )
            
            results.append({
                "profit": profit,
                "irr": waterfall["actual_irr"],
                "lp_total": waterfall["distribution"]["LP"]["total"],
                "gp_total": waterfall["distribution"]["GP"]["total"],
                "gp_promote": waterfall["distribution"]["GP"].get("promote", 0),
                "scenario": waterfall["distribution"]["scenario"]
            })
        
        return results


# Instance globale
waterfall_service = WaterfallService()
