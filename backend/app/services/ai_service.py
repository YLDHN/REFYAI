"""
Services IA pour l'analyse de documents et l'assistance métier
"""
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from app.core.config import settings

class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    async def analyze_document(self, text: str, document_type: str) -> Dict[str, Any]:
        """
        Analyse un document avec l'IA
        
        Args:
            text: Contenu textuel du document
            document_type: Type de document (PLU, diagnostic, etc.)
        
        Returns:
            Résultat de l'analyse structuré
        """
        
        prompt = self._get_analysis_prompt(document_type, text)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en immobilier spécialisé dans l'analyse de documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            return {
                "success": True,
                "analysis": response.choices[0].message.content,
                "model": self.model
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _get_analysis_prompt(self, document_type: str, text: str) -> str:
        """Génère le prompt approprié selon le type de document"""
        
        prompts = {
            "plu": f"""
Analyse ce document PLU et identifie:
1. Les zones de construction autorisées
2. Les contraintes d'urbanisme (COS, CES, hauteurs)
3. Les restrictions particulières
4. Les risques réglementaires

Document:
{text}
""",
            "diagnostic": f"""
Analyse ce diagnostic technique et identifie:
1. Les problèmes majeurs détectés
2. Les risques pour la sécurité
3. Les travaux nécessaires
4. L'estimation des coûts de remise en état

Document:
{text}
""",
            "default": f"""
Analyse ce document immobilier et extrais les informations importantes:
{text}
"""
        }
        
        return prompts.get(document_type, prompts["default"])
    
    async def chat_assistance(self, message: str, context: Optional[Dict] = None) -> str:
        """
        Chat IA métier pour assister l'utilisateur
        
        Args:
            message: Message de l'utilisateur
            context: Contexte du projet (optionnel)
        
        Returns:
            Réponse de l'assistant
        """
        
        system_prompt = """
Tu es un assistant expert en immobilier d'investissement.
Tu aides les professionnels à analyser leurs projets immobiliers.
Tu es spécialisé en:
- Analyse réglementaire (PLU, urbanisme)
- Calculs financiers (TRI, LTV, DSCR)
- Évaluation des risques
- Stratégies d'investissement
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Erreur lors de la génération de la réponse: {str(e)}"

# Instance globale
ai_service = AIService()
