"""
TEST SECTION 8: CONFIDENTIALITÉ (PRIVACY SHIELD)
Tests de la règle des 2 mois et cloisonnement des données
"""
import pytest
from datetime import datetime, timedelta
from app.services.privacy_shield_service import privacy_shield_service


class TestRegleDe2Mois:
    """Test: Données privées pendant 2 mois après sortie deal"""
    
    def test_donnees_privees_projet_actif(self):
        """Les données d'un projet actif sont marquées privées"""
        project_id = 123
        
        # Créer un projet actif (pas encore sorti)
        project_status = privacy_shield_service.get_project_privacy_status(
            project_id=project_id,
            deal_status="ACTIVE",
            exit_date=None
        )
        
        assert project_status["is_private"] is True
        assert project_status["can_use_for_training"] is False
    
    def test_donnees_privees_apres_sortie_recente(self):
        """Données restent privées 2 mois après sortie du deal"""
        project_id = 456
        
        # Sortie il y a 1 mois
        exit_date = datetime.now() - timedelta(days=30)
        
        project_status = privacy_shield_service.get_project_privacy_status(
            project_id=project_id,
            deal_status="EXITED",
            exit_date=exit_date
        )
        
        assert project_status["is_private"] is True
        assert project_status["can_use_for_training"] is False
        assert project_status["days_until_public"] > 0
    
    def test_donnees_publiques_apres_2_mois(self):
        """Après 2 mois de sortie, données utilisables pour modèle"""
        project_id = 789
        
        # Sortie il y a 3 mois
        exit_date = datetime.now() - timedelta(days=90)
        
        project_status = privacy_shield_service.get_project_privacy_status(
            project_id=project_id,
            deal_status="EXITED",
            exit_date=exit_date
        )
        
        assert project_status["is_private"] is False
        assert project_status["can_use_for_training"] is True
        assert project_status["days_until_public"] == 0


class TestCloisonnementDonnees:
    """Test: Aucune fuite de données entre projets"""
    
    def test_pas_de_fuite_entre_projets(self):
        """Les données d'un projet ne fuient pas vers un autre"""
        # Projet A (fonds X)
        project_a_id = 111
        project_a_data = {
            "fund_id": "FUND_X",
            "purchase_price": 5_000_000,
            "internal_irr_target": 0.20
        }
        
        # Projet B (fonds Y)
        project_b_id = 222
        project_b_data = {
            "fund_id": "FUND_Y",
            "purchase_price": 3_000_000,
            "internal_irr_target": 0.15
        }
        
        # Vérifier isolation
        accessible_from_b = privacy_shield_service.get_accessible_project_data(
            requesting_project_id=project_b_id,
            target_project_id=project_a_id
        )
        
        # Projet B ne doit PAS voir les données privées de Projet A
        assert accessible_from_b is None or accessible_from_b.get("fund_id") != "FUND_X"
    
    def test_acces_uniquement_donnees_publiques(self):
        """Un projet ne peut accéder qu'aux données publiques"""
        project_id = 333
        
        # Récupérer suggestions CAPEX (basées sur historique)
        suggestions = privacy_shield_service.get_capex_suggestions_from_history(
            project_id=project_id,
            asset_type="BUREAU",
            surface_m2=1000
        )
        
        # Vérifier que les suggestions ne viennent QUE de projets publics
        for suggestion in suggestions:
            assert suggestion["source_project_status"] == "PUBLIC"
            assert suggestion["exit_date"] is not None
            
            # Vérifier que la sortie date > 2 mois
            days_since_exit = (datetime.now() - suggestion["exit_date"]).days
            assert days_since_exit > 60


class TestCloisonnementStrict:
    """Test: Cloisonnement strict entre fonds"""
    
    def test_fonds_ne_voient_pas_donnees_concurrents(self):
        """Un fonds ne voit pas les données d'un fonds concurrent"""
        fund_a_projects = privacy_shield_service.get_fund_projects("FUND_A")
        fund_b_projects = privacy_shield_service.get_fund_projects("FUND_B")
        
        # Aucun overlap entre les deux listes
        fund_a_ids = {p["id"] for p in fund_a_projects}
        fund_b_ids = {p["id"] for p in fund_b_projects}
        
        assert len(fund_a_ids & fund_b_ids) == 0
    
    def test_pas_de_recommendations_basees_sur_concurrents(self):
        """Les recommandations IA ne doivent pas utiliser données concurrents"""
        project_id = 444
        fund_id = "FUND_X"
        
        recommendations = privacy_shield_service.get_ai_recommendations(
            project_id=project_id,
            fund_id=fund_id
        )
        
        # Vérifier que les sources ne viennent PAS de fonds actifs
        for rec in recommendations:
            if "source_fund_id" in rec:
                source_fund = rec["source_fund_id"]
                
                # Si même fonds, OK
                if source_fund == fund_id:
                    continue
                
                # Si autre fonds, le projet source doit être PUBLIC
                assert rec["source_project_status"] == "PUBLIC"


class TestAuditTrail:
    """Test: Traçabilité des accès aux données"""
    
    def test_logs_acces_donnees_sensibles(self):
        """Les accès aux données sensibles sont loggés"""
        project_id = 555
        user_id = "user_123"
        
        # Accéder aux données financières
        data = privacy_shield_service.access_financial_data(
            project_id=project_id,
            user_id=user_id
        )
        
        # Vérifier qu'un log a été créé
        logs = privacy_shield_service.get_access_logs(project_id=project_id)
        
        assert len(logs) > 0
        last_log = logs[-1]
        
        assert last_log["user_id"] == user_id
        assert last_log["accessed_at"] is not None
        assert last_log["data_type"] == "FINANCIAL"
    
    def test_refus_acces_non_autorise(self):
        """Les accès non autorisés sont refusés et loggés"""
        project_id = 666
        unauthorized_user_id = "hacker_999"
        
        with pytest.raises(PermissionError):
            privacy_shield_service.access_financial_data(
                project_id=project_id,
                user_id=unauthorized_user_id
            )
        
        # Vérifier que la tentative est loggée
        logs = privacy_shield_service.get_access_logs(project_id=project_id)
        
        denied_attempts = [log for log in logs if log.get("access_denied") is True]
        assert len(denied_attempts) > 0


class TestAnonymisation:
    """Test: Anonymisation des données publiques"""
    
    def test_donnees_publiques_anonymisees(self):
        """Les données publiques sont anonymisées"""
        project_id = 777
        
        # Marquer comme public (après 2 mois)
        exit_date = datetime.now() - timedelta(days=90)
        privacy_shield_service.mark_project_as_exited(project_id, exit_date)
        
        # Récupérer données publiques
        public_data = privacy_shield_service.get_public_project_data(project_id)
        
        # Vérifier anonymisation
        assert "fund_name" not in public_data or public_data["fund_name"] == "ANONYME"
        assert "contact_email" not in public_data
        assert "contact_phone" not in public_data
        assert "internal_notes" not in public_data
    
    def test_donnees_techniques_preservees(self):
        """Les données techniques sont préservées (utiles pour IA)"""
        project_id = 888
        
        exit_date = datetime.now() - timedelta(days=90)
        privacy_shield_service.mark_project_as_exited(project_id, exit_date)
        
        public_data = privacy_shield_service.get_public_project_data(project_id)
        
        # Ces données DOIVENT être présentes
        assert "asset_type" in public_data
        assert "surface_m2" in public_data
        assert "capex_total" in public_data
        assert "construction_duration" in public_data


class TestConformiteRGPD:
    """Test: Conformité RGPD"""
    
    def test_droit_oubli(self):
        """Un utilisateur peut demander suppression de ses données"""
        user_id = "user_789"
        
        # Supprimer toutes les données utilisateur
        privacy_shield_service.delete_user_data(user_id)
        
        # Vérifier que les données sont bien supprimées
        user_data = privacy_shield_service.get_user_data(user_id)
        
        assert user_data is None or user_data == {}
    
    def test_export_donnees_personnelles(self):
        """Un utilisateur peut exporter ses données (portabilité)"""
        user_id = "user_456"
        
        export = privacy_shield_service.export_user_data(user_id)
        
        assert export is not None
        assert "projects" in export
        assert "personal_info" in export
        assert isinstance(export, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
