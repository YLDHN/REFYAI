"""
Service d'extraction de texte depuis documents
"""
from typing import Optional
import PyPDF2
from docx import Document
import io

class DocumentExtractionService:
    """Service pour extraire le texte des documents PDF et DOCX"""
    
    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """
        Extrait le texte d'un fichier PDF
        
        Args:
            file_bytes: Contenu binaire du fichier PDF
            
        Returns:
            Texte extrait du PDF
        """
        try:
            pdf_file = io.BytesIO(file_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction du PDF: {str(e)}")
    
    def extract_text_from_docx(self, file_bytes: bytes) -> str:
        """
        Extrait le texte d'un fichier DOCX
        
        Args:
            file_bytes: Contenu binaire du fichier DOCX
            
        Returns:
            Texte extrait du DOCX
        """
        try:
            docx_file = io.BytesIO(file_bytes)
            doc = Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction du DOCX: {str(e)}")
    
    def extract_text(self, file_bytes: bytes, mime_type: str) -> str:
        """
        Extrait le texte d'un document selon son type
        
        Args:
            file_bytes: Contenu binaire du fichier
            mime_type: Type MIME du fichier
            
        Returns:
            Texte extrait
        """
        if mime_type == "application/pdf":
            return self.extract_text_from_pdf(file_bytes)
        elif mime_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            return self.extract_text_from_docx(file_bytes)
        else:
            raise ValueError(f"Type de document non supporté: {mime_type}")

# Instance globale
document_extraction_service = DocumentExtractionService()
