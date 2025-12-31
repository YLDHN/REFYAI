"""
Service complet de gestion des documents
Upload, stockage, extraction, analyse
"""
from typing import Dict, List, Optional, BinaryIO
import os
import uuid
from datetime import datetime
from pathlib import Path
import mimetypes
import PyPDF2
from PIL import Image
import pytesseract


class DocumentType:
    """Types de documents"""
    PLU = "plu"
    DIAGNOSTIC = "diagnostic"
    CADASTRE = "cadastre"
    PHOTOS = "photos"
    PLANS = "plans"
    DEVIS = "devis"
    FACTURES = "factures"
    CONTRATS = "contrats"
    ATTESTATIONS = "attestations"
    COURRIERS = "courriers"
    OTHER = "other"


class DocumentStatus:
    """Statut d'analyse du document"""
    UPLOADED = "uploaded"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    ERROR = "error"


class DocumentService:
    """Service de gestion des documents"""
    
    def __init__(self, storage_path: str = "/tmp/refyai_documents"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    async def upload_document(
        self,
        file: BinaryIO,
        filename: str,
        project_id: int,
        document_type: str = DocumentType.OTHER,
        user_id: Optional[int] = None
    ) -> Dict:
        """
        Upload et stockage d'un document
        
        Args:
            file: Fichier binaire
            filename: Nom original du fichier
            project_id: ID du projet
            document_type: Type de document
            user_id: ID utilisateur (optionnel)
        
        Returns:
            Métadonnées du document uploadé
        """
        try:
            # Générer nom unique
            file_extension = Path(filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Créer dossier projet
            project_folder = self.storage_path / str(project_id)
            project_folder.mkdir(parents=True, exist_ok=True)
            
            # Sauvegarder fichier
            file_path = project_folder / unique_filename
            
            # Lire contenu
            content = await file.read()
            file_size = len(content)
            
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Détecter MIME type
            mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
            
            return {
                "success": True,
                "document": {
                    "filename": unique_filename,
                    "original_filename": filename,
                    "file_path": str(file_path),
                    "file_size": file_size,
                    "mime_type": mime_type,
                    "document_type": document_type,
                    "project_id": project_id,
                    "user_id": user_id,
                    "status": DocumentStatus.UPLOADED,
                    "uploaded_at": datetime.now().isoformat()
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def extract_text_from_pdf(self, file_path: str) -> Dict:
        """
        Extraire le texte d'un PDF
        
        Args:
            file_path: Chemin du fichier PDF
        
        Returns:
            Texte extrait et métadonnées
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                text_content = []
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    text_content.append({
                        "page": page_num + 1,
                        "text": text
                    })
                
                full_text = "\n\n".join([p["text"] for p in text_content])
                
                return {
                    "success": True,
                    "num_pages": num_pages,
                    "text": full_text,
                    "pages": text_content,
                    "word_count": len(full_text.split()),
                    "char_count": len(full_text)
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur extraction PDF: {str(e)}"
            }
    
    def extract_text_from_image(self, file_path: str) -> Dict:
        """
        Extraire le texte d'une image (OCR)
        
        Args:
            file_path: Chemin de l'image
        
        Returns:
            Texte extrait par OCR
        """
        try:
            image = Image.open(file_path)
            
            # OCR avec Tesseract
            text = pytesseract.image_to_string(image, lang='fra')
            
            return {
                "success": True,
                "text": text,
                "image_size": image.size,
                "image_format": image.format,
                "word_count": len(text.split()),
                "char_count": len(text)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur OCR image: {str(e)}"
            }
    
    async def analyze_document(
        self,
        document_id: int,
        file_path: str,
        document_type: str
    ) -> Dict:
        """
        Analyser automatiquement un document
        
        Args:
            document_id: ID du document
            file_path: Chemin du fichier
            document_type: Type de document
        
        Returns:
            Résultat de l'analyse
        """
        # Détecter extension
        file_extension = Path(file_path).suffix.lower()
        
        # Extraire texte selon type
        if file_extension == '.pdf':
            extraction = self.extract_text_from_pdf(file_path)
        elif file_extension in ['.jpg', '.jpeg', '.png', '.tiff']:
            extraction = self.extract_text_from_image(file_path)
        else:
            return {
                "success": False,
                "error": f"Type de fichier non supporté: {file_extension}"
            }
        
        if not extraction.get("success"):
            return extraction
        
        text = extraction["text"]
        
        # Analyse selon type de document
        analysis = self._analyze_by_type(text, document_type)
        
        return {
            "success": True,
            "document_id": document_id,
            "extraction": extraction,
            "analysis": analysis,
            "analyzed_at": datetime.now().isoformat()
        }
    
    def _analyze_by_type(self, text: str, document_type: str) -> Dict:
        """
        Analyse spécifique selon type de document
        
        Args:
            text: Texte extrait
            document_type: Type de document
        
        Returns:
            Analyse structurée
        """
        analysis = {
            "document_type": document_type,
            "key_information": {}
        }
        
        if document_type == DocumentType.PLU:
            # Détecter informations PLU
            analysis["key_information"] = {
                "zones_detected": self._detect_plu_zones(text),
                "constraints": self._detect_constraints(text),
                "cos_ces": self._detect_cos_ces(text)
            }
        
        elif document_type == DocumentType.DIAGNOSTIC:
            # Détecter diagnostics
            analysis["key_information"] = {
                "dpe": self._detect_dpe(text),
                "amiante": "amiante" in text.lower(),
                "plomb": "plomb" in text.lower(),
                "termites": "termites" in text.lower(),
                "risks": self._detect_risks(text)
            }
        
        elif document_type == DocumentType.CADASTRE:
            # Détecter références cadastrales
            analysis["key_information"] = {
                "parcels": self._detect_parcels(text),
                "surface": self._detect_surface(text)
            }
        
        return analysis
    
    def _detect_plu_zones(self, text: str) -> List[str]:
        """Détecter zones PLU dans texte"""
        zones = []
        common_zones = ["UA", "UB", "UC", "UD", "AU", "A", "N", "UE", "UF"]
        
        for zone in common_zones:
            if f"zone {zone}" in text.upper() or f"ZONE {zone}" in text.upper():
                zones.append(zone)
        
        return zones
    
    def _detect_constraints(self, text: str) -> List[str]:
        """Détecter contraintes urbanistiques"""
        constraints = []
        keywords = [
            "abf", "architecte des bâtiments de france",
            "monuments historiques", "site classé", "site inscrit",
            "périmètre de protection", "zone inondable",
            "zone protégée", "servitude"
        ]
        
        text_lower = text.lower()
        for keyword in keywords:
            if keyword in text_lower:
                constraints.append(keyword)
        
        return constraints
    
    def _detect_cos_ces(self, text: str) -> Dict:
        """Détecter COS et CES"""
        import re
        
        cos_pattern = r"cos[:\s]+([0-9.]+)"
        ces_pattern = r"ces[:\s]+([0-9.]+)"
        
        cos_match = re.search(cos_pattern, text.lower())
        ces_match = re.search(ces_pattern, text.lower())
        
        return {
            "cos": float(cos_match.group(1)) if cos_match else None,
            "ces": float(ces_match.group(1)) if ces_match else None
        }
    
    def _detect_dpe(self, text: str) -> Optional[str]:
        """Détecter classe DPE"""
        dpe_classes = ["A", "B", "C", "D", "E", "F", "G"]
        text_upper = text.upper()
        
        for classe in dpe_classes:
            if f"CLASSE {classe}" in text_upper or f"DPE {classe}" in text_upper:
                return classe
        
        return None
    
    def _detect_risks(self, text: str) -> List[str]:
        """Détecter risques dans diagnostic"""
        risks = []
        risk_keywords = {
            "structure": ["fissure", "affaissement", "tassement"],
            "humidite": ["humidité", "infiltration", "moisissure"],
            "electricite": ["installation électrique", "tableau électrique", "mise à la terre"],
            "isolation": ["isolation", "déperdition", "pont thermique"]
        }
        
        text_lower = text.lower()
        for risk_type, keywords in risk_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    risks.append(risk_type)
                    break
        
        return list(set(risks))
    
    def _detect_parcels(self, text: str) -> List[str]:
        """Détecter références cadastrales"""
        import re
        
        # Pattern: Section XX Parcelle YYYY
        pattern = r"section\s+([A-Z]+)\s+parcelle\s+([0-9]+)"
        matches = re.findall(pattern, text.upper())
        
        parcels = [f"{section} {parcel}" for section, parcel in matches]
        return parcels
    
    def _detect_surface(self, text: str) -> Optional[float]:
        """Détecter surface cadastrale"""
        import re
        
        # Pattern: XX m2 ou XX m²
        pattern = r"([0-9]+[,.]?[0-9]*)\s*m[²2]"
        matches = re.findall(pattern, text.lower())
        
        if matches:
            surface_str = matches[0].replace(",", ".")
            return float(surface_str)
        
        return None
    
    def delete_document(self, file_path: str) -> Dict:
        """
        Supprimer un document
        
        Args:
            file_path: Chemin du fichier
        
        Returns:
            Confirmation suppression
        """
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                return {
                    "success": True,
                    "message": "Document supprimé"
                }
            else:
                return {
                    "success": False,
                    "error": "Fichier introuvable"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_project_documents(self, project_id: int) -> Dict:
        """
        Lister tous les documents d'un projet
        
        Args:
            project_id: ID du projet
        
        Returns:
            Liste des documents avec métadonnées
        """
        try:
            project_folder = self.storage_path / str(project_id)
            
            if not project_folder.exists():
                return {
                    "success": True,
                    "documents": [],
                    "total": 0
                }
            
            documents = []
            for file_path in project_folder.iterdir():
                if file_path.is_file():
                    stat = file_path.stat()
                    documents.append({
                        "filename": file_path.name,
                        "file_path": str(file_path),
                        "file_size": stat.st_size,
                        "mime_type": mimetypes.guess_type(file_path.name)[0],
                        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat()
                    })
            
            return {
                "success": True,
                "documents": documents,
                "total": len(documents),
                "total_size": sum(d["file_size"] for d in documents)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Instance globale
document_service = DocumentService()
