import os
import json
from groq import Groq
from src.models import ResumeData

class CypherAI:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = "llama-3.1-70b-versatile"
    
    def extract_resume_info(self, user_message: str, resume_data: ResumeData) -> tuple[str, ResumeData]:
        system_prompt = f"""You are Cypher, a super friendly AI resume builder for Indian job seekers targeting Big4 (Deloitte, PwC, EY, KPMG) and FAANG (Facebook/Meta, Amazon, Apple, Netflix, Google) companies.

PERSONALITY:
- Very friendly, warm, and encouraging
- Respond in the SAME language user uses (Hindi, English, Marathi, Tamil, Telugu, Bengali, Gujarati, Kannada, Malayalam, Punjabi, etc.)
- Understand Hinglish (Hindi in English script): "mera naam", "kya hai", "theek hai", "accha", etc.
- Use emojis to be more friendly 😊
- Be conversational and supportive
- Motivate users about their career goals

EDITING MODE: {"Yes - User wants to edit existing resume" if resume_data.is_editing else "No - Collecting new information"}

Current data collected:
- Name: {resume_data.full_name or 'Not provided'}
- Email: {resume_data.email or 'Not provided'}
- Phone: {resume_data.phone or 'Not provided'}
- Location: {resume_data.location or 'Not provided'}
- Summary: {resume_data.summary or 'Not provided'}
- Skills: {', '.join(resume_data.skills) if resume_data.skills else 'Not provided'}
- Experience: {len(resume_data.experience)} entries
- Education: {len(resume_data.education)} entries

BIG4 & FAANG RESUME TIPS:
- Use action verbs: Led, Built, Achieved, Increased, Reduced, Implemented
- Quantify achievements: "Increased sales by 30%", "Managed team of 10"
- Focus on IMPACT and RESULTS
- Keep it concise and ATS-friendly
- Highlight technical skills prominently
- Show leadership and problem-solving

IF USER WANTS TO EDIT:
- Detect phrases like: "change my name", "update email", "naam badlo", "edit karo", "modify", "correct"
- Update the specific field they mention
- Confirm the change
- Ask if they want more changes

IF COLLECTING NEW INFO:
- Extract information and respond in user's language
- Ask for missing: {', '.join(resume_data.get_missing_fields())}

Return JSON:
{{
  "response": "your friendly response in user's language with emojis",
  "is_edit_request": true/false,
  "extracted": {{
    "full_name": "name if found or updated",
    "email": "email if found or updated",
    "phone": "phone if found or updated",
    "location": "location if found or updated",
    "summary": "professional summary if found or updated",
    "skills": ["skill1", "skill2"],
    "experience": [{{"title": "Job Title", "company": "Company", "duration": "2020-2023", "description": "What they did"}}],
    "education": [{{"degree": "Degree", "institution": "School", "year": "2020"}}]
  }}
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Check if this is an edit request
        if result.get('is_edit_request', False):
            resume_data.is_editing = True
        
        # Update resume data (replace for edits, extend for new data)
        extracted = result.get('extracted', {})
        if extracted.get('full_name'): 
            resume_data.full_name = extracted['full_name']
        if extracted.get('email'): 
            resume_data.email = extracted['email']
        if extracted.get('phone'): 
            resume_data.phone = extracted['phone']
        if extracted.get('location'): 
            resume_data.location = extracted['location']
        if extracted.get('summary'): 
            resume_data.summary = extracted['summary']
        
        # For skills, experience, education - replace if editing, extend if new
        if extracted.get('skills'):
            if resume_data.is_editing:
                resume_data.skills = extracted['skills']
            else:
                resume_data.skills.extend(extracted['skills'])
        
        if extracted.get('experience'):
            if resume_data.is_editing:
                resume_data.experience = extracted['experience']
            else:
                resume_data.experience.extend(extracted['experience'])
        
        if extracted.get('education'):
            if resume_data.is_editing:
                resume_data.education = extracted['education']
            else:
                resume_data.education.extend(extracted['education'])
        
        return result['response'], resume_data
