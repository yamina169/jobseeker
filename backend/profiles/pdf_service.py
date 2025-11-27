# profiles/pdf_service.py
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configure les styles personnalisés modernes"""
        # Style pour le titre principal
        if 'ModernTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='ModernTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1e293b'),
                spaceAfter=12,
                alignment=1,
                fontName='Helvetica-Bold'
            ))
        
        # Style pour le sous-titre
        if 'ModernSubtitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='ModernSubtitle',
                parent=self.styles['Normal'],
                fontSize=14,
                textColor=colors.HexColor('#64748b'),
                spaceAfter=20,
                alignment=1,
                fontName='Helvetica'
            ))
        
        # Style pour les sections
        if 'SectionHeader' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SectionHeader',
                parent=self.styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#1e293b'),
                spaceAfter=12,
                spaceBefore=20,
                fontName='Helvetica-Bold',
                borderPadding=(0, 0, 6, 0),
                borderColor=colors.HexColor('#2563eb'),
                borderWidth=0,
                leftIndent=0
            ))
        
        # Style pour les postes/formations
        if 'ItemTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='ItemTitle',
                parent=self.styles['Heading3'],
                fontSize=12,
                textColor=colors.HexColor('#1e293b'),
                spaceAfter=4,
                fontName='Helvetica-Bold'
            ))
        
        # Style pour les entreprises/institutions
        if 'ItemSubtitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='ItemSubtitle',
                parent=self.styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#475569'),
                spaceAfter=4,
                fontName='Helvetica-Bold'
            ))
        
        # Style pour les dates
        if 'DateStyle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='DateStyle',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#64748b'),
                spaceAfter=6,
                fontName='Helvetica-Oblique'
            ))
        
        # Style pour le texte principal
        if 'BodyText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='BodyText',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#374151'),
                spaceAfter=8,
                fontName='Helvetica',
                leading=12
            ))
        
        # Style pour les compétences
        if 'SkillStyle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SkillStyle',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#374151'),
                spaceAfter=2,
                leftIndent=0,
                fontName='Helvetica'
            ))

    def generate_cv_pdf(self, user_data):
        """Génère un CV PDF moderne et professionnel"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4, 
            topMargin=1.5*cm, 
            bottomMargin=1.5*cm,
            leftMargin=1.5*cm,
            rightMargin=1.5*cm
        )
        story = []
        
        # En-tête moderne
        story.extend(self.create_modern_header(user_data))
        story.append(Spacer(1, 15))
        
        # Ligne de séparation
        story.append(HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor('#e2e8f0'),
            spaceAfter=15
        ))
        
        # Sections dans un ordre logique
        sections = [
            ('personal_info', self.create_profile_summary, "Profil"),
            ('experiences', self.create_experiences, "Expériences Professionnelles"),
            ('formations', self.create_education, "Formation"),
            ('skills', self.create_skills, "Compétences"),
            ('projects', self.create_projects, "Projets"),
            ('certifications', self.create_certifications, "Certifications"),
            ('languages', self.create_languages, "Langues")
        ]
        
        for section_key, section_method, section_title in sections:
            if user_data.get(section_key):
                story.extend(section_method(user_data[section_key], section_title))
                story.append(Spacer(1, 10))
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    def create_modern_header(self, user_data):
        """Crée un en-tête moderne avec mise en page améliorée"""
        elements = []
        user = user_data['user']
        personal_info = user_data.get('personal_info', {})
        
        # Nom complet en grand
        full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        if full_name:
            elements.append(Paragraph(full_name.upper(), self.styles['ModernTitle']))
        
        # Titre professionnel s'il existe
        if personal_info.get('title') or personal_info.get('professional_summary'):
            title = personal_info.get('title', 'Développeur Professionnel')
            elements.append(Paragraph(title, self.styles['ModernSubtitle']))
        
        # Grille de contact moderne
        contact_data = []
        
        # Email
        if user.get('email'):
            contact_data.append(['📧', user['email']])
        
        # Téléphone
        if personal_info.get('phone'):
            contact_data.append(['📱', personal_info['phone']])
        
        # Localisation
        location_parts = []
        if personal_info.get('city'):
            location_parts.append(personal_info['city'])
        if personal_info.get('country'):
            location_parts.append(personal_info['country'])
        if location_parts:
            contact_data.append(['📍', ', '.join(location_parts)])
        
        # Liens professionnels
        if personal_info.get('linkedin_url'):
            contact_data.append(['💼', f"LinkedIn: {personal_info['linkedin_url']}"])
        if personal_info.get('github_url'):
            contact_data.append(['⚡', f"GitHub: {personal_info['github_url']}"])
        if personal_info.get('portfolio_url'):
            contact_data.append(['🌐', f"Portfolio: {personal_info['portfolio_url']}"])
        
        if contact_data:
            # Créer un tableau pour les contacts
            contact_table = Table(contact_data, colWidths=[0.5*cm, None])
            contact_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#64748b')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (0, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, -1), 2),
                ('LEFTPADDING', (1, 0), (1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ]))
            elements.append(contact_table)
        
        return elements

    def create_profile_summary(self, personal_info, title="Profil"):
        """Crée une section profil avec résumé professionnel"""
        elements = []
        elements.append(Paragraph(title, self.styles['SectionHeader']))
        
        # Résumé professionnel
        if personal_info.get('professional_summary'):
            elements.append(Paragraph(
                personal_info['professional_summary'], 
                self.styles['BodyText']
            ))
        else:
            # Informations personnelles de base
            info_lines = []
            if personal_info.get('date_of_birth'):
                try:
                    birth_date = personal_info['date_of_birth']
                    if isinstance(birth_date, str):
                        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
                    age = datetime.now().year - birth_date.year
                    info_lines.append(f"<b>Âge:</b> {age} ans")
                except:
                    pass
            
            if personal_info.get('nationality'):
                info_lines.append(f"<b>Nationalité:</b> {personal_info['nationality']}")
            
            if info_lines:
                elements.append(Paragraph(" • ".join(info_lines), self.styles['BodyText']))
        
        elements.append(Spacer(1, 15))
        return elements

    def create_experiences(self, experiences, title="Expériences Professionnelles"):
        """Crée une section expériences avec mise en page moderne"""
        elements = []
        elements.append(Paragraph(title, self.styles['SectionHeader']))
        
        for exp in experiences:
            # Ligne 1: Titre et entreprise
            title_text = f"<b>{exp.get('title', 'Poste non spécifié')}</b>"
            company_text = f"<font color='#2563eb'>@{exp.get('company', 'Entreprise non spécifiée')}</font>"
            elements.append(Paragraph(f"{title_text} • {company_text}", self.styles['ItemTitle']))
            
            # Ligne 2: Période
            start_date = self.format_date(exp.get('start_date'))
            end_date = "<b>Présent</b>" if not exp.get('end_date') else self.format_date(exp.get('end_date'))
            period_text = f"{start_date} - {end_date}"
            elements.append(Paragraph(period_text, self.styles['DateStyle']))
            
            # Ligne 3: Description avec puces si nécessaire
            if exp.get('description'):
                description = self.format_description(exp['description'])
                elements.append(Paragraph(description, self.styles['BodyText']))
            
            elements.append(Spacer(1, 12))
        
        return elements

    def create_education(self, formations, title="Formation"):
        """Crée une section formation améliorée"""
        elements = []
        elements.append(Paragraph(title, self.styles['SectionHeader']))
        
        for formation in formations:
            # Diplôme et institution
            degree_text = f"<b>{formation.get('degree', 'Diplôme non spécifié')}</b>"
            institution_text = f"<font color='#2563eb'>{formation.get('institution', 'Établissement non spécifié')}</font>"
            elements.append(Paragraph(f"{degree_text} • {institution_text}", self.styles['ItemTitle']))
            
            # Période
            start_date = self.format_date(formation.get('start_date'))
            end_date = "<b>En cours</b>" if not formation.get('end_date') else self.format_date(formation.get('end_date'))
            period_text = f"{start_date} - {end_date}"
            elements.append(Paragraph(period_text, self.styles['DateStyle']))
            
            # Description
            if formation.get('description'):
                description = self.format_description(formation['description'])
                elements.append(Paragraph(description, self.styles['BodyText']))
            
            elements.append(Spacer(1, 12))
        
        return elements

    def create_skills(self, skills, title="Compétences"):
        """Crée une section compétences organisée par catégories"""
        elements = []
        elements.append(Paragraph(title, self.styles['SectionHeader']))
        
        # Grouper les compétences par niveau
        skill_groups = {}
        for skill in skills:
            level = skill.get('level', 'Autres')
            if level not in skill_groups:
                skill_groups[level] = []
            skill_groups[level].append(skill.get('name', ''))
        
        # Afficher les compétences par groupe
        skill_texts = []
        for level, skill_list in skill_groups.items():
            level_display = {
                'Expert': '🟢 Expert',
                'Intermediate': '🟡 Intermédiaire', 
                'Beginner': '🔴 Débutant'
            }.get(level, f'⚪ {level}')
            
            skill_texts.append(
                f"<b>{level_display}:</b> {', '.join(skill_list)}"
            )
        
        if skill_texts:
            elements.append(Paragraph('<br/>'.join(skill_texts), self.styles['SkillStyle']))
        
        elements.append(Spacer(1, 15))
        return elements

    def create_languages(self, languages, title="Langues"):
        """Crée une section langues avec indicateurs visuels"""
        elements = []
        elements.append(Paragraph(title, self.styles['SectionHeader']))
        
        lang_data = []
        for lang in languages:
            name = lang.get('name', '')
            level = lang.get('level', '')
            
            # Icônes pour les niveaux
            level_icon = {
                'Native': '🔴',
                'Fluent': '🟢', 
                'Intermediate': '🟡',
                'Beginner': '⚪'
            }.get(level, '⚪')
            
            lang_data.append([f"{level_icon} {name}", level])
        
        if lang_data:
            lang_table = Table(lang_data, colWidths=[4*cm, 3*cm])
            lang_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(lang_table)
        
        elements.append(Spacer(1, 15))
        return elements

    def create_projects(self, projects, title="Projets"):
        """Crée une section projets détaillée"""
        elements = []
        elements.append(Paragraph(title, self.styles['SectionHeader']))
        
        for project in projects:
            # Titre du projet
            elements.append(Paragraph(
                f"<b>🚀 {project.get('title', 'Projet sans titre')}</b>", 
                self.styles['ItemTitle']
            ))
            
            # Période
            start_date = self.format_date(project.get('start_date'))
            end_date = "<b>En cours</b>" if not project.get('end_date') else self.format_date(project.get('end_date'))
            elements.append(Paragraph(f"{start_date} - {end_date}", self.styles['DateStyle']))
            
            # Technologies
            if project.get('technologies'):
                elements.append(Paragraph(
                    f"<b>Technologies:</b> {project['technologies']}", 
                    self.styles['BodyText']
                ))
            
            # Description
            if project.get('description'):
                description = self.format_description(project['description'])
                elements.append(Paragraph(description, self.styles['BodyText']))
            
            # Liens
            links = []
            if project.get('project_url'):
                links.append(f"<b>Lien:</b> {project['project_url']}")
            if project.get('github_url'):
                links.append(f"<b>GitHub:</b> {project['github_url']}")
            
            if links:
                elements.append(Paragraph(" • ".join(links), self.styles['BodyText']))
            
            elements.append(Spacer(1, 12))
        
        return elements

    def create_certifications(self, certifications, title="Certifications"):
        """Crée une section certifications professionnelle"""
        elements = []
        elements.append(Paragraph(title, self.styles['SectionHeader']))
        
        for cert in certifications:
            # Nom et organisation
            cert_text = f"<b>🏆 {cert.get('name', 'Certification sans nom')}</b>"
            org_text = f"<font color='#2563eb'>{cert.get('issuing_organization', 'Organisme inconnu')}</font>"
            elements.append(Paragraph(f"{cert_text} • {org_text}", self.styles['ItemTitle']))
            
            # Dates
            issue_date = self.format_date(cert.get('issue_date'))
            date_text = f"<b>Délivrée:</b> {issue_date}"
            if cert.get('expiration_date'):
                exp_date = self.format_date(cert['expiration_date'])
                date_text += f" • <b>Expire:</b> {exp_date}"
            
            elements.append(Paragraph(date_text, self.styles['BodyText']))
            
            # ID de credential
            if cert.get('credential_id'):
                elements.append(Paragraph(
                    f"<b>ID:</b> {cert['credential_id']}", 
                    self.styles['BodyText']
                ))
            
            elements.append(Spacer(1, 10))
        
        return elements

    def format_date(self, date_string):
        """Formate une date en français"""
        if not date_string:
            return ""
        try:
            if isinstance(date_string, str):
                date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()
                return date_obj.strftime('%m/%Y')
            return date_string
        except:
            return date_string

    def format_description(self, description):
        """Formate la description avec des puces si nécessaire"""
        if not description:
            return ""
        
        # Si la description contient des retours à la ligne, on les transforme en puces
        if '\n' in description:
            lines = description.split('\n')
            formatted_lines = []
            for line in lines:
                line = line.strip()
                if line:
                    formatted_lines.append(f"• {line}")
            return '<br/>'.join(formatted_lines)
        
        return description

    def create_two_column_layout(self, left_content, right_content):
        """Crée une mise en page sur deux colonnes"""
        data = [[left_content, right_content]]
        table = Table(data, colWidths=[8*cm, 8*cm])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        return table