from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import ai_service
from typing import List

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatMessage(BaseModel):
    role: str  # "user" ou "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    context: dict | None = None
    history: List[ChatMessage] | None = None

class ChatResponse(BaseModel):
    message: str
    timestamp: str

@router.post("/", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """Chat avec l'assistant IA métier"""
    
    try:
        response = await ai_service.chat_assistance(
            message=request.message,
            context=request.context
        )
        
        from datetime import datetime
        
        return ChatResponse(
            message=response,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération de la réponse: {str(e)}"
        )

class DocumentAnalysisRequest(BaseModel):
    text: str
    document_type: str = "default"

@router.post("/analyze-document")
async def analyze_text(request: DocumentAnalysisRequest):
    """Analyser un texte avec l'IA"""
    
    try:
        analysis = await ai_service.analyze_document(
            text=request.text,
            document_type=request.document_type
        )
        
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse: {str(e)}"
        )
