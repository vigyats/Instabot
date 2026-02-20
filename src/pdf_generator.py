from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from io import BytesIO
from src.models import ResumeData

class ATSResumePDF:
    """ATS-Friendly Resume Generator optimized for Big4 and FAANG companies"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        # Clean, professional style for ATS systems
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#000000'),
            spaceAfter=4,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=11,
            textColor=colors.HexColor('#000000'),
            spaceAfter=6,
            spaceBefore=10,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderPadding=0,
            leftIndent=0
        ))
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=12
        ))
    
    def generate(self, resume_data: ResumeData) -> BytesIO:
        """Generate Big4/FAANG optimized ATS-friendly resume"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter, 
            topMargin=0.5*inch, 
            bottomMargin=0.5*inch,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch
        )
        story = []
        
        # Name - Bold and prominent
        story.append(Paragraph(f"<b>{resume_data.full_name or 'N/A'}</b>", self.styles['CustomTitle']))
        
        # Contact Info - Single line, ATS-friendly
        contact_parts = []
        if resume_data.email:
            contact_parts.append(resume_data.email)
        if resume_data.phone:
            contact_parts.append(resume_data.phone)
        if resume_data.location:
            contact_parts.append(resume_data.location)
        
        if contact_parts:
            story.append(Paragraph(" | ".join(contact_parts), self.styles['ContactInfo']))
        
        story.append(Spacer(1, 0.1*inch))
        
        # Professional Summary - Critical for Big4/FAANG
        if resume_data.summary:
            story.append(Paragraph("<b>PROFESSIONAL SUMMARY</b>", self.styles['SectionHeader']))
            story.append(Paragraph(resume_data.summary, self.styles['Normal']))
            story.append(Spacer(1, 0.12*inch))
        
        # Skills - Prominent placement for ATS
        if resume_data.skills:
            story.append(Paragraph("<b>TECHNICAL SKILLS</b>", self.styles['SectionHeader']))
            skills_text = " • ".join(resume_data.skills)
            story.append(Paragraph(skills_text, self.styles['Normal']))
            story.append(Spacer(1, 0.12*inch))
        
        # Work Experience - Most important section
        if resume_data.experience:
            story.append(Paragraph("<b>PROFESSIONAL EXPERIENCE</b>", self.styles['SectionHeader']))
            for exp in resume_data.experience:
                # Job Title & Company - Bold
                title_company = f"<b>{exp.get('title', 'N/A')}</b> | {exp.get('company', 'N/A')}"
                story.append(Paragraph(title_company, self.styles['Normal']))
                
                # Duration
                story.append(Paragraph(f"<i>{exp.get('duration', 'N/A')}</i>", self.styles['Normal']))
                
                # Description with bullet points
                desc = exp.get('description', '')
                if desc:
                    # Add bullet if not present
                    if not desc.startswith('•'):
                        desc = f"• {desc}"
                    story.append(Paragraph(desc, self.styles['Normal']))
                
                story.append(Spacer(1, 0.1*inch))
        
        # Education
        if resume_data.education:
            story.append(Paragraph("<b>EDUCATION</b>", self.styles['SectionHeader']))
            for edu in resume_data.education:
                degree_school = f"<b>{edu.get('degree', 'N/A')}</b> | {edu.get('institution', 'N/A')}"
                story.append(Paragraph(degree_school, self.styles['Normal']))
                story.append(Paragraph(edu.get('year', 'N/A'), self.styles['Normal']))
                story.append(Spacer(1, 0.08*inch))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
