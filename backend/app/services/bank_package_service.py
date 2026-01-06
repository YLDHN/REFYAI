"""
Service assemblage PDF dossier banque
Combine résumé projet + financier + documents en PDF unique
"""
from typing import List, Optional
import os
from datetime import datetime
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.document import Document


class BankPackageService:
    """Service génération PDF dossier banque"""
    
    def __init__(self):
        self.output_dir = "./exports/bank_packages"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_cover_page(
        self,
        project_name: str,
        project_type: str,
        total_investment: float,
        loan_requested: float
    ) -> bytes:
        """Génère page de garde PDF"""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Logo / Header
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width/2, height - 4*cm, "DOSSIER DE FINANCEMENT")
        
        # Projet
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, height - 6*cm, project_name)
        
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, height - 7*cm, f"Type : {project_type}")
        
        # Financements
        c.setFont("Helvetica-Bold", 14)
        c.drawString(4*cm, height - 10*cm, "SYNTHÈSE FINANCIÈRE")
        
        c.setFont("Helvetica", 12)
        c.drawString(5*cm, height - 11.5*cm, f"Investissement total : {total_investment:,.0f} €")
        c.drawString(5*cm, height - 12.5*cm, f"Financement demandé : {loan_requested:,.0f} €")
        c.drawString(5*cm, height - 13.5*cm, f"LTV : {(loan_requested/total_investment*100):.1f}%")
        
        # Footer
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(
            width/2,
            2*cm,
            f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}"
        )
        c.drawCentredString(
            width/2,
            1.5*cm,
            "REFY AI - Plateforme d'analyse immobilière"
        )
        
        c.showPage()
        c.save()
        
        buffer.seek(0)
        return buffer.read()
    
    def generate_summary_page(
        self,
        project_data: dict
    ) -> bytes:
        """Génère page résumé projet"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph("RÉSUMÉ EXÉCUTIF", title_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Informations projet
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12
        )
        
        story.append(Paragraph("📍 LOCALISATION", heading_style))
        location_data = [
            ["Adresse", project_data.get("address", "N/A")],
            ["Ville", project_data.get("city", "N/A")],
            ["Code postal", project_data.get("zip_code", "N/A")],
            ["Surface", f"{project_data.get('surface', 0)} m²"]
        ]
        
        location_table = Table(location_data, colWidths=[5*cm, 10*cm])
        location_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(location_table)
        story.append(Spacer(1, 1*cm))
        
        # Indicateurs financiers
        story.append(Paragraph("💰 INDICATEURS CLÉS", heading_style))
        
        financial_data = [
            ["Prix acquisition", f"{project_data.get('acquisition_price', 0):,.0f} €"],
            ["Budget travaux", f"{project_data.get('capex_budget', 0):,.0f} €"],
            ["Investissement total", f"{project_data.get('total_investment', 0):,.0f} €"],
            ["Apport", f"{project_data.get('equity', 0):,.0f} €"],
            ["Prêt demandé", f"{project_data.get('loan_amount', 0):,.0f} €"],
            ["LTV", f"{project_data.get('ltv', 0)*100:.1f}%"],
            ["TRI attendu", f"{project_data.get('tri', 0)*100:.1f}%"],
            ["VAN", f"{project_data.get('van', 0):,.0f} €"]
        ]
        
        financial_table = Table(financial_data, colWidths=[5*cm, 10*cm])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(financial_table)
        
        doc.build(story)
        buffer.seek(0)
        return buffer.read()
    
    async def assemble_bank_package(
        self,
        project_id: int,
        db: Session,
        include_documents: bool = True
    ) -> dict:
        """
        Assemble dossier banque complet en PDF
        
        Args:
            project_id: ID projet
            db: Session SQLAlchemy
            include_documents: Inclure documents uploadés
        
        Returns:
            Dict avec chemin PDF + métadonnées
        """
        
        # Récupérer projet
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {"error": "Projet introuvable"}
        
        # Préparer données
        project_data = {
            "address": project.address or "N/A",
            "city": project.city or "N/A",
            "zip_code": project.zip_code or "N/A",
            "surface": project.surface or 0,
            "acquisition_price": project.purchase_price or 0,
            "capex_budget": project.estimated_budget or 0,
            "total_investment": (project.purchase_price or 0) + (project.estimated_budget or 0),
            "equity": project.equity or 0,
            "loan_amount": project.loan_amount or 0,
            "ltv": project.ltv or 0,
            "tri": project.tri or 0,
            "van": project.van or 0
        }
        
        # Créer merger PDF
        merger = PdfMerger()
        
        # === 1. PAGE DE GARDE ===
        cover_pdf = self.generate_cover_page(
            project_name=project.name or f"Projet #{project_id}",
            project_type=project.typologie or "N/A",
            total_investment=project_data["total_investment"],
            loan_requested=project_data["loan_amount"]
        )
        merger.append(io.BytesIO(cover_pdf))
        
        # === 2. RÉSUMÉ EXÉCUTIF ===
        summary_pdf = self.generate_summary_page(project_data)
        merger.append(io.BytesIO(summary_pdf))
        
        # === 3. DOCUMENTS PROJET ===
        if include_documents:
            documents = db.query(Document).filter(
                Document.project_id == project_id
            ).all()
            
            # Priorité documents (critiques d'abord)
            priority_order = {
                "titre_propriete": 1,
                "business_plan": 2,
                "permis_construire": 3,
                "dpe": 4,
                "budget_travaux": 5
            }
            
            docs_sorted = sorted(
                documents,
                key=lambda d: priority_order.get(d.document_type, 99)
            )
            
            for doc in docs_sorted:
                # Vérifier si fichier existe et est PDF
                if doc.file_path and os.path.exists(doc.file_path):
                    if doc.file_path.lower().endswith('.pdf'):
                        try:
                            merger.append(doc.file_path)
                        except Exception as e:
                            print(f"⚠️ Erreur ajout {doc.file_name}: {e}")
        
        # === 4. SAUVEGARDER PDF FINAL ===
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dossier_banque_projet_{project_id}_{timestamp}.pdf"
        output_path = os.path.join(self.output_dir, filename)
        
        with open(output_path, "wb") as output_file:
            merger.write(output_file)
        
        merger.close()
        
        # Taille fichier
        file_size = os.path.getsize(output_path)
        
        return {
            "success": True,
            "project_id": project_id,
            "filename": filename,
            "file_path": output_path,
            "file_size_mb": round(file_size / (1024 * 1024), 2),
            "pages_count": len(merger.pages) if hasattr(merger, 'pages') else "N/A",
            "generated_at": datetime.now().isoformat(),
            "sections": {
                "cover": True,
                "summary": True,
                "documents": include_documents,
                "documents_count": len(documents) if include_documents else 0
            }
        }


# Instance globale
bank_package_service = BankPackageService()
