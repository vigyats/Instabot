import os
import google.generativeai as genai
from src.models import ResumeData
import re

class GeminiAI:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def extract_resume_info(self, user_message, current_data):
        # First, extract data using regex (fast and reliable)
        updated_data = self._smart_extract(user_message, current_data)
        
        # Check if user is asking for help
        help_keywords = ['help', 'what', 'how', 'why', 'explain', 'tell me', '?']
        is_question = any(word in user_message.lower() for word in help_keywords)
        
        # Only use AI for questions/help
        if is_question:
            try:
                prompt = f"User asks: {user_message}\n\nAnswer briefly and helpfully about resume building."
                response = self.model.generate_content(prompt)
                return response.text, updated_data
            except:
                return "I'm here to help you build your resume! Just answer the questions and I'll create an ATS-friendly resume for you.", updated_data
        
        # Generate next question based on missing fields
        missing = current_data.get_missing_fields()
        
        if not missing:
            return "Perfect! I have all the information. Generating your resume now...", updated_data
        
        next_field = missing[0]
        responses = {
            "full name": "Great! What's your email address?",
            "email": "Perfect! What's your phone number?",
            "phone number": "Awesome! List your top skills (e.g., Python, React, AWS)",
            "skills": "Excellent! Tell me about your work experience (company, role, duration)",
            "work experience": "Nice! What's your education background? (degree, university, year)",
            "education": "Amazing! Your resume is ready!"
        }
        
        return responses.get(next_field, "Tell me more about yourself"), updated_data
    
    def _smart_extract(self, message, data):
        # Extract email
        if not data.email:
            email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message)
            if email_match:
                data.email = email_match.group(0)
                return data
        
        # Extract phone
        if not data.phone:
            phone_match = re.search(r'[\d\s\+\-\(\)]{10,}', message)
            if phone_match:
                digits = re.sub(r'[^\d]', '', phone_match.group(0))
                if len(digits) >= 10:
                    data.phone = digits
                    return data
        
        # Extract name (if first field and no special chars)
        if not data.full_name and not re.search(r'[@\d]', message):
            words = message.strip().split()
            if 2 <= len(words) <= 5:
                data.full_name = message.strip()
                return data
        
        # Extract skills
        if not data.skills:
            skill_keywords = ['python', 'java', 'javascript', 'react', 'node', 'aws', 'sql', 'html', 'css', 'docker', 'kubernetes', 'git']
            if any(skill in message.lower() for skill in skill_keywords) or ',' in message:
                skills = [s.strip() for s in re.split(r'[,\n]', message) if len(s.strip()) > 1]
                if skills:
                    data.skills = skills[:15]
                    return data
        
        # Extract experience
        if not data.experience:
            exp_keywords = ['worked', 'developer', 'engineer', 'manager', 'company', 'years']
            if any(word in message.lower() for word in exp_keywords):
                data.experience.append({
                    'company': 'Company',
                    'position': 'Position',
                    'duration': '2020-2023',
                    'description': message
                })
                return data
        
        # Extract education
        if not data.education:
            edu_keywords = ['university', 'college', 'degree', 'bachelor', 'master', 'btech', 'mba']
            if any(word in message.lower() for word in edu_keywords):
                data.education.append({
                    'institution': 'University',
                    'degree': 'Degree',
                    'year': '2023',
                    'details': message
                })
                return data
        
        return data
