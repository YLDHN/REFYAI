"""
Service de calculs financiers immobiliers
"""
from typing import Dict, Any
import numpy as np
from scipy.optimize import newton

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

# Instance globale
financial_service = FinancialService()
