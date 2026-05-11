from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

class ResumePDFGenerator:
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        # Header Style
        self.styles.add(ParagraphStyle(
            name='NameHeader',
            fontSize=24,
            leading=28,
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        # Contact Style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            fontSize=10,
            leading=12,
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName='Helvetica'
        ))
        
        # Section Header Style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            fontSize=14,
            leading=18,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=6,
            fontName='Helvetica-Bold',
            borderPadding=(0, 0, 1, 0),
            borderWidth=0,
            borderColor=colors.black
        ))
        
        # Body Text Style
        self.styles.add(ParagraphStyle(
            name='BodyTextCustom',
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName='Helvetica'
        ))

    def generate(self, data: dict):
        doc = SimpleDocTemplate(self.output_path, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
        story = []

        # 1. Name and Contact
        story.append(Paragraph(data['contact']['name'], self.styles['NameHeader']))
        
        contact_line = f"{data['contact']['email']} | {data['contact']['phone']}"
        if data['contact'].get('linkedin'):
            contact_line += f" | <a href='{data['contact']['linkedin']}' color='blue'>LinkedIn</a>"
        if data['contact'].get('github'):
            contact_line += f" | <a href='{data['contact']['github']}' color='blue'>GitHub</a>"
        
        story.append(Paragraph(contact_line, self.styles['ContactInfo']))

        # 2. Summary
        if data.get('summary'):
            story.append(Paragraph("SUMMARY", self.styles['SectionHeader']))
            story.append(Paragraph(data['summary'], self.styles['BodyTextCustom']))

        # 3. Skills
        if data.get('skills'):
            story.append(Paragraph("TECHNICAL SKILLS", self.styles['SectionHeader']))
            skills_text = ", ".join(data['skills'])
            story.append(Paragraph(skills_text, self.styles['BodyTextCustom']))

        # 4. Experience
        if data.get('experience'):
            story.append(Paragraph("EXPERIENCE", self.styles['SectionHeader']))
            for exp in data['experience']:
                exp_header = f"<b>{exp['job_title']}</b> | {exp['company']}"
                story.append(Paragraph(exp_header, self.styles['BodyTextCustom']))
                story.append(Paragraph(f"<i>{exp['start_date']} - {exp['end_date']}</i>", self.styles['BodyTextCustom']))
                story.append(Paragraph(exp['description'], self.styles['BodyTextCustom']))
                story.append(Spacer(1, 6))

        # 5. Projects
        if data.get('projects'):
            story.append(Paragraph("PROJECTS", self.styles['SectionHeader']))
            for proj in data['projects']:
                proj_header = f"<b>{proj['title']}</b>"
                story.append(Paragraph(proj_header, self.styles['BodyTextCustom']))
                story.append(Paragraph(proj['description'], self.styles['BodyTextCustom']))
                story.append(Paragraph(f"<i>Technologies: {', '.join(proj['technologies'])}</i>", self.styles['BodyTextCustom']))
                story.append(Spacer(1, 6))

        # 6. Education
        if data.get('education'):
            story.append(Paragraph("EDUCATION", self.styles['SectionHeader']))
            for edu in data['education']:
                edu_text = f"<b>{edu['degree']}</b>, {edu['institution']} ({edu['year']})"
                story.append(Paragraph(edu_text, self.styles['BodyTextCustom']))

        doc.build(story)
        return self.output_path
