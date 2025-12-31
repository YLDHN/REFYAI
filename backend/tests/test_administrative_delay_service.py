"""
Tests unitaires pour le service de délais administratifs
"""
import pytest
from datetime import datetime, timedelta
from app.services.administrative_delay_service import (
    AdministrativeDelayService,
    ComplexityLevel,
    ProcedureType
)


@pytest.fixture
def delay_service():
    return AdministrativeDelayService()


def test_get_procedure_delay_paris_pc(delay_service):
    """Test délai PC à Paris"""
    result = delay_service.get_procedure_delay(
        "Paris",
        ProcedureType.PC,
        ComplexityLevel.SIMPLE,
        has_abf=False
    )
    
    assert "error" not in result
    assert result["city"] == "Paris"
    assert result["procedure"] == ProcedureType.PC
    assert result["has_abf"] is False
    assert "delays_days" in result
    assert "delays_months" in result
    assert result["delays_days"]["avg"] > 0


def test_get_procedure_delay_with_abf(delay_service):
    """Test délai avec ABF"""
    # Sans ABF
    result_no_abf = delay_service.get_procedure_delay(
        "Paris",
        ProcedureType.PC,
        ComplexityLevel.SIMPLE,
        has_abf=False
    )
    
    # Avec ABF
    result_with_abf = delay_service.get_procedure_delay(
        "Paris",
        ProcedureType.PC,
        ComplexityLevel.SIMPLE,
        has_abf=True
    )
    
    # ABF doit augmenter le délai
    assert result_with_abf["delays_days"]["avg"] > result_no_abf["delays_days"]["avg"]
    assert result_with_abf["abf_additional_days"] > 0


def test_get_procedure_delay_complexity(delay_service):
    """Test impact complexité sur délai"""
    # Simple
    result_simple = delay_service.get_procedure_delay(
        "Paris",
        ProcedureType.PC,
        ComplexityLevel.SIMPLE,
        has_abf=False
    )
    
    # Très complexe
    result_complex = delay_service.get_procedure_delay(
        "Paris",
        ProcedureType.PC,
        ComplexityLevel.VERY_COMPLEX,
        has_abf=False
    )
    
    # Complexité doit augmenter le délai
    assert result_complex["delays_days"]["avg"] > result_simple["delays_days"]["avg"]
    assert result_complex["complexity_factor"] > result_simple["complexity_factor"]


def test_get_procedure_delay_default_city(delay_service):
    """Test délai pour ville sans données spécifiques"""
    result = delay_service.get_procedure_delay(
        "VilleInconnue",
        ProcedureType.PC,
        ComplexityLevel.SIMPLE,
        has_abf=False
    )
    
    assert "error" not in result
    assert result["delays_days"]["avg"] > 0


def test_get_procedure_delay_dp(delay_service):
    """Test délai Déclaration Préalable"""
    result = delay_service.get_procedure_delay(
        "Paris",
        ProcedureType.DP,
        ComplexityLevel.SIMPLE,
        has_abf=False
    )
    
    assert result["procedure"] == ProcedureType.DP
    # DP doit être plus rapide que PC
    assert result["delays_days"]["avg"] < 60


def test_get_procedure_delay_invalid(delay_service):
    """Test procédure invalide"""
    result = delay_service.get_procedure_delay(
        "Paris",
        "procedure_invalide",
        ComplexityLevel.SIMPLE,
        has_abf=False
    )
    
    assert "error" in result
    assert "available_procedures" in result


def test_calculate_project_timeline_sequential(delay_service):
    """Test planning séquentiel"""
    procedures = [
        {"type": ProcedureType.PC, "complexity": ComplexityLevel.SIMPLE, "has_abf": False},
        {"type": ProcedureType.DAACT, "complexity": ComplexityLevel.SIMPLE, "has_abf": False}
    ]
    
    result = delay_service.calculate_project_timeline(
        "Paris",
        procedures,
        parallel_execution=False
    )
    
    assert "project_timeline" in result
    assert result["project_timeline"]["execution_mode"] == "sequential"
    assert "total_delays_days" in result["project_timeline"]
    assert "estimated_completion" in result["project_timeline"]
    assert len(result["procedures_detail"]) == 2


def test_calculate_project_timeline_parallel(delay_service):
    """Test planning parallèle"""
    procedures = [
        {"type": ProcedureType.PC, "complexity": ComplexityLevel.SIMPLE, "has_abf": False},
        {"type": ProcedureType.PD, "complexity": ComplexityLevel.SIMPLE, "has_abf": False}
    ]
    
    # Séquentiel
    result_seq = delay_service.calculate_project_timeline(
        "Paris",
        procedures,
        parallel_execution=False
    )
    
    # Parallèle
    result_par = delay_service.calculate_project_timeline(
        "Paris",
        procedures,
        parallel_execution=True
    )
    
    # Parallèle doit être plus rapide
    assert result_par["project_timeline"]["total_delays_days"]["avg"] < \
           result_seq["project_timeline"]["total_delays_days"]["avg"]


def test_calculate_project_timeline_dates(delay_service):
    """Test calcul des dates"""
    procedures = [
        {"type": ProcedureType.PC, "complexity": ComplexityLevel.SIMPLE, "has_abf": False}
    ]
    
    result = delay_service.calculate_project_timeline(
        "Paris",
        procedures,
        parallel_execution=False
    )
    
    completion = result["project_timeline"]["estimated_completion"]
    
    # Vérifier format dates
    assert "optimistic" in completion
    assert "realistic" in completion
    assert "pessimistic" in completion
    
    # Vérifier format ISO
    datetime.fromisoformat(completion["optimistic"])
    datetime.fromisoformat(completion["realistic"])
    datetime.fromisoformat(completion["pessimistic"])


def test_estimate_full_project_duration_with_pc(delay_service):
    """Test durée complète projet avec PC"""
    project_data = {
        "has_pc": True,
        "has_dp": False,
        "has_abf": True,
        "complexity": ComplexityLevel.MODERATE,
        "construction_months": 8
    }
    
    result = delay_service.estimate_full_project_duration(
        "Paris",
        project_data
    )
    
    assert "full_project_duration" in result
    assert "phases" in result["full_project_duration"]
    
    phases = result["full_project_duration"]["phases"]
    assert "studies" in phases
    assert "administrative" in phases
    assert "construction" in phases
    assert "completion" in phases
    
    # Vérifier construction = 8 mois
    assert phases["construction"]["days"] == 8 * 30


def test_estimate_full_project_duration_with_dp(delay_service):
    """Test durée complète projet avec DP"""
    project_data_pc = {
        "has_pc": True,
        "has_dp": False,
        "has_abf": False,
        "complexity": ComplexityLevel.SIMPLE,
        "construction_months": 6
    }
    
    project_data_dp = {
        "has_pc": False,
        "has_dp": True,
        "has_abf": False,
        "complexity": ComplexityLevel.SIMPLE,
        "construction_months": 6
    }
    
    result_pc = delay_service.estimate_full_project_duration("Paris", project_data_pc)
    result_dp = delay_service.estimate_full_project_duration("Paris", project_data_dp)
    
    # DP doit être plus rapide que PC en phase admin
    assert result_dp["full_project_duration"]["phases"]["administrative"]["avg_days"] < \
           result_pc["full_project_duration"]["phases"]["administrative"]["avg_days"]


def test_estimate_full_project_duration_total(delay_service):
    """Test cohérence total durée"""
    project_data = {
        "has_pc": True,
        "has_dp": False,
        "has_abf": False,
        "complexity": ComplexityLevel.SIMPLE,
        "construction_months": 6
    }
    
    result = delay_service.estimate_full_project_duration("Paris", project_data)
    
    phases = result["full_project_duration"]["phases"]
    total = result["full_project_duration"]["total_duration_days"]
    
    # Vérifier total = somme phases
    calculated_total = (
        phases["studies"]["avg_days"] +
        phases["administrative"]["avg_days"] +
        phases["construction"]["days"] +
        phases["completion"]["avg_days"]
    )
    
    assert total["avg"] == calculated_total


def test_get_available_procedures(delay_service):
    """Test liste procédures disponibles"""
    procedures = delay_service._get_available_procedures()
    
    assert isinstance(procedures, list)
    assert len(procedures) > 0
    assert ProcedureType.PC.replace("permis_construire", "permis_construire") in \
           [p.replace("_", "_") for p in procedures]


def test_get_cities_with_data(delay_service):
    """Test liste villes avec données"""
    cities = delay_service.get_cities_with_data()
    
    assert isinstance(cities, list)
    assert "Paris" in cities
    assert "Lyon" in cities
    assert "Marseille" in cities


def test_delays_conversion_days_to_months(delay_service):
    """Test conversion jours → mois"""
    result = delay_service.get_procedure_delay(
        "Paris",
        ProcedureType.PC,
        ComplexityLevel.SIMPLE,
        has_abf=False
    )
    
    # Vérifier cohérence
    days = result["delays_days"]["avg"]
    months = result["delays_months"]["avg"]
    
    assert abs((days / 30) - months) < 0.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
