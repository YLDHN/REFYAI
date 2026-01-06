from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.services.asset_management_service import asset_management_service

router = APIRouter(prefix="/asset-management", tags=["asset-management"])


class RentScheduleRequest(BaseModel):
    """Requête de calcul de planning locatif"""
    annual_rent: float = Field(gt=0, description="Loyer annuel de base")
    lease_start_date: datetime = Field(description="Date de début du bail")
    lease_duration_years: int = Field(ge=1, le=30, description="Durée du bail en années")
    rent_free_months: int = Field(default=0, ge=0, description="Mois de franchise")
    tenant_improvements: float = Field(default=0, ge=0, description="Montant travaux preneur")
    indexation_type: str = Field(default="ILAT", description="ICC, ILAT, ILC, FIXED")
    indexation_rate: Optional[float] = Field(default=None, ge=0, le=0.10, description="Taux custom")
    indexation_start_year: int = Field(default=2, ge=1, description="Année début indexation")


class IndexationProjectionRequest(BaseModel):
    """Requête de projection d'indexation"""
    initial_rent: float = Field(gt=0, description="Loyer initial")
    years: int = Field(ge=1, le=30, description="Années de projection")
    indexation_type: str = Field(default="ILAT")
    custom_rate: Optional[float] = Field(default=None, ge=0, le=0.10)
    scenarios: List[str] = Field(default=["pessimistic", "base", "optimistic"])


class RentFreeValueRequest(BaseModel):
    """Requête de valorisation franchise"""
    monthly_rent: float = Field(gt=0)
    rent_free_months: int = Field(ge=1, le=24)
    discount_rate: float = Field(default=0.05, ge=0, le=0.20)


class TenantImprovementsRequest(BaseModel):
    """Requête d'optimisation tenant improvements"""
    monthly_rent: float = Field(gt=0)
    lease_duration_years: int = Field(ge=1, le=30)
    options: List[Dict[str, float]] = Field(
        description="Liste d'options [{cost: X, rent_increase: Y}, ...]"
    )


@router.post("/rent-schedule")
async def calculate_rent_schedule(data: RentScheduleRequest):
    """
    Calculer le planning de loyers avec franchise et indexation
    
    Prend en compte :
    - **Rent Free** : Mois sans loyer en début de bail
    - **Tenant Improvements** : Travaux payés par le bailleur
    - **Indexation** : Augmentation annuelle (ICC, ILAT, ILC)
    
    Retourne :
    - Planning mensuel complet
    - Impact financier sur le rendement
    - Mois de break-even
    
    Exemple de cas d'usage :
    - Bureau avec 3 mois de franchise + 30k€ de travaux
    - Indexation ILAT 2% par an à partir année 2
    """
    try:
        result = asset_management_service.calculate_rent_schedule_with_rent_free(
            annual_rent=data.annual_rent,
            lease_start_date=data.lease_start_date,
            lease_duration_years=data.lease_duration_years,
            rent_free_months=data.rent_free_months,
            tenant_improvements=data.tenant_improvements,
            indexation_type=data.indexation_type,
            indexation_rate=data.indexation_rate,
            indexation_start_year=data.indexation_start_year
        )
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du calcul: {str(e)}"
        )


@router.post("/indexation/projection")
async def project_rent_indexation(data: IndexationProjectionRequest):
    """
    Projeter l'évolution du loyer selon différents scénarios
    
    Génère 3 scénarios :
    - **Pessimiste** : 50% du taux historique
    - **Base** : Taux historique moyen
    - **Optimiste** : 150% du taux historique
    
    Indices disponibles :
    - **ICC** : Indice du Coût de la Construction (~2.5% historique)
    - **ILAT** : Indice Loyers Activités Tertiaires (~2.0%)
    - **ILC** : Indice Loyers Commerciaux (~2.2%)
    - **FIXED** : Taux fixe personnalisé
    
    Utile pour :
    - Modélisation financière long terme
    - Étude de sensibilité
    - Négociation des termes du bail
    """
    try:
        result = asset_management_service.calculate_indexation_projection(
            initial_rent=data.initial_rent,
            years=data.years,
            indexation_type=data.indexation_type,
            custom_rate=data.custom_rate,
            scenarios=data.scenarios
        )
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la projection: {str(e)}"
        )


@router.post("/rent-free/value")
async def calculate_rent_free_value(data: RentFreeValueRequest):
    """
    Calculer la valeur actualisée d'une franchise de loyer
    
    Compare :
    - Valeur nominale (montant total non perçu)
    - Valeur actuelle (actualisée avec discount rate)
    
    Utile pour :
    - Négociation avec le locataire
    - Décision make/buy pour le bailleur
    - Arbitrage franchise vs réduction de loyer
    
    Exemple :
    - 6 mois de franchise à 5000€/mois = 30k€ nominal
    - Mais seulement 28.5k€ en valeur actuelle (discount 5%)
    """
    try:
        result = asset_management_service.calculate_rent_free_value(
            monthly_rent=data.monthly_rent,
            rent_free_months=data.rent_free_months,
            discount_rate=data.discount_rate
        )
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du calcul: {str(e)}"
        )


@router.post("/tenant-improvements/optimize")
async def optimize_tenant_improvements(data: TenantImprovementsRequest):
    """
    Analyser la rentabilité des tenant improvements
    
    Compare différentes options d'investissement dans les travaux locataire :
    - Coût de l'investissement
    - Augmentation de loyer obtenue
    - ROI et payback period
    
    Exemple d'options :
    ```json
    {
      "options": [
        {"cost": 30000, "rent_increase": 300},
        {"cost": 50000, "rent_increase": 450},
        {"cost": 80000, "rent_increase": 600}
      ]
    }
    ```
    
    Identifie automatiquement l'option la plus rentable.
    """
    try:
        result = asset_management_service.optimize_tenant_improvements(
            monthly_rent=data.monthly_rent,
            tenant_improvements_options=data.options,
            lease_duration_years=data.lease_duration_years
        )
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse: {str(e)}"
        )


@router.get("/indexation/indices")
async def get_indexation_indices():
    """
    Récupérer les informations sur les indices disponibles
    
    Taux historiques moyens et cas d'usage recommandés
    """
    return {
        "indices": {
            "ICC": {
                "name": "Indice du Coût de la Construction",
                "historical_rate": 0.025,
                "historical_rate_pct": "2.5%",
                "use_case": "Baux d'habitation, logements sociaux",
                "publication": "INSEE - Trimestriel",
                "volatility": "Moyenne"
            },
            "ILAT": {
                "name": "Indice des Loyers des Activités Tertiaires",
                "historical_rate": 0.020,
                "historical_rate_pct": "2.0%",
                "use_case": "Bureaux, activités tertiaires",
                "publication": "INSEE - Trimestriel",
                "volatility": "Faible",
                "recommended": True
            },
            "ILC": {
                "name": "Indice des Loyers Commerciaux",
                "historical_rate": 0.022,
                "historical_rate_pct": "2.2%",
                "use_case": "Commerces, retail",
                "publication": "INSEE - Trimestriel",
                "volatility": "Moyenne"
            },
            "FIXED": {
                "name": "Taux Fixe",
                "historical_rate": None,
                "use_case": "Indexation personnalisée, baux atypiques",
                "note": "Nécessite de spécifier custom_rate"
            }
        },
        "recommendations": {
            "office": "ILAT",
            "retail": "ILC",
            "residential": "ICC",
            "logistics": "ILAT",
            "mixed": "ILAT"
        },
        "notes": [
            "Les taux historiques sont des moyennes sur 10 ans",
            "Les indices sont publiés par l'INSEE chaque trimestre",
            "L'indexation s'applique généralement à partir de l'année 2",
            "Toujours vérifier les clauses contractuelles du bail"
        ]
    }
