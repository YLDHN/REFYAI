"""
TEST SECTION 5: IA PRÉDICTIVE (AVEC MOCKS)
Tests de la mécanique IA sans appel OpenAI réel
"""
import pytest
from unittest.mock import Mock, patch
from app.services.capex_service import capex_service


class TestSuggestionCAPEX:
    """Test endpoint suggestion CAPEX avec mocks"""
    
    @patch('app.services.capex_ai_service.capex_ai_service.suggest_capex')
    def test_suggestion_retourne_montant_et_justification(self, mock_suggest):
        """L'endpoint renvoie montant + justification"""
        # Mock de la réponse IA
        mock_suggest.return_value = {
            "suggested_amount": 450_000,
            "cost_per_m2": 375,
            "justification": "Bureau ancien nécessite rénovation complète",
            "confidence": "MEDIUM",
            "postes_suggeres": [
                {"key": "facade_ravalement", "quantity": 150, "unit": "m2"},
                {"key": "electricite_renovation", "quantity": 1200, "unit": "m2"}
            ]
        }
        
        result = capex_service.get_ai_suggestion(
            project_description="Bureaux 1200m2 années 80 à rénover",
            surface_m2=1200,
            typologie="RENOVATION",
            city_tier=1
        )
        
        assert "suggested_amount" in result
        assert "justification" in result
        assert result["suggested_amount"] > 0
        assert isinstance(result["justification"], str)
    
    @patch('app.services.capex_ai_service.capex_ai_service.suggest_capex')
    def test_suggestion_coherente_avec_typologie(self, mock_suggest):
        """Suggestion cohérente avec typologie et année"""
        # Mock: Bureaux anciens = rénovation lourde
        mock_suggest.return_value = {
            "suggested_amount": 600_000,
            "cost_per_m2": 500,
            "justification": "Bâtiment ancien (années 70) nécessite mise aux normes",
            "confidence": "HIGH"
        }
        
        result = capex_service.get_ai_suggestion(
            project_description="Bureaux 1970, 1200m2, Paris",
            surface_m2=1200,
            typologie="RENOVATION_LOURDE",
            construction_year=1970,
            city_tier=1
        )
        
        # Rénovation lourde = coût élevé
        assert result["cost_per_m2"] > 400
    
    @patch('app.services.capex_ai_service.capex_ai_service.suggest_capex')
    def test_suggestion_modifiable_par_utilisateur(self, mock_suggest):
        """L'utilisateur peut modifier ou ignorer la suggestion"""
        mock_suggest.return_value = {
            "suggested_amount": 450_000,
            "cost_per_m2": 375,
            "justification": "Suggestion IA",
            "confidence": "MEDIUM"
        }
        
        # Récupérer suggestion
        suggestion = capex_service.get_ai_suggestion(
            project_description="Bureau 1200m2",
            surface_m2=1200,
            typologie="RENOVATION"
        )
        
        # Utilisateur modifie
        user_capex = 600_000  # Différent de la suggestion
        
        # Le système accepte la valeur utilisateur
        final_capex = capex_service.override_capex_suggestion(
            project_id=123,
            suggested_amount=suggestion["suggested_amount"],
            user_amount=user_capex
        )
        
        assert final_capex == user_capex
        assert final_capex != suggestion["suggested_amount"]


class TestMecaniqueIA:
    """Test de la mécanique IA (pas la qualité du texte)"""
    
    @pytest.mark.skip(reason="Nécessite capex_ai_service - intégration IA future")
    @patch('app.services.capex_ai_service.capex_ai_service.llm')
    def test_appel_llm_structure(self, mock_llm):
        """L'appel LLM est bien structuré"""
        mock_llm.invoke.return_value = Mock(
            content='{"suggested_amount": 500000, "justification": "Test"}'
        )
        
        result = capex_service.get_ai_suggestion(
            project_description="Test",
            surface_m2=1000,
            typologie="RENOVATION"
        )
        
        # Vérifier que le LLM a été appelé
        assert mock_llm.invoke.called
    
    @pytest.mark.skip(reason="Nécessite capex_ai_service - intégration IA future")
    @patch('app.services.capex_ai_service.capex_ai_service.suggest_capex')
    def test_gestion_erreur_ia(self, mock_suggest):
        """Si l'IA échoue, retourner une valeur par défaut"""
        # Simuler erreur IA
        mock_suggest.side_effect = Exception("API OpenAI timeout")
        
        result = capex_service.get_ai_suggestion(
            project_description="Test",
            surface_m2=1000,
            typologie="RENOVATION"
        )
        
        # Fallback: calcul basique sans IA
        assert "error" in result or result["suggested_amount"] > 0
        assert result.get("fallback_mode") is True
    
    @patch('app.services.capex_ai_service.capex_ai_service.suggest_capex')
    def test_pas_appel_ia_si_key_manquante(self, mock_suggest):
        """Si OPENAI_API_KEY absente, pas d'appel IA"""
        with patch.dict('os.environ', {}, clear=True):
            result = capex_service.get_ai_suggestion(
                project_description="Test",
                surface_m2=1000,
                typologie="RENOVATION"
            )
            
            # Doit retourner un fallback, pas une erreur
            assert "error" in result or "fallback_mode" in result
            # Le mock ne doit pas être appelé
            assert not mock_suggest.called


class TestCoherenceSuggestions:
    """Test cohérence des suggestions"""
    
    @patch('app.services.capex_ai_service.capex_ai_service.suggest_capex')
    def test_cout_m2_dans_fourchette_realiste(self, mock_suggest):
        """Le coût/m² doit être dans une fourchette réaliste"""
        mock_suggest.return_value = {
            "suggested_amount": 450_000,
            "cost_per_m2": 375,
            "justification": "Test",
            "confidence": "MEDIUM"
        }
        
        result = capex_service.get_ai_suggestion(
            project_description="Bureau 1200m2",
            surface_m2=1200,
            typologie="RENOVATION"
        )
        
        # Fourchette réaliste: 200-1800 €/m² (incluant rénovation lourde)
        assert 200 <= result["cost_per_m2"] <= 1800
    
    @patch('app.services.capex_ai_service.capex_ai_service.suggest_capex')
    def test_montant_total_coherent_avec_surface(self, mock_suggest):
        """Montant total = surface × coût/m² (±10%)"""
        mock_suggest.return_value = {
            "suggested_amount": 450_000,
            "cost_per_m2": 375,
            "justification": "Test",
            "confidence": "MEDIUM"
        }
        
        result = capex_service.get_ai_suggestion(
            project_description="Bureau 1200m2",
            surface_m2=1200,
            typologie="RENOVATION"
        )
        
        expected = result["surface_m2"] * result["cost_per_m2"]
        tolerance = expected * 0.10
        
        assert abs(result["suggested_amount"] - expected) <= tolerance


class TestNiveauConfiance:
    """Test du niveau de confiance"""
    
    @patch('app.services.capex_ai_service.capex_ai_service.suggest_capex')
    def test_confiance_elevee_si_projet_similaire(self, mock_suggest):
        """Confiance HIGH si projet similaire en base"""
        mock_suggest.return_value = {
            "suggested_amount": 450_000,
            "cost_per_m2": 375,
            "justification": "3 projets similaires trouvés en historique",
            "confidence": "HIGH",
            "similar_projects_count": 3
        }
        
        result = capex_service.get_ai_suggestion(
            project_description="Bureau 1200m2 Paris",
            surface_m2=1200,
            typologie="RENOVATION"
        )
        
        assert result["confidence"] == "HIGH"
        assert result["similar_projects_count"] > 0
    
    @patch('app.services.capex_ai_service.capex_ai_service.suggest_capex')
    def test_confiance_faible_si_typologie_rare(self, mock_suggest):
        """Confiance LOW si typologie atypique"""
        mock_suggest.return_value = {
            "suggested_amount": 800_000,
            "cost_per_m2": 800,
            "justification": "Typologie rare, estimation incertaine",
            "confidence": "LOW",
            "similar_projects_count": 0
        }
        
        result = capex_service.get_ai_suggestion(
            project_description="Château à convertir en hôtel",
            surface_m2=1000,
            typologie="CONVERSION_ATYPIQUE"
        )
        
        assert result["confidence"] == "LOW"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
