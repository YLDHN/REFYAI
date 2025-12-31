from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services import financial_service
from typing import List

router = APIRouter(prefix="/financial", tags=["financial"])

class FinancialInput(BaseModel):
    purchase_price: float
    renovation_budget: float
    notary_fees: float
    loan_amount: float
    interest_rate: float
    loan_duration: int
    monthly_rent: float = 0
    resale_price: float = 0
    project_type: str = "rental"  # rental ou resale

class FinancialAnalysisResponse(BaseModel):
    total_cost: float
    equity: float
    loan_amount: float
    monthly_payment: float
    annual_debt_service: float
    annual_rent: float
    tri: float
    van: float
    ltv: float
    ltc: float
    dscr: float
    roi: float
    cash_flows: List[float]

@router.post("/analyze", response_model=FinancialAnalysisResponse)
async def calculate_financial_analysis(data: FinancialInput):
    """Calculer une analyse financière complète"""
    
    try:
        analysis = financial_service.calculate_full_analysis(
            purchase_price=data.purchase_price,
            renovation_budget=data.renovation_budget,
            notary_fees=data.notary_fees,
            loan_amount=data.loan_amount,
            interest_rate=data.interest_rate,
            loan_duration=data.loan_duration,
            monthly_rent=data.monthly_rent,
            resale_price=data.resale_price,
            project_type=data.project_type
        )
        
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du calcul: {str(e)}"
        )

@router.post("/tri")
async def calculate_tri(
    initial_investment: float,
    cash_flows: List[float]
):
    """Calculer le TRI (Taux de Rendement Interne)"""
    
    tri = financial_service.calculate_tri(
        initial_investment=initial_investment,
        cash_flows=cash_flows
    )
    
    return {"tri": tri, "tri_percentage": f"{tri * 100:.2f}%"}

@router.post("/ltv")
async def calculate_ltv(
    loan_amount: float,
    property_value: float
):
    """Calculer le LTV (Loan to Value)"""
    
    ltv = financial_service.calculate_ltv(
        loan_amount=loan_amount,
        property_value=property_value
    )
    
    return {"ltv": ltv, "ltv_percentage": f"{ltv * 100:.2f}%"}

@router.post("/dscr")
async def calculate_dscr(
    net_operating_income: float,
    debt_service: float
):
    """Calculer le DSCR (Debt Service Coverage Ratio)"""
    
    dscr = financial_service.calculate_dscr(
        net_operating_income=net_operating_income,
        debt_service=debt_service
    )
    
    return {"dscr": dscr}
