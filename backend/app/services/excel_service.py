"""
Service de génération de Business Plan Excel
"""
from typing import Dict, Any, Optional
import xlsxwriter
from io import BytesIO
from datetime import datetime

class ExcelService:
    
    def generate_business_plan(
        self,
        project_data: Dict[str, Any],
        financial_data: Dict[str, Any]
    ) -> BytesIO:
        """
        Génère un Business Plan Excel professionnel
        
        Args:
            project_data: Données du projet
            financial_data: Données financières calculées
        
        Returns:
            BytesIO contenant le fichier Excel
        """
        
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        # Styles
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#0284c7',
            'font_color': 'white',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'bg_color': '#e0f2fe',
            'border': 1
        })
        
        currency_format = workbook.add_format({'num_format': '#,##0.00 €'})
        percent_format = workbook.add_format({'num_format': '0.00%'})
        
        # Onglet 1: Synthèse
        self._create_summary_sheet(workbook, project_data, financial_data, header_format, title_format)
        
        # Onglet 2: Hypothèses
        self._create_assumptions_sheet(workbook, financial_data, header_format, currency_format)
        
        # Onglet 3: Plan de financement
        self._create_financing_sheet(workbook, financial_data, header_format, currency_format)
        
        # Onglet 4: Compte de résultat prévisionnel
        self._create_income_statement_sheet(workbook, financial_data, header_format, currency_format)
        
        # Onglet 5: Indicateurs financiers
        self._create_indicators_sheet(workbook, financial_data, header_format, percent_format, currency_format)
        
        workbook.close()
        output.seek(0)
        
        return output
    
    def _create_summary_sheet(self, workbook, project_data, financial_data, header_format, title_format):
        """Crée l'onglet de synthèse"""
        worksheet = workbook.add_worksheet('Synthèse')
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 30)
        
        row = 0
        worksheet.merge_range(row, 0, row, 1, 'BUSINESS PLAN - ' + project_data.get('name', 'Projet'), title_format)
        
        row += 2
        worksheet.write(row, 0, 'Date de création:', header_format)
        worksheet.write(row, 1, datetime.now().strftime('%d/%m/%Y'))
        
        row += 1
        worksheet.write(row, 0, 'Adresse:', header_format)
        worksheet.write(row, 1, project_data.get('address', 'N/A'))
        
        row += 1
        worksheet.write(row, 0, 'Type de projet:', header_format)
        worksheet.write(row, 1, project_data.get('project_type', 'N/A'))
        
        # Indicateurs clés
        row += 3
        worksheet.merge_range(row, 0, row, 1, 'INDICATEURS CLÉS', title_format)
        
        indicators = [
            ('TRI (Taux de Rendement Interne)', financial_data.get('tri', 0)),
            ('LTV (Loan to Value)', financial_data.get('ltv', 0)),
            ('DSCR (Debt Service Coverage Ratio)', financial_data.get('dscr', 0)),
            ('ROI', financial_data.get('roi', 0))
        ]
        
        for label, value in indicators:
            row += 1
            worksheet.write(row, 0, label, header_format)
            worksheet.write(row, 1, f"{value:.2%}")
    
    def _create_assumptions_sheet(self, workbook, financial_data, header_format, currency_format):
        """Crée l'onglet des hypothèses"""
        worksheet = workbook.add_worksheet('Hypothèses')
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 20)
        
        row = 0
        worksheet.write(row, 0, 'Hypothèse', header_format)
        worksheet.write(row, 1, 'Valeur', header_format)
        
        assumptions = [
            ('Prix d\'achat', financial_data.get('purchase_price', 0)),
            ('Travaux', financial_data.get('renovation_budget', 0)),
            ('Frais de notaire', financial_data.get('notary_fees', 0)),
            ('Frais de garantie', financial_data.get('guarantee_fees', 0)),
            ('Durée du prêt (années)', financial_data.get('loan_duration', 20)),
            ('Taux d\'intérêt', financial_data.get('interest_rate', 0.04)),
        ]
        
        for label, value in assumptions:
            row += 1
            worksheet.write(row, 0, label)
            if isinstance(value, (int, float)) and label not in ['Durée du prêt (années)']:
                worksheet.write(row, 1, value, currency_format)
            else:
                worksheet.write(row, 1, value)
    
    def _create_financing_sheet(self, workbook, financial_data, header_format, currency_format):
        """Crée l'onglet du plan de financement"""
        worksheet = workbook.add_worksheet('Plan de financement')
        
        # À implémenter avec les formules Excel
        worksheet.write(0, 0, 'Plan de financement à développer', header_format)
    
    def _create_income_statement_sheet(self, workbook, financial_data, header_format, currency_format):
        """Crée l'onglet du compte de résultat"""
        worksheet = workbook.add_worksheet('Compte de résultat')
        
        # À implémenter avec les formules Excel
        worksheet.write(0, 0, 'Compte de résultat à développer', header_format)
    
    def _create_indicators_sheet(self, workbook, financial_data, header_format, percent_format, currency_format):
        """Crée l'onglet des indicateurs"""
        worksheet = workbook.add_worksheet('Indicateurs')
        worksheet.set_column('A:A', 35)
        worksheet.set_column('B:B', 20)
        
        row = 0
        worksheet.write(row, 0, 'Indicateur', header_format)
        worksheet.write(row, 1, 'Valeur', header_format)
        
        indicators = [
            ('TRI (Taux de Rendement Interne)', financial_data.get('tri', 0), percent_format),
            ('VAN (Valeur Actuelle Nette)', financial_data.get('van', 0), currency_format),
            ('LTV (Loan to Value)', financial_data.get('ltv', 0), percent_format),
            ('LTC (Loan to Cost)', financial_data.get('ltc', 0), percent_format),
            ('DSCR (Debt Service Coverage Ratio)', financial_data.get('dscr', 0), None),
            ('ROI (Return on Investment)', financial_data.get('roi', 0), percent_format),
        ]
        
        for label, value, fmt in indicators:
            row += 1
            worksheet.write(row, 0, label)
            if fmt:
                worksheet.write(row, 1, value, fmt)
            else:
                worksheet.write(row, 1, value)

# Instance globale
excel_service = ExcelService()
