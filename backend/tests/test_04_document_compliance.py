"""
TEST SECTION 4: CONFORMITÉ DOCUMENTAIRE (CHECKLIST DYNAMIQUE)
Tests de la logique déterministe de documents requis
"""
import pytest
from app.services.document_service import document_service


class TestChecklistDynamique:
    """Test: Liste documents dépend de la typologie"""
    
    def test_documents_logistique(self):
        """Logistique → ICPE, rapport de sol, accessibilité PL"""
        required_docs = document_service.get_required_documents(
            asset_type="LOGISTIQUE",
            surface_m2=5000,
            construction_year=2010
        )
        
        required_names = [doc["name"] for doc in required_docs]
        
        assert "ICPE" in required_names
        assert "RAPPORT_SOL" in required_names
        assert "ACCESSIBILITE_PL" in required_names
        assert "ETUDE_FLUX" in required_names
    
    def test_documents_bureaux(self):
        """Bureau → DPE, Décret Tertiaire, conformité ERP"""
        required_docs = document_service.get_required_documents(
            asset_type="BUREAU",
            surface_m2=3000,
            construction_year=2005
        )
        
        required_names = [doc["name"] for doc in required_docs]
        
        assert "DPE" in required_names
        assert "DECRET_TERTIAIRE" in required_names
        assert "CONFORMITE_ERP" in required_names
    
    def test_documents_residentiel(self):
        """Résidentiel → Étude de sol, PLU, diagnostics"""
        required_docs = document_service.get_required_documents(
            asset_type="RESIDENTIEL",
            surface_m2=1500,
            construction_year=1990
        )
        
        required_names = [doc["name"] for doc in required_docs]
        
        assert "ETUDE_SOL" in required_names
        assert "PLU" in required_names
        assert "DIAGNOSTIC_AMIANTE" in required_names
        assert "DIAGNOSTIC_PLOMB" in required_names


class TestDocumentsManquants:
    """Test: Détection exacte des documents manquants"""
    
    def test_detection_documents_manquants(self):
        """Le backend dit exactement quels documents manquent"""
        project_id = 123
        
        # Documents requis pour logistique
        required = document_service.get_required_documents(
            asset_type="LOGISTIQUE",
            surface_m2=5000,
            construction_year=2010
        )
        
        # Documents uploadés (incomplets)
        uploaded = document_service.get_uploaded_documents(project_id)
        uploaded_names = [doc["document_type"] for doc in uploaded]
        
        # Calcul des manquants
        missing = document_service.get_missing_documents(
            project_id=project_id,
            asset_type="LOGISTIQUE",
            surface_m2=5000,
            construction_year=2010
        )
        
        required_names = [doc["name"] for doc in required]
        missing_names = [doc["name"] for doc in missing]
        
        # Vérification: manquants = requis - uploadés
        expected_missing = set(required_names) - set(uploaded_names)
        assert set(missing_names) == expected_missing
    
    def test_aucun_manquant_si_complet(self):
        """Si tous les docs sont uploadés, liste vide"""
        project_id = 456
        
        # Simuler upload de tous les documents requis
        required = document_service.get_required_documents(
            asset_type="BUREAU",
            surface_m2=2000,
            construction_year=2015
        )
        
        # Upload simulé de tous les docs
        for doc in required:
            document_service.upload_document_sync(
                project_id=project_id,
                document_type=doc["name"],
                file_path="/fake/path.pdf"
            )
        
        missing = document_service.get_missing_documents(
            project_id=project_id,
            asset_type="BUREAU",
            surface_m2=2000,
            construction_year=2015
        )
        
        assert len(missing) == 0


class TestLogiqueDeterministe:
    """Test: Logique 100% déterministe, sans IA"""
    
    def test_pas_de_variabilite(self):
        """Appels multiples = même résultat"""
        result1 = document_service.get_required_documents(
            asset_type="LOGISTIQUE",
            surface_m2=5000,
            construction_year=2010
        )
        
        result2 = document_service.get_required_documents(
            asset_type="LOGISTIQUE",
            surface_m2=5000,
            construction_year=2010
        )
        
        assert result1 == result2
    
    def test_pas_hallucination(self):
        """Aucun document fantaisiste ou inventé"""
        required = document_service.get_required_documents(
            asset_type="COMMERCE",
            surface_m2=500,
            construction_year=2000
        )
        
        # Liste blanche de documents officiels
        valid_docs = [
            "PLU", "DPE", "ICPE", "ERP", "DIAGNOSTIC_AMIANTE",
            "DIAGNOSTIC_PLOMB", "RAPPORT_SOL", "PC", "DP",
            "CONFORMITE_ERP", "ACCESSIBILITE", "ETUDE_SOL"
        ]
        
        for doc in required:
            assert doc["name"] in valid_docs, \
                f"Document inconnu détecté: {doc['name']}"
    
    def test_documents_obligatoires_toujours_presents(self):
        """Certains docs sont toujours obligatoires"""
        for asset_type in ["LOGISTIQUE", "BUREAU", "RESIDENTIEL", "COMMERCE"]:
            required = document_service.get_required_documents(
                asset_type=asset_type,
                surface_m2=1000,
                construction_year=2010
            )
            
            required_names = [doc["name"] for doc in required]
            
            # PLU toujours requis
            assert "PLU" in required_names


class TestDocumentsConditionnels:
    """Test: Certains documents dépendent des caractéristiques"""
    
    def test_amiante_si_avant_1997(self):
        """Diagnostic amiante obligatoire si construction avant 1997"""
        # Avant 1997
        required_old = document_service.get_required_documents(
            asset_type="BUREAU",
            surface_m2=2000,
            construction_year=1990
        )
        
        # Après 1997
        required_new = document_service.get_required_documents(
            asset_type="BUREAU",
            surface_m2=2000,
            construction_year=2000
        )
        
        old_names = [doc["name"] for doc in required_old]
        new_names = [doc["name"] for doc in required_new]
        
        assert "DIAGNOSTIC_AMIANTE" in old_names
        assert "DIAGNOSTIC_AMIANTE" not in new_names
    
    def test_icpe_si_logistique_grande_surface(self):
        """ICPE obligatoire si logistique > 2000m²"""
        # Petite surface
        required_small = document_service.get_required_documents(
            asset_type="LOGISTIQUE",
            surface_m2=1500,
            construction_year=2010
        )
        
        # Grande surface
        required_large = document_service.get_required_documents(
            asset_type="LOGISTIQUE",
            surface_m2=5000,
            construction_year=2010
        )
        
        small_names = [doc["name"] for doc in required_small]
        large_names = [doc["name"] for doc in required_large]
        
        assert "ICPE" not in small_names
        assert "ICPE" in large_names


class TestStatutConformite:
    """Test: Calcul du statut de conformité documentaire"""
    
    def test_statut_conforme_si_100_percent(self):
        """Statut CONFORME si tous les docs sont présents"""
        project_id = 789
        
        # Upload de tous les docs requis
        required = document_service.get_required_documents(
            asset_type="BUREAU",
            surface_m2=2000,
            construction_year=2015
        )
        
        for doc in required:
            document_service.upload_document_sync(
                project_id=project_id,
                document_type=doc["name"],
                file_path="/fake/path.pdf"
            )
        
        status = document_service.get_compliance_status(
            project_id=project_id,
            asset_type="BUREAU",
            surface_m2=2000,
            construction_year=2015
        )
        
        assert status["compliance_rate"] == 100
        assert status["status"] == "CONFORME"
    
    def test_statut_partiel_si_incomplet(self):
        """Statut PARTIEL si 50-99% des docs"""
        project_id = 890
        
        required = document_service.get_required_documents(
            asset_type="LOGISTIQUE",
            surface_m2=5000,
            construction_year=2010
        )
        
        # Upload de 75% des docs
        for i, doc in enumerate(required):
            if i < len(required) * 0.75:
                document_service.upload_document_sync(
                    project_id=project_id,
                    document_type=doc["name"],
                    file_path="/fake/path.pdf"
                )
        
        status = document_service.get_compliance_status(
            project_id=project_id,
            asset_type="LOGISTIQUE",
            surface_m2=5000,
            construction_year=2010
        )
        
        assert 50 <= status["compliance_rate"] < 100
        assert status["status"] == "PARTIEL"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
