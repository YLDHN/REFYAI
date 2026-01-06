"""
Service IA pour suggestions CAPEX intelligentes
Utilise LangChain + OpenAI + ChromaDB pour analyse historique
"""
import os
from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
import json

from app.services.capex_service import capex_service


class CAPEXAIService:
    """Service IA pour suggestions CAPEX personnalisées"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.llm = None
        self.embeddings = None
        self.vector_store = None
        
        # Initialisation lazy : uniquement si API key présente
        if self.openai_api_key and self.openai_api_key.startswith("sk-"):
            try:
                # LLM pour génération
                self.llm = ChatOpenAI(
                    model="gpt-4-turbo-preview",
                    temperature=0.3,
                    api_key=self.openai_api_key
                )
                
                # Embeddings pour RAG
                self.embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
                
                # ChromaDB pour historique projets
                self._init_vector_store()
            except Exception as e:
                print(f"⚠️  CAPEX AI Service: OpenAI non disponible - {str(e)}")
        else:
            print("⚠️  CAPEX AI Service: OPENAI_API_KEY non configurée")
    
    def _init_vector_store(self):
        """Initialise ChromaDB avec projets historiques"""
        try:
            # Chemin persistant pour ChromaDB
            persist_directory = "./chroma_db"
            
            # Tentative de charger DB existante
            self.vector_store = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings,
                collection_name="capex_projects"
            )
            
            # Si collection vide, initialiser avec exemples
            if self.vector_store._collection.count() == 0:
                self._populate_initial_data()
                
        except Exception as e:
            print(f"⚠️ Erreur init ChromaDB: {e}")
            self.vector_store = None
    
    def _populate_initial_data(self):
        """Peuple ChromaDB avec projets exemples (à remplacer par vraies données)"""
        example_projects = [
            {
                "description": "Réhabilitation immeuble haussmannien 1200m2 Paris 17ème, 8 appartements, façade à refaire",
                "typologie": "RESIDENTIAL",
                "surface": 1200,
                "capex": {
                    "facade_ravalement_simple": {"quantity": 400, "unit": "m2", "cost": 180000},
                    "charpente_refection": {"quantity": 200, "unit": "m2", "cost": 60000},
                    "electricite_renovation": {"quantity": 1200, "unit": "m2", "cost": 84000},
                    "plomberie_renovation": {"quantity": 1200, "unit": "m2", "cost": 72000},
                    "menuiseries_double_vitrage": {"quantity": 45, "unit": "unité", "cost": 67500}
                },
                "total_capex": 463500,
                "cost_per_m2": 386
            },
            {
                "description": "Transformation bureaux 800m2 en logements Bordeaux centre, création 6 appartements",
                "typologie": "CONVERSION",
                "surface": 800,
                "capex": {
                    "demolition_legere": {"quantity": 200, "unit": "m2", "cost": 15000},
                    "cloisons_creation": {"quantity": 150, "unit": "m2", "cost": 18000},
                    "electricite_renovation": {"quantity": 800, "unit": "m2", "cost": 48000},
                    "plomberie_creation": {"quantity": 6, "unit": "unité", "cost": 36000},
                    "menuiseries_double_vitrage": {"quantity": 30, "unit": "unité", "cost": 45000},
                    "isolation_thermique": {"quantity": 800, "unit": "m2", "cost": 64000}
                },
                "total_capex": 226000,
                "cost_per_m2": 282
            },
            {
                "description": "Construction neuve 15 logements R+3 Lyon 3ème, parking souterrain",
                "typologie": "NEUF",
                "surface": 1500,
                "capex": {
                    "terrassement": {"quantity": 500, "unit": "m3", "cost": 50000},
                    "fondations": {"quantity": 300, "unit": "m2", "cost": 90000},
                    "structure_beton": {"quantity": 1500, "unit": "m2", "cost": 450000},
                    "facade_enduit": {"quantity": 600, "unit": "m2", "cost": 90000},
                    "toiture": {"quantity": 400, "unit": "m2", "cost": 60000},
                    "electricite_neuf": {"quantity": 1500, "unit": "m2", "cost": 120000},
                    "plomberie_neuf": {"quantity": 1500, "unit": "m2", "cost": 90000},
                    "ascenseur": {"quantity": 1, "unit": "unité", "cost": 80000}
                },
                "total_capex": 1030000,
                "cost_per_m2": 686
            }
        ]
        
        # Insérer dans ChromaDB
        texts = []
        metadatas = []
        
        for proj in example_projects:
            text = f"{proj['description']} | Surface: {proj['surface']}m2 | Typologie: {proj['typologie']} | Coût/m2: {proj['cost_per_m2']}€"
            texts.append(text)
            metadatas.append({
                "typologie": proj['typologie'],
                "surface": proj['surface'],
                "cost_per_m2": proj['cost_per_m2'],
                "capex_detail": json.dumps(proj['capex'])
            })
        
        if self.vector_store and texts:
            self.vector_store.add_texts(texts, metadatas=metadatas)
            print(f"✅ {len(texts)} projets exemples ajoutés à ChromaDB")
    
    async def suggest_capex_with_ai(
        self,
        project_description: str,
        surface: float,
        typologie: str,
        city_tier: int = 1
    ) -> Dict:
        """
        Suggère CAPEX intelligent basé sur IA + RAG historique
        
        Args:
            project_description: Description textuelle du projet
            surface: Surface en m2
            typologie: NEUF, RENOVATION, CONVERSION, etc.
            city_tier: Niveau ville (1,2,3)
        
        Returns:
            Dict avec suggestions CAPEX détaillées
        """
        
        # Vérifier si le service IA est disponible
        if not self.llm:
            return {
                "postes_suggeres": [],
                "budget_estime": 0,
                "cout_m2_estime": 0,
                "niveau_confiance": "UNAVAILABLE",
                "warnings": ["Service CAPEX AI non disponible - OPENAI_API_KEY non configurée"],
                "error": "OPENAI_API_KEY_MISSING"
            }
        
        # === ÉTAPE 1 : RAG - Recherche projets similaires ===
        similar_projects = []
        if self.vector_store:
            try:
                query = f"{project_description} {typologie} {surface}m2"
                results = self.vector_store.similarity_search(query, k=3)
                
                for doc in results:
                    similar_projects.append({
                        "description": doc.page_content,
                        "metadata": doc.metadata
                    })
            except Exception as e:
                print(f"⚠️ Erreur RAG: {e}")
        
        # === ÉTAPE 2 : LLM - Génération suggestions ===
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""Tu es un expert en CAPEX immobilier.
Analyse le projet et suggère les postes de travaux nécessaires avec quantités réalistes.

Base-toi sur:
1. Les projets similaires fournis (historique)
2. Les standards du marché français
3. La typologie du projet (NEUF, RENOVATION, CONVERSION)

Retourne un JSON avec:
{
  "postes_suggeres": [
    {
      "key": "facade_ravalement_simple",
      "label": "Ravalement façade simple",
      "quantity": 150,
      "unit": "m2",
      "justification": "Façade de 150m2 à rénover"
    }
  ],
  "budget_estime": 250000,
  "cout_m2_estime": 500,
  "niveau_confiance": "MEDIUM",
  "warnings": ["Attention: diagnostic amiante requis avant démolition"]
}"""),
            HumanMessage(content=f"""Projet à analyser:
- Description: {project_description}
- Surface: {surface} m2
- Typologie: {typologie}
- Ville: Tier {city_tier}

Projets similaires (historique):
{json.dumps(similar_projects, indent=2, ensure_ascii=False)}

Postes CAPEX disponibles:
{json.dumps(list(capex_service.get_all_categories().keys()), ensure_ascii=False)}

Suggère les postes pertinents avec quantités.""")
        ])
        
        try:
            messages = prompt.format_messages()
            response = self.llm.invoke(messages)
            
            # Parse réponse JSON
            content = response.content
            # Nettoyer markdown si présent
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            ai_suggestions = json.loads(content)
            
            # === ÉTAPE 3 : Enrichissement avec données réelles CAPEX ===
            postes_enrichis = []
            total_min = 0
            total_max = 0
            total_avg = 0
            
            for poste in ai_suggestions.get("postes_suggeres", []):
                key = poste.get("key")
                quantity = poste.get("quantity", 0)
                
                # Récupérer coûts réels
                estimate = capex_service.get_cost_estimate(key, quantity, city_tier)
                
                if "error" not in estimate:
                    postes_enrichis.append({
                        **poste,
                        "estimate": estimate
                    })
                    total_min += estimate["total_min"]
                    total_max += estimate["total_max"]
                    total_avg += estimate["total_avg"]
            
            return {
                "success": True,
                "ai_analysis": {
                    "description": project_description,
                    "surface": surface,
                    "typologie": typologie,
                    "niveau_confiance": ai_suggestions.get("niveau_confiance", "MEDIUM"),
                    "warnings": ai_suggestions.get("warnings", [])
                },
                "similar_projects_used": len(similar_projects),
                "suggested_items": postes_enrichis,
                "budget_estimate": {
                    "total_min": total_min,
                    "total_avg": total_avg,
                    "total_max": total_max,
                    "cost_per_m2_avg": total_avg / surface if surface > 0 else 0,
                    "contingency_10pct": total_avg * 0.10,
                    "total_with_contingency": total_avg * 1.10
                },
                "next_steps": [
                    "Affiner les quantités après visite terrain",
                    "Obtenir devis artisans pour confirmation",
                    "Vérifier diagnostics techniques obligatoires"
                ]
            }
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Erreur parsing IA: {e}",
                "raw_response": content if 'content' in locals() else "N/A"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur IA: {str(e)}"
            }
    
    def suggest_capex(
        self,
        asset_type: str,
        surface_m2: float,
        construction_year: int = 2000,
        city: str = "Paris",
        additional_context: Optional[Dict] = None
    ) -> Dict:
        """
        Méthode simplifiée pour suggestion CAPEX (stub pour tests)
        
        Args:
            asset_type: Type d'actif
            surface_m2: Surface en m²
            construction_year: Année de construction
            city: Ville
            additional_context: Contexte additionnel
        
        Returns:
            Suggestion avec montant et justification
        """
        # Si OpenAI disponible, utiliser l'IA
        if self.llm:
            try:
                result = self.suggest_capex_from_description(
                    project_description=f"{asset_type} de {surface_m2}m² à {city}, construit en {construction_year}",
                    surface=surface_m2,
                    typologie=asset_type.upper()
                )
                
                if result.get("success"):
                    return {
                        "suggested_amount": result["budget_estimate"]["total_avg"],
                        "confidence": "HIGH",
                        "justification": f"Estimation basée sur {result['similar_projects_used']} projets similaires",
                        "cost_per_m2": result["budget_estimate"]["cost_per_m2_avg"],
                        "min_amount": result["budget_estimate"]["total_min"],
                        "max_amount": result["budget_estimate"]["total_max"]
                    }
            except Exception as e:
                print(f"Erreur IA suggestion: {e}")
        
        # Fallback: utiliser estimation basique
        from app.services.capex_service import capex_service
        return capex_service.get_ai_suggestion(
            asset_type=asset_type,
            surface_m2=surface_m2,
            construction_year=construction_year,
            city=city
        )


# Instance globale
capex_ai_service = CAPEXAIService()
