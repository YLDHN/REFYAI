"""
Service de calculs financiers immobiliers
"""
from typing import Dict, Any, List
from enum import Enum
from datetime import datetime
import numpy as np
from scipy.optimize import newton


class AmortizationType(str, Enum):
    """Types d'amortissement de prêt"""
    CLASSIC = "classic"  # Amortissement constant (mensualités fixes)
    IN_FINE = "in_fine"  # Remboursement du capital en fin de prêt
    DEFERRED = "deferred"  # Différé d'amortissement pendant travaux
    
    def __str__(self):
        return self.value


class FinancialService:
    
    def calculate_tri(
        self,
        initial_investment: float,
        cash_flows: list[float],
        periods: int = 20
    ) -> float:
        """
        Calcule le Taux de Rendement Interne (TRI/IRR)
        
        Args:
            initial_investment: Investissement initial
            cash_flows: Flux de trésorerie par période
            periods: Nombre de périodes
        
        Returns:
            TRI en pourcentage
        """
        
        def npv(rate):
            """Calcule la VAN pour un taux donné"""
            return -initial_investment + sum(
                cf / (1 + rate) ** (i + 1) for i, cf in enumerate(cash_flows)
            )
        
        try:
            tri = newton(npv, 0.1)  # On commence avec 10% comme estimation
            return tri
        except:
            return 0.0
    
    def calculate_van(
        self,
        initial_investment: float,
        cash_flows: list[float],
        discount_rate: float = 0.08
    ) -> float:
        """
        Calcule la Valeur Actuelle Nette (VAN/NPV)
        
        Args:
            initial_investment: Investissement initial
            cash_flows: Flux de trésorerie par période
            discount_rate: Taux d'actualisation
        
        Returns:
            VAN
        """
        
        van = -initial_investment
        for i, cf in enumerate(cash_flows):
            van += cf / ((1 + discount_rate) ** (i + 1))
        
        return van
    
    def calculate_ltv(
        self,
        loan_amount: float,
        property_value: float
    ) -> float:
        """
        Calcule le Loan to Value (LTV)
        
        Args:
            loan_amount: Montant du prêt
            property_value: Valeur du bien
        
        Returns:
            LTV en pourcentage
        """
        
        if property_value == 0:
            return 0.0
        
        return loan_amount / property_value
    
    def calculate_ltc(
        self,
        loan_amount: float,
        total_cost: float
    ) -> float:
        """
        Calcule le Loan to Cost (LTC)
        
        Args:
            loan_amount: Montant du prêt
            total_cost: Coût total (achat + travaux + frais)
        
        Returns:
            LTC en pourcentage
        """
        
        if total_cost == 0:
            return 0.0
        
        return loan_amount / total_cost
    
    def calculate_dscr(
        self,
        net_operating_income: float,
        debt_service: float
    ) -> float:
        """
        Calcule le Debt Service Coverage Ratio (DSCR)
        
        Args:
            net_operating_income: Revenu net d'exploitation
            debt_service: Service de la dette (mensualités annuelles)
        
        Returns:
            DSCR (>1 = capacité à rembourser)
        """
        
        if debt_service == 0:
            return 0.0
        
        return net_operating_income / debt_service
    
    def calculate_monthly_payment(
        self,
        loan_amount: float,
        annual_rate: float,
        years: int
    ) -> float:
        """
        Calcule la mensualité d'un prêt
        
        Args:
            loan_amount: Montant du prêt
            annual_rate: Taux annuel (ex: 0.04 pour 4%)
            years: Durée en années
        
        Returns:
            Mensualité
        """
        
        monthly_rate = annual_rate / 12
        n_payments = years * 12
        
        if monthly_rate == 0:
            return loan_amount / n_payments
        
        monthly_payment = loan_amount * (
            monthly_rate * (1 + monthly_rate) ** n_payments
        ) / (
            (1 + monthly_rate) ** n_payments - 1
        )
        
        return monthly_payment
    
    def calculate_loan_schedule(
        self,
        loan_amount: float,
        annual_rate: float,
        years: int,
        amortization_type: str = "classic",
        deferred_months: int = 0,
        deferred_interest_capitalized: bool = False
    ) -> Dict[str, Any]:
        """
        Génère un tableau d'amortissement complet selon le type choisi
        
        Args:
            loan_amount: Montant du prêt
            annual_rate: Taux annuel (ex: 0.04 pour 4%)
            years: Durée en années
            amortization_type: "classic", "in_fine", "deferred"
            deferred_months: Nombre de mois de différé (pour type deferred)
            deferred_interest_capitalized: Si True, les intérêts du différé sont capitalisés
        
        Returns:
            Tableau d'amortissement détaillé mois par mois
        """
        
        monthly_rate = annual_rate / 12
        total_months = years * 12
        schedule = []
        
        if amortization_type == "classic":
            # === AMORTISSEMENT CLASSIQUE (Mensualités constantes) ===
            monthly_payment = self.calculate_monthly_payment(loan_amount, annual_rate, years)
            remaining_capital = loan_amount
            
            for month in range(1, total_months + 1):
                # Intérêts du mois
                interest = remaining_capital * monthly_rate
                
                # Capital remboursé ce mois
                principal = monthly_payment - interest
                
                # Capital restant
                remaining_capital -= principal
                
                # Éviter les arrondis négatifs en fin de prêt
                if remaining_capital < 0.01:
                    remaining_capital = 0
                
                schedule.append({
                    "month": month,
                    "payment": round(monthly_payment, 2),
                    "principal": round(principal, 2),
                    "interest": round(interest, 2),
                    "remaining_capital": round(remaining_capital, 2),
                    "cumulative_principal": round(loan_amount - remaining_capital, 2),
                    "cumulative_interest": round(sum(s["interest"] for s in schedule) + interest, 2)
                })
        
        elif amortization_type == "in_fine":
            # === IN-FINE (Capital remboursé en une fois à la fin) ===
            monthly_interest = loan_amount * monthly_rate
            
            for month in range(1, total_months + 1):
                is_last_month = (month == total_months)
                
                # Mensualité = intérêts seuls (sauf dernier mois)
                payment = monthly_interest
                principal = 0
                
                if is_last_month:
                    # Dernier mois : remboursement du capital + intérêts
                    principal = loan_amount
                    payment = monthly_interest + loan_amount
                
                remaining_capital = 0 if is_last_month else loan_amount
                
                schedule.append({
                    "month": month,
                    "payment": round(payment, 2),
                    "principal": round(principal, 2),
                    "interest": round(monthly_interest, 2),
                    "remaining_capital": round(remaining_capital, 2),
                    "cumulative_principal": round(principal, 2),
                    "cumulative_interest": round(monthly_interest * month, 2),
                    "note": "Remboursement capital" if is_last_month else "Intérêts seuls"
                })
        
        elif amortization_type == "deferred":
            # === DIFFÉRÉ D'AMORTISSEMENT (Pendant travaux) ===
            if deferred_months <= 0:
                raise ValueError("Le différé doit être > 0 mois pour type 'deferred'")
            
            if deferred_months >= total_months:
                raise ValueError("Le différé ne peut pas être >= à la durée totale")
            
            # Phase 1 : Différé (intérêts seuls ou capitalisés)
            deferred_interest_total = 0
            adjusted_loan_amount = loan_amount
            
            for month in range(1, deferred_months + 1):
                monthly_interest = adjusted_loan_amount * monthly_rate
                
                if deferred_interest_capitalized:
                    # Intérêts capitalisés : ajoutés au capital
                    adjusted_loan_amount += monthly_interest
                    payment = 0
                    note = "Différé - Intérêts capitalisés"
                else:
                    # Intérêts payés chaque mois
                    payment = monthly_interest
                    note = "Différé - Intérêts payés"
                
                deferred_interest_total += monthly_interest
                
                schedule.append({
                    "month": month,
                    "payment": round(payment, 2),
                    "principal": 0,
                    "interest": round(monthly_interest, 2),
                    "remaining_capital": round(adjusted_loan_amount, 2),
                    "cumulative_principal": 0,
                    "cumulative_interest": round(deferred_interest_total, 2),
                    "note": note,
                    "phase": "DEFERRED"
                })
            
            # Phase 2 : Amortissement normal sur le reste de la durée
            remaining_months = total_months - deferred_months
            monthly_payment = self.calculate_monthly_payment(
                adjusted_loan_amount,
                annual_rate,
                remaining_months / 12
            )
            
            remaining_capital = adjusted_loan_amount
            
            for month in range(deferred_months + 1, total_months + 1):
                interest = remaining_capital * monthly_rate
                principal = monthly_payment - interest
                remaining_capital -= principal
                
                if remaining_capital < 0.01:
                    remaining_capital = 0
                
                schedule.append({
                    "month": month,
                    "payment": round(monthly_payment, 2),
                    "principal": round(principal, 2),
                    "interest": round(interest, 2),
                    "remaining_capital": round(remaining_capital, 2),
                    "cumulative_principal": round(adjusted_loan_amount - remaining_capital, 2),
                    "cumulative_interest": round(deferred_interest_total + sum(
                        s["interest"] for s in schedule if s["month"] > deferred_months
                    ) + interest, 2),
                    "phase": "AMORTIZATION"
                })
        
        else:
            raise ValueError(f"Type d'amortissement invalide: {amortization_type}")
        
        # Calculs de synthèse
        total_paid = sum(s["payment"] for s in schedule)
        total_interest = sum(s["interest"] for s in schedule)
        total_principal = sum(s["principal"] for s in schedule)
        
        return {
            "loan_amount": loan_amount,
            "annual_rate": annual_rate,
            "annual_rate_pct": f"{annual_rate * 100:.2f}%",
            "duration_years": years,
            "duration_months": total_months,
            "amortization_type": amortization_type,
            "deferred_months": deferred_months if amortization_type == "deferred" else 0,
            "deferred_interest_capitalized": deferred_interest_capitalized if amortization_type == "deferred" else False,
            "summary": {
                "total_paid": round(total_paid, 2),
                "total_principal": round(total_principal, 2),
                "total_interest": round(total_interest, 2),
                "cost_of_credit": round(total_interest, 2),
                "cost_of_credit_pct": f"{(total_interest / loan_amount) * 100:.2f}%"
            },
            "schedule": schedule
        }
    
    def compare_amortization_types(
        self,
        loan_amount: float,
        annual_rate: float,
        years: int,
        deferred_months: int = 12
    ) -> Dict[str, Any]:
        """
        Compare les différents types d'amortissement pour aide à la décision
        
        Returns:
            Comparaison des coûts et cash-flows selon chaque type
        """
        
        results = {}
        
        # Classic
        classic = self.calculate_loan_schedule(
            loan_amount, annual_rate, years, "classic"
        )
        results["classic"] = {
            "type": "Amortissement Classique",
            "monthly_payment": classic["schedule"][0]["payment"],
            "total_cost": classic["summary"]["total_paid"],
            "total_interest": classic["summary"]["total_interest"]
        }
        
        # In-Fine
        in_fine = self.calculate_loan_schedule(
            loan_amount, annual_rate, years, "in_fine"
        )
        results["in_fine"] = {
            "type": "In-Fine",
            "monthly_payment_during": in_fine["schedule"][0]["payment"],
            "final_payment": in_fine["schedule"][-1]["payment"],
            "total_cost": in_fine["summary"]["total_paid"],
            "total_interest": in_fine["summary"]["total_interest"]
        }
        
        # Deferred (intérêts capitalisés)
        deferred_cap = self.calculate_loan_schedule(
            loan_amount, annual_rate, years, "deferred",
            deferred_months=deferred_months,
            deferred_interest_capitalized=True
        )
        results["deferred_capitalized"] = {
            "type": f"Différé {deferred_months} mois (intérêts capitalisés)",
            "monthly_payment_deferred": 0,
            "monthly_payment_after": deferred_cap["schedule"][deferred_months]["payment"],
            "total_cost": deferred_cap["summary"]["total_paid"],
            "total_interest": deferred_cap["summary"]["total_interest"]
        }
        
        # Deferred (intérêts payés)
        deferred_paid = self.calculate_loan_schedule(
            loan_amount, annual_rate, years, "deferred",
            deferred_months=deferred_months,
            deferred_interest_capitalized=False
        )
        results["deferred_paid"] = {
            "type": f"Différé {deferred_months} mois (intérêts payés)",
            "monthly_payment_deferred": deferred_paid["schedule"][0]["payment"],
            "monthly_payment_after": deferred_paid["schedule"][deferred_months]["payment"],
            "total_cost": deferred_paid["summary"]["total_paid"],
            "total_interest": deferred_paid["summary"]["total_interest"]
        }
        
        # Recommandation
        cheapest = min(results.items(), key=lambda x: x[1]["total_cost"])
        
        return {
            "loan_amount": loan_amount,
            "annual_rate": annual_rate,
            "duration_years": years,
            "comparison": results,
            "recommendation": {
                "cheapest_option": cheapest[0],
                "cheapest_type": cheapest[1]["type"],
                "total_cost": cheapest[1]["total_cost"],
                "savings_vs_most_expensive": max(r["total_cost"] for r in results.values()) - cheapest[1]["total_cost"]
            }
        }
    
    def calculate_roi(
        self,
        gain: float,
        initial_investment: float
    ) -> float:
        """
        Calcule le Return on Investment (ROI)
        
        Args:
            gain: Gain net
            initial_investment: Investissement initial
        
        Returns:
            ROI en pourcentage
        """
        
        if initial_investment == 0:
            return 0.0
        
        return gain / initial_investment
    
    def calculate_full_analysis(
        self,
        purchase_price: float,
        renovation_budget: float,
        notary_fees: float,
        loan_amount: float,
        interest_rate: float,
        loan_duration: int,
        monthly_rent: float = 0,
        resale_price: float = 0,
        project_type: str = "rental"
    ) -> Dict[str, Any]:
        """
        Calcule une analyse financière complète
        
        Returns:
            Dictionnaire avec tous les indicateurs
        """
        
        # Coûts totaux
        total_cost = purchase_price + renovation_budget + notary_fees
        equity = total_cost - loan_amount
        
        # Mensualité
        monthly_payment = self.calculate_monthly_payment(
            loan_amount,
            interest_rate,
            loan_duration
        )
        
        annual_debt_service = monthly_payment * 12
        
        # Revenus annuels (locatif)
        annual_rent = monthly_rent * 12 if project_type == "rental" else 0
        
        # Cash-flows (simplifié)
        if project_type == "rental":
            # Locatif: loyers - remboursement
            annual_cash_flow = annual_rent - annual_debt_service
            cash_flows = [annual_cash_flow] * loan_duration
            # Ajout de la revente à la fin
            if resale_price > 0:
                cash_flows[-1] += resale_price - loan_amount
        else:
            # Revente: gain à la revente
            cash_flows = [resale_price - total_cost]
        
        # Calculs
        tri = self.calculate_tri(equity, cash_flows, loan_duration)
        van = self.calculate_van(equity, cash_flows)
        ltv = self.calculate_ltv(loan_amount, purchase_price)
        ltc = self.calculate_ltc(loan_amount, total_cost)
        dscr = self.calculate_dscr(annual_rent, annual_debt_service) if annual_rent > 0 else 0
        
        # ROI
        if project_type == "rental":
            total_gain = sum(cash_flows)
        else:
            total_gain = resale_price - total_cost
        
        roi = self.calculate_roi(total_gain, equity)
        
        return {
            "total_cost": total_cost,
            "equity": equity,
            "loan_amount": loan_amount,
            "monthly_payment": monthly_payment,
            "annual_debt_service": annual_debt_service,
            "annual_rent": annual_rent,
            "tri": tri,
            "van": van,
            "ltv": ltv,
            "ltc": ltc,
            "dscr": dscr,
            "roi": roi,
            "cash_flows": cash_flows,
            "purchase_price": purchase_price,
            "renovation_budget": renovation_budget,
            "notary_fees": notary_fees,
            "interest_rate": interest_rate,
            "loan_duration": loan_duration,
        }
    
    def calculate_technical_score(
        self,
        has_construction_permit: bool = True,
        has_environmental_studies: bool = True,
        has_soil_study: bool = True,
        has_abf_clearance: bool = True,
        has_urban_planning_certificate: bool = True,
        structural_issues: bool = False,
        pollution_detected: bool = False,
        protected_area: bool = False
    ) -> Dict[str, Any]:
        """
        Calcule le score technique sur 100 avec pénalités automatiques
        
        Args:
            has_construction_permit: Permis de construire obtenu
            has_environmental_studies: Études environnementales faites
            has_soil_study: Étude de sol réalisée
            has_abf_clearance: Accord ABF (Architecte Bâtiments de France)
            has_urban_planning_certificate: Certificat d'urbanisme obtenu
            structural_issues: Problèmes structurels détectés
            pollution_detected: Pollution détectée
            protected_area: Zone protégée
        
        Returns:
            {"score": int, "grade": str, "penalties": list}
        """
        score = 100
        penalties = []
        
        # Pénalités pour documents manquants
        if not has_construction_permit:
            penalties.append({"reason": "Permis de construire manquant", "points": 20})
            score -= 20
        
        if not has_environmental_studies:
            penalties.append({"reason": "Études environnementales manquantes", "points": 15})
            score -= 15
        
        if not has_soil_study:
            penalties.append({"reason": "Étude de sol manquante", "points": 10})
            score -= 10
        
        if not has_abf_clearance:
            penalties.append({"reason": "Accord ABF manquant", "points": 15})
            score -= 15
        
        if not has_urban_planning_certificate:
            penalties.append({"reason": "Certificat d'urbanisme manquant", "points": 10})
            score -= 10
        
        # Pénalités pour risques
        if structural_issues:
            penalties.append({"reason": "Problèmes structurels", "points": 25})
            score -= 25
        
        if pollution_detected:
            penalties.append({"reason": "Pollution détectée", "points": 30})
            score -= 30
        
        if protected_area:
            penalties.append({"reason": "Zone protégée", "points": 20})
            score -= 20
        
        # Score minimum = 0
        score = max(0, score)
        
        # Attribution du grade
        if score >= 90:
            grade = "A"
        elif score >= 75:
            grade = "B"
        elif score >= 60:
            grade = "C"
        elif score >= 50:
            grade = "D"
        elif score >= 40:
            grade = "E"
        else:
            grade = "F"
        
        return {
            "score": score,
            "grade": grade,
            "penalties": penalties,
            "max_score": 100
        }
    
    def calculate_notary_fees(
        self,
        purchase_price: float,
        property_type: str = "ANCIEN",
        buyer_profile: str = "INVESTISSEUR"
    ) -> Dict[str, Any]:
        """
        Calcule les frais de notaire selon le type de bien et le profil acheteur
        
        Args:
            purchase_price: Prix d'achat
            property_type: "NEUF" ou "ANCIEN"
            buyer_profile: "PRIMO_ACCEDANT", "INVESTISSEUR", "MDB"
        
        Returns:
            {"notary_fees": float, "tax_rate": float, "buyer_profile": str}
        """
        property_type_upper = property_type.upper()
        buyer_profile_upper = buyer_profile.upper()
        
        # Déterminer le taux de droits de mutation (taxes)
        if buyer_profile_upper == "MDB":
            # MDB : régime réduit ~3%
            tax_rate = 0.025
            notary_rate = 0.005  # Émoluments notaire
        elif property_type_upper == "NEUF":
            # Neuf : droits réduits ~2-3%
            tax_rate = 0.020
            notary_rate = 0.005
        else:
            # Ancien : droits pleins ~7-8%
            tax_rate = 0.060
            notary_rate = 0.015
        
        notary_fees = purchase_price * (tax_rate + notary_rate)
        
        return {
            "notary_fees": round(notary_fees, 2),
            "tax_rate": tax_rate,
            "buyer_profile": buyer_profile_upper,
            "property_type": property_type_upper,
            "purchase_price": purchase_price
        }
    
    def check_mdb_tax_risk(
        self,
        project_duration_years: float,
        buyer_profile: str
    ) -> Dict[str, Any]:
        """
        Vérifie le risque fiscal pour marchand de biens
        
        Args:
            project_duration_years: Durée du projet en années
            buyer_profile: Profil acheteur ("MDB", "INVESTISSEUR", etc.)
        
        Returns:
            {"has_risk": bool, "warning": str (optionnel)}
        """
        is_mdb = buyer_profile.upper() == "MDB"
        
        if not is_mdb:
            return {
                "has_risk": False
            }
        
        # Risque si détention > 5 ans pour MDB
        if project_duration_years > 5:
            return {
                "has_risk": True,
                "warning": f"Risque fiscal MDB: durée {project_duration_years} ans dépasse le seuil de 5 ans",
                "duration_years": project_duration_years,
                "threshold_years": 5
            }
        
        return {
            "has_risk": False,
            "duration_years": project_duration_years,
            "threshold_years": 5
        }
    
    def calculate_debt_from_ltv(
        self,
        asset_value: float,
        ltv: float
    ) -> Dict[str, Any]:
        """
        Calcule le montant de la dette depuis LTV
        
        Args:
            asset_value: Valeur de l'actif
            ltv: Ratio LTV (ex: 0.75 pour 75%)
        
        Returns:
            {"debt_amount": float, "equity": float, "ltv": float}
        """
        if ltv > 1.0:
            raise ValueError("LTV ne peut pas dépasser 100%")
        
        debt_amount = asset_value * ltv
        equity = asset_value - debt_amount
        
        return {
            "debt_amount": round(debt_amount, 2),
            "equity": round(equity, 2),
            "ltv": ltv,
            "asset_value": asset_value
        }
    
    def calculate_debt_from_ltc(
        self,
        total_cost: float,
        ltc: float
    ) -> Dict[str, Any]:
        """
        Calcule le montant de la dette depuis LTC
        
        Args:
            total_cost: Coût total (achat + travaux + frais)
            ltc: Ratio LTC (ex: 0.70 pour 70%)
        
        Returns:
            {"debt_amount": float, "equity": float, "ltc": float}
        """
        debt_amount = total_cost * ltc
        equity = total_cost - debt_amount
        
        return {
            "debt_amount": round(debt_amount, 2),
            "equity": round(equity, 2),
            "ltc": ltc,
            "total_cost": total_cost
        }
    
    def generate_project_timeline(
        self,
        project_start: datetime = None,
        permit_duration_months: int = None,
        construction_duration_months: int = None,
        commercialization_duration_months: int = None,
        # Anciens paramètres pour compatibilité
        acquisition_months: int = None,
        construction_months: int = None,
        commercialization_months: int = None
    ) -> Dict[str, Any]:
        """
        Génère le phasage temporel du projet (3 phases obligatoires)
        
        Supporte deux signatures:
        1. Nouvelle: project_start + permit_duration_months + construction_duration_months + commercialization_duration_months
        2. Ancienne: acquisition_months + construction_months + commercialization_months
        
        Returns:
            Timeline structurée avec les 3 phases
        """
        from datetime import timedelta
        from dateutil.relativedelta import relativedelta
        
        # Si ancienne signature (sans dates)
        if project_start is None and acquisition_months is not None:
            phases = []
            current_month = 0
            
            # Phase 1: Acquisition
            phases.append({
                "name": "Acquisition",
                "start_month": current_month,
                "end_month": current_month + acquisition_months,
                "duration_months": acquisition_months
            })
            current_month += acquisition_months
            
            # Phase 2: Construction (Travaux)
            phases.append({
                "name": "Construction",
                "start_month": current_month,
                "end_month": current_month + construction_months,
                "duration_months": construction_months
            })
            current_month += construction_months
            
            # Phase 3: Commercialisation
            phases.append({
                "name": "Commercialization",
                "start_month": current_month,
                "end_month": current_month + commercialization_months,
                "duration_months": commercialization_months
            })
            
            return {
                "phases": phases,
                "total_duration_months": current_month + commercialization_months
            }
        
        # Nouvelle signature avec dates
        if project_start is None:
            project_start = datetime.now()
        
        phases = []
        current_date = project_start
        
        # Phase 1: Études et Permis
        phase1_end = current_date + relativedelta(months=permit_duration_months)
        phases.append({
            "name": "ÉTUDES_PERMIS",
            "start_date": current_date,
            "end_date": phase1_end,
            "duration_months": permit_duration_months,
            "description": "Études, permis de construire, autorisations"
        })
        current_date = phase1_end
        
        # Phase 2: Travaux (Construction)
        phase2_end = current_date + relativedelta(months=construction_duration_months)
        phases.append({
            "name": "TRAVAUX",
            "start_date": current_date,
            "end_date": phase2_end,
            "duration_months": construction_duration_months,
            "description": "Phase de construction/rénovation"
        })
        current_date = phase2_end
        
        # Phase 3: Commercialisation
        phase3_end = current_date + relativedelta(months=commercialization_duration_months)
        phases.append({
            "name": "COMMERCIALISATION",
            "start_date": current_date,
            "end_date": phase3_end,
            "duration_months": commercialization_duration_months,
            "description": "Vente/location/mise en exploitation"
        })
        
        total_duration = permit_duration_months + construction_duration_months + commercialization_duration_months
        
        return {
            "project_start": project_start,
            "project_end": phase3_end,
            "total_duration_months": total_duration,
            "phases": phases
        }
    
    def generate_cashflows(
        self,
        timeline: Dict[str, Any],
        capex_total: float,
        monthly_rent: float = 0,
        capex_distribution: str = "LINEAR"
    ) -> List[Dict[str, Any]]:
        """
        Génère les cashflows mensuels alignés sur la timeline
        CAPEX uniquement pendant TRAVAUX
        Revenus uniquement pendant COMMERCIALISATION
        
        Args:
            timeline: Timeline du projet avec phases
            capex_total: Budget CAPEX total
            monthly_rent: Loyer mensuel (ou 0 si vente)
            capex_distribution: "LINEAR" ou autre
        
        Returns:
            Liste de cashflows mois par mois avec phase
        """
        from dateutil.relativedelta import relativedelta
        
        phases = timeline["phases"]
        cashflows = []
        
        # Parcourir chaque phase et générer les mois
        for phase in phases:
            phase_name = phase["name"]
            start_date = phase["start_date"]
            end_date = phase["end_date"]
            duration_months = phase["duration_months"]
            
            # Calculer CAPEX mensuel si phase = TRAVAUX
            if phase_name == "TRAVAUX":
                if capex_distribution == "LINEAR":
                    capex_per_month = capex_total / duration_months if duration_months > 0 else 0
                else:
                    capex_per_month = capex_total / duration_months if duration_months > 0 else 0
            else:
                capex_per_month = 0
            
            # Calculer revenus mensuels si phase = COMMERCIALISATION
            if phase_name == "COMMERCIALISATION":
                revenue_per_month = monthly_rent
            else:
                revenue_per_month = 0
            
            # Générer un cashflow par mois dans cette phase
            current_date = start_date
            for month_idx in range(duration_months):
                cashflows.append({
                    "date": current_date,
                    "month": len(cashflows),
                    "phase": phase_name,
                    "capex": capex_per_month,
                    "revenue": revenue_per_month,
                    "net_cashflow": revenue_per_month - capex_per_month
                })
                current_date += relativedelta(months=1)
        
        return cashflows

    
    def calculate_waterfall(
        self,
        proceeds: float = None,
        invested_capital: float = None,
        hurdle_rate: float = None,
        promote_rate: float = None,
        # Nouvelle signature pour tests
        total_proceeds: float = None,
        initial_investment: float = None,
        promote_percentage: float = None,
        investment_duration_years: float = None
    ) -> Dict[str, Any]:
        """
        Calcule la distribution waterfall Private Equity
        
        Supporte deux signatures:
        1. Ancienne: proceeds, invested_capital, hurdle_rate, promote_rate
        2. Nouvelle: total_proceeds, initial_investment, hurdle_rate, promote_percentage, investment_duration_years
        
        Returns:
            Distribution investisseur/sponsor avec IRR
        """
        # Normaliser les paramètres
        if total_proceeds is not None:
            proceeds = total_proceeds
        if initial_investment is not None:
            invested_capital = initial_investment
        if promote_percentage is not None:
            promote_rate = promote_percentage
        
        # Calcul IRR si durée fournie
        irr = None
        if investment_duration_years and proceeds and invested_capital:
            # IRR simple = (proceeds / invested_capital) ^ (1/years) - 1
            if proceeds > 0 and invested_capital > 0:
                irr = (proceeds / invested_capital) ** (1 / investment_duration_years) - 1
            else:
                irr = -1.0
        
        # Étape 1: Retour du capital investi
        remaining = proceeds
        investor_capital_return = min(remaining, invested_capital)
        remaining -= investor_capital_return
        
        # Gestion cas de perte
        if remaining <= 0:
            result = {
                "investor_distribution": investor_capital_return,
                "sponsor_distribution": 0,
                "sponsor_promote": 0,
                "investor_pct": 100.0,
                "sponsor_pct": 0.0,
                "hurdle_reached": False
            }
            if irr is not None:
                result["irr"] = round(irr, 4)
            return result
        
        # Étape 2: Hurdle à l'investisseur (si hurdle_rate > 0)
        investor_hurdle = 0
        if hurdle_rate and hurdle_rate > 0 and investment_duration_years:
            # Hurdle composé = capital * (1 + hurdle)^years - capital
            target_amount = invested_capital * ((1 + hurdle_rate) ** investment_duration_years)
            hurdle_amount = target_amount - invested_capital
            investor_hurdle = min(remaining, hurdle_amount)
            remaining -= investor_hurdle
            
            total_investor = investor_capital_return + investor_hurdle
            
            if remaining <= 0:
                result = {
                    "investor_distribution": total_investor,
                    "sponsor_distribution": 0,
                    "sponsor_promote": 0,
                    "investor_pct": 100.0,
                    "sponsor_pct": 0.0,
                    "hurdle_reached": True,
                    "hurdle_met": False
                }
                if irr is not None:
                    result["irr"] = round(irr, 4)
                return result
        elif hurdle_rate and hurdle_rate > 0:
            # Si pas de durée, hurdle simple
            hurdle_amount = invested_capital * hurdle_rate
            investor_hurdle = min(remaining, hurdle_amount)
            remaining -= investor_hurdle
            
            total_investor = investor_capital_return + investor_hurdle
            
            if remaining <= 0:
                result = {
                    "investor_distribution": total_investor,
                    "sponsor_distribution": 0,
                    "sponsor_promote": 0,
                    "investor_pct": 100.0,
                    "sponsor_pct": 0.0,
                    "hurdle_reached": True,
                    "hurdle_met": False
                }
                if irr is not None:
                    result["irr"] = round(irr, 4)
                return result
        else:
            total_investor = investor_capital_return
        
        # Étape 3: Split du surplus avec promote
        sponsor_promote = remaining * promote_rate
        investor_surplus = remaining * (1 - promote_rate)
        
        total_investor += investor_surplus
        total_sponsor = sponsor_promote
        
        investor_pct = (total_investor / proceeds) * 100
        sponsor_pct = (total_sponsor / proceeds) * 100
        
        # Métriques PE
        multiple_on_invested_capital = proceeds / invested_capital if invested_capital > 0 else 0
        effective_promote_rate = total_sponsor / (proceeds - invested_capital) if proceeds > invested_capital else 0
        
        result = {
            "investor_distribution": round(total_investor, 2),
            "sponsor_distribution": round(total_sponsor, 2),
            "sponsor_promote": round(sponsor_promote, 2),
            "investor_pct": round(investor_pct, 2),
            "sponsor_pct": round(sponsor_pct, 2),
            "hurdle_reached": True,
            "hurdle_met": True,
            "capital_returned": investor_capital_return,
            "hurdle_payment": investor_hurdle,
            "surplus_investor": investor_surplus,
            "surplus_sponsor": sponsor_promote,
            "multiple_on_invested_capital": round(multiple_on_invested_capital, 2),
            "effective_promote_rate": round(effective_promote_rate, 4)
        }
        
        if irr is not None:
            result["irr"] = round(irr, 4)
        
        return result
    
    def calculate_waterfall_multi_tier(
        self,
        proceeds: float = None,
        invested_capital: float = None,
        hurdle_tiers: List[Dict[str, float]] = None,
        investment_duration_years: float = None,
        # Alias
        total_proceeds: float = None,
        initial_investment: float = None
    ) -> Dict[str, Any]:
        """
        Waterfall avec plusieurs paliers de promote
        
        Args:
            hurdle_tiers: Liste de {"threshold_irr": float, "promote": float}
            
        Returns:
            Distribution avec promote multi-paliers
        """
        # Normaliser
        if total_proceeds is not None:
            proceeds = total_proceeds
        if initial_investment is not None:
            invested_capital = initial_investment
        
        # Calcul IRR
        irr = None
        if investment_duration_years and proceeds and invested_capital:
            if proceeds > 0 and invested_capital > 0:
                irr = (proceeds / invested_capital) ** (1 / investment_duration_years) - 1
            else:
                irr = -1.0
        
        # Retour capital
        remaining = proceeds
        investor_capital_return = min(remaining, invested_capital)
        remaining -= investor_capital_return
        
        if remaining <= 0:
            return {
                "investor_distribution": investor_capital_return,
                "sponsor_distribution": 0,
                "sponsor_promote": 0,
                "irr": round(irr, 4) if irr is not None else None
            }
        
        # Déterminer le promote basé sur l'IRR atteint
        promote_rate = 0
        if irr is not None and hurdle_tiers:
            for tier in sorted(hurdle_tiers, key=lambda x: x["threshold_irr"], reverse=True):
                if irr >= tier["threshold_irr"]:
                    promote_rate = tier["promote"]
                    break
        
        # Split du surplus
        sponsor_promote = remaining * promote_rate
        investor_surplus = remaining * (1 - promote_rate)
        
        total_investor = investor_capital_return + investor_surplus
        total_sponsor = sponsor_promote
        
        # Métriques
        effective_promote_rate = total_sponsor / (proceeds - invested_capital) if proceeds > invested_capital else 0
        
        return {
            "investor_distribution": round(total_investor, 2),
            "sponsor_distribution": round(total_sponsor, 2),
            "sponsor_promote": round(sponsor_promote, 2),
            "irr": round(irr, 4) if irr is not None else None,
            "promote_tier_used": promote_rate,
            "effective_promote_rate": round(effective_promote_rate, 4)
        }

# Instance globale
financial_service = FinancialService()
