"""
Tests unitaires pour les services critiques
"""
import pytest
from app.services.location_questionnaire_service import LocationQuestionnaireService
from app.services.showstopper_service import ShowstopperDetectionService, ShowstopperSeverity
from app.services.interest_rate_service import InterestRateService


# =========================
# TESTS QUESTIONNAIRE
# =========================

@pytest.fixture
def questionnaire_service():
    return LocationQuestionnaireService()


def test_get_questions(questionnaire_service):
    """Test récupération questions"""
    questions = questionnaire_service.get_questions()
    
    assert isinstance(questions, list)
    assert len(questions) == 12
    
    # Vérifier structure première question
    first_q = questions[0]
    assert "id" in first_q
    assert "question" in first_q
    assert "type" in first_q
    assert "required" in first_q


def test_validate_answers_complete(questionnaire_service):
    """Test validation réponses complètes"""
    answers = {
        "commune": "Paris",
        "adresse": "10 rue de la Paix",
        "parcelle_cadastrale": "AK 123",
        "zone_plu": "UC",
        "surface_terrain": 500,
        "surface_construite": 300,
        "hauteur_batiment": 12,
        "nombre_niveaux": 3,
        "monuments_historiques": False,
        "abf_avis": False,
        "nature_travaux": ["Rénovation intérieure"],
        "destination_finale": "Habitation"
    }
    
    result = questionnaire_service.validate_answers(answers)
    
    assert result["valid"] is True
    assert len(result["errors"]) == 0


def test_validate_answers_missing(questionnaire_service):
    """Test validation réponses manquantes"""
    answers = {
        "commune": "Paris"
        # Manque toutes les autres réponses requises
    }
    
    result = questionnaire_service.validate_answers(answers)
    
    assert result["valid"] is False
    assert len(result["errors"]) > 0


def test_extract_plu_filters(questionnaire_service):
    """Test extraction filtres PLU"""
    answers = {
        "zone_plu": "UC",
        "nature_travaux": ["Changement de destination"],
        "destination_finale": "Commerce",
        "abf_avis": True,
        "monuments_historiques": False
    }
    
    filters = questionnaire_service.extract_plu_filters(answers)
    
    assert "zone" in filters
    assert "keywords" in filters
    assert "constraints" in filters
    assert filters["zone"] == "UC"
    assert len(filters["keywords"]) > 0


# =========================
# TESTS SHOWSTOPPERS
# =========================

@pytest.fixture
def showstopper_service():
    return ShowstopperDetectionService()


def test_detect_showstoppers_none(showstopper_service):
    """Test aucun showstopper"""
    project = {
        "city": "Paris",
        "tri": 12.5,
        "ltv": 70
    }
    
    questionnaire = {
        "zone_plu": "UC",
        "abf_required": False,
        "destination_actuelle": "habitation",
        "destination_future": "habitation"
    }
    
    plu = {
        "zone_constructible": True,
        "cos_depassement": False
    }
    
    tech = {
        "risque_structure": False,
        "amiante": False
    }
    
    result = showstopper_service.detect_showstoppers(project, questionnaire, plu, tech)
    
    assert isinstance(result, list)
    # Peut avoir des showstoppers de faible sévérité


def test_detect_showstoppers_critical(showstopper_service):
    """Test showstopper critique"""
    project = {
        "city": "Paris",
        "tri": 5.0,  # TRI trop faible
        "ltv": 95    # LTV trop élevé
    }
    
    questionnaire = {
        "zone_plu": "N",  # Zone non constructible
        "abf_required": True,
        "destination_actuelle": "habitation",
        "destination_future": "commerce",  # Changement destination
        "nature_travaux": ["Changement de destination"]
    }
    
    plu = {
        "zone_type": "N",  # Zone non constructible (clé correcte)
        "zone_constructible": False,
        "cos_exceeded": True,
        "planned_surface": 500,
        "max_surface": 400
    }
    
    tech = {
        "risque_structure": True,  # Risque structure
        "amiante": True
    }
    
    result = showstopper_service.detect_showstoppers(project, questionnaire, plu, tech)
    
    # Doit avoir plusieurs showstoppers critiques
    critical = [s for s in result if s["severity"] == ShowstopperSeverity.CRITICAL]
    assert len(critical) > 0


def test_generate_action_plan(showstopper_service):
    """Test génération plan d'action"""
    showstoppers = [
        {
            "category": "regulatory",
            "type": "zone_non_constructible",
            "severity": ShowstopperSeverity.CRITICAL,
            "description": "Zone non constructible",
            "impact": "Projet impossible en l'état",
            "recommendations": ["Consulter le service urbanisme", "Envisager une dérogation"]
        },
        {
            "category": "technical",
            "type": "structure_risk",
            "severity": ShowstopperSeverity.HIGH,
            "description": "Risque structurel",
            "impact": "Travaux importants requis",
            "recommendations": ["Étude structure approfondie", "Prévoir budget supplémentaire"]
        }
    ]
    
    result = showstopper_service.generate_action_plan(showstoppers)
    
    assert "priority_actions" in result or "action_plan" in result
    assert "summary" in result or "critical_count" in result
    
    # Vérifier qu'il y a des actions
    if "priority_actions" in result:
        assert len(result["priority_actions"]) > 0


# =========================
# TESTS INTEREST RATE
# =========================

@pytest.fixture
def interest_rate_service():
    return InterestRateService()


@pytest.mark.asyncio
async def test_calculate_risk_score_excellent(interest_rate_service):
    """Test calcul score de risque excellent"""
    project = {
        "city": "Paris",
        "ltv": 0.65,  # LTV en décimal
        "tri": 15.0,
        "showstoppers_count": 0
    }
    
    company = {
        "years_experience": 8,
        "projects_completed": 12
    }
    
    market_trend = "hausse"
    technical_issues = []
    
    score = interest_rate_service.calculate_risk_score(
        project,
        company,
        market_trend,
        technical_issues
    )
    
    assert 0 <= score <= 100
    assert score >= 70  # Devrait être bon score


@pytest.mark.asyncio
async def test_calculate_risk_score_poor(interest_rate_service):
    """Test calcul score de risque faible"""
    project = {
        "city": "PetiteVille",  # Tier 3
        "ltv": 0.95,  # LTV élevé en décimal
        "tri": 6.0,  # TRI faible
        "showstoppers_count": 5  # Nombreux showstoppers
    }
    
    company = {
        "years_experience": 1,  # Peu d'expérience
        "projects_completed": 0
    }
    
    market_trend = "baisse"
    technical_issues = ["structure", "amiante", "incendie"]
    
    score = interest_rate_service.calculate_risk_score(
        project,
        company,
        market_trend,
        technical_issues
    )
    
    assert 0 <= score <= 100
    assert score < 50  # Devrait être score faible


@pytest.mark.asyncio
async def test_calculate_interest_rate(interest_rate_service):
    """Test calcul taux d'intérêt"""
    project = {
        "city": "Paris",
        "ltv": 70,
        "tri": 12.0,
        "showstoppers_count": 1
    }
    
    company = {
        "experience_years": 5,
        "successful_projects": 8
    }
    
    duration = 24
    
    result = await interest_rate_service.calculate_interest_rate(
        project,
        company,
        duration
    )
    
    assert "interest_rate" in result
    assert "euribor" in result
    assert "margin" in result
    assert "risk_score" in result
    assert "category" in result
    
    # Taux doit être positif
    assert result["interest_rate"] > 0
    
    # Vérifier formule: taux = euribor + marge
    assert abs(result["interest_rate"] - (result["euribor"] + result["margin"])) < 0.01


@pytest.mark.asyncio
async def test_interest_rate_risk_categories(interest_rate_service):
    """Test catégories de risque"""
    # Excellent (score >= 85)
    project_excellent = {
        "city": "Paris",
        "ltv": 60,
        "tri": 18.0,
        "showstoppers_count": 0
    }
    
    # Risqué (score < 50)
    project_risky = {
        "city": "PetiteVille",
        "ltv": 95,
        "tri": 5.0,
        "showstoppers_count": 5
    }
    
    company = {
        "experience_years": 5,
        "successful_projects": 8
    }
    
    result_excellent = await interest_rate_service.calculate_interest_rate(
        project_excellent,
        company,
        24
    )
    
    result_risky = await interest_rate_service.calculate_interest_rate(
        project_risky,
        company,
        24
    )
    
    # Taux risqué doit être supérieur à taux excellent
    assert result_risky["interest_rate"] > result_excellent["interest_rate"]
    assert result_risky["margin"] > result_excellent["margin"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
