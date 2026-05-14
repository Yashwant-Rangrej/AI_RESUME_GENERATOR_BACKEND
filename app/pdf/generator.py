from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
import re

class ResumePDFGenerator:
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self.primary_color = colors.HexColor("#0f172a")  # Slate 900
        self.accent_color = colors.HexColor("#4f46e5")   # Indigo 600
        self._setup_custom_styles()

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        # Remove common non-ASCII characters that might not render in Helvetica
        # Replace common bullet symbols with standard ones or spaces
        text = text.replace("■", "•")
        # Remove other potentially problematic non-ASCII chars
        text = re.sub(r'[^\x00-\x7f]+', '', text)
        return text

    def _setup_custom_styles(self):
        # Header Style
        self.styles.add(ParagraphStyle(
            name='NameHeader',
            fontSize=26,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=4,
            fontName='Helvetica-Bold',
            textColor=self.primary_color
        ))
        
        # Contact Style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            fontSize=10,
            leading=12,
            alignment=TA_CENTER,
            spaceAfter=14,
            fontName='Helvetica',
            textColor=colors.grey
        ))
        
        # Section Header Style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            fontSize=13,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=14,
            spaceAfter=4,
            fontName='Helvetica-Bold',
            textColor=self.primary_color,
            textTransform='UPPERCASE',
            borderPadding=(0, 0, 2, 0),
            borderWidth=0,
            borderColor=self.primary_color
        ))
        
        # Job Title / Degree Style
        self.styles.add(ParagraphStyle(
            name='SubHeaderBold',
            fontSize=11,
            leading=13,
            fontName='Helvetica-Bold',
            textColor=self.primary_color
        ))

        # Company / Institution Style
        self.styles.add(ParagraphStyle(
            name='SubHeaderRegular',
            fontSize=11,
            leading=13,
            fontName='Helvetica',
            textColor=colors.black
        ))
        
        # Body Text Style
        self.styles.add(ParagraphStyle(
            name='BodyTextCustom',
            fontSize=10,
            leading=13,
            alignment=TA_LEFT,
            spaceAfter=4,
            fontName='Helvetica',
            textColor=colors.HexColor("#334155") # Slate 700
        ))

        # Date Style
        self.styles.add(ParagraphStyle(
            name='DateText',
            fontSize=10,
            leading=13,
            alignment=TA_RIGHT,
            fontName='Helvetica',
            textColor=colors.HexColor("#64748b") # Slate 500
        ))

    def _add_section_line(self, story):
        # A simple hack to draw a line: a Table with a bottom border
        line_table = Table([[""]], colWidths=[7.27 * inch])
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, self.primary_color),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 6))

    def generate(self, data: dict):
        # Set margins to be a bit wider for professional look
        doc = SimpleDocTemplate(
            self.output_path, 
            pagesize=A4, 
            rightMargin=0.5*inch, 
            leftMargin=0.5*inch, 
            topMargin=0.5*inch, 
            bottomMargin=0.5*inch
        )
        story = []

        # 1. Name and Contact
        story.append(Paragraph(self._clean_text(data['contact']['name']), self.styles['NameHeader']))
        
        links = []
        links.append(data['contact']['email'])
        links.append(data['contact']['phone'])
        if data['contact'].get('linkedin'):
            links.append(f"<a href='{data['contact']['linkedin']}' color='{self.accent_color.hexval()[2:]}'>LinkedIn</a>")
        if data['contact'].get('github'):
            links.append(f"<a href='{data['contact']['github']}' color='{self.accent_color.hexval()[2:]}'>GitHub</a>")
        
        contact_line = " | ".join(links)
        story.append(Paragraph(contact_line, self.styles['ContactInfo']))

        # 2. Summary
        if data.get('summary'):
            story.append(Paragraph("Summary", self.styles['SectionHeader']))
            self._add_section_line(story)
            story.append(Paragraph(self._clean_text(data['summary']), self.styles['BodyTextCustom']))

        # 3. Skills
        if data.get('skills'):
            story.append(Paragraph("Technical Skills", self.styles['SectionHeader']))
            self._add_section_line(story)
            skills_text = ", ".join(data['skills'])
            story.append(Paragraph(self._clean_text(skills_text), self.styles['BodyTextCustom']))

        # 4. Experience
        if data.get('experience'):
            story.append(Paragraph("Experience", self.styles['SectionHeader']))
            self._add_section_line(story)
            for exp in data['experience']:
                # Header Table for Job Title | Date
                title_para = Paragraph(f"<b>{self._clean_text(exp['job_title'])}</b>, {self._clean_text(exp['company'])}", self.styles['SubHeaderRegular'])
                date_para = Paragraph(f"{exp['start_date']} - {exp['end_date']}", self.styles['DateText'])
                
                header_table = Table([[title_para, date_para]], colWidths=[5.5*inch, 1.77*inch])
                header_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                story.append(header_table)
                
                if exp.get('description'):
                    story.append(Paragraph(self._clean_text(exp['description']), self.styles['BodyTextCustom']))
                story.append(Spacer(1, 8))

        # 5. Projects
        if data.get('projects'):
            story.append(Paragraph("Projects", self.styles['SectionHeader']))
            self._add_section_line(story)
            for proj in data['projects']:
                story.append(Paragraph(f"<b>{self._clean_text(proj['title'])}</b>", self.styles['SubHeaderBold']))
                story.append(Paragraph(self._clean_text(proj['description']), self.styles['BodyTextCustom']))
                if proj.get('technologies'):
                    story.append(Paragraph(f"<i>Technologies: {', '.join(proj['technologies'])}</i>", self.styles['BodyTextCustom']))
                story.append(Spacer(1, 8))

        # 6. Education
        if data.get('education'):
            story.append(Paragraph("Education", self.styles['SectionHeader']))
            self._add_section_line(story)
            for edu in data['education']:
                edu_para = Paragraph(f"<b>{self._clean_text(edu['degree'])}</b>, {self._clean_text(edu['institution'])}", self.styles['SubHeaderRegular'])
                year_para = Paragraph(edu['year'], self.styles['DateText'])
                
                edu_table = Table([[edu_para, year_para]], colWidths=[6.2*inch, 1.07*inch])
                edu_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ]))
                story.append(edu_table)
                story.append(Spacer(1, 4))

        doc.build(story)
        return self.output_path
