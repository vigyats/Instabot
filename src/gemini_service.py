import os
import google.generativeai as genai
from src.models import ResumeData

class GeminiAI:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
    
    def extract_resume_info(self, user_message, current_data):
        prompt = f"""You are Cypher, an AI resume builder. Extract resume information from user messages.

Current Resume Data:
- Name: {current_data.name or 'Not provided'}
- Email: {current_data.email or 'Not provided'}
- Phone: {current_data.phone or 'Not provided'}
- Skills: {', '.join(current_data.skills) if current_data.skills else 'Not provided'}
- Experience: {len(current_data.experience)} entries
- Education: {len(current_data.education)} entries

User Message: "{user_message}"

Instructions:
1. Extract any new information from the user message
2. Ask for the next missing field in a friendly way
3. If all fields are complete, say "Great! Your resume is complete."

Required fields: name, email, phone, skills (at least 3), experience (at least 1), education (at least 1)

Respond conversationally and ask for ONE thing at a time."""

        response = self.model.generate_content(prompt)
        ai_response = response.text
        
        # Update resume data based on user message
        updated_data = self._parse_and_update(user_message, current_data)
        
        return ai_response, updated_data
    
    def _parse_and_update(self, message, data):
        msg_lower = message.lower()
        
        # Extract name
        if not data.name and len(message.split()) <= 4 and '@' not in message:
            data.name = message.strip()
        
        # Extract email
        if '@' in message and '.' in message:
            words = message.split()
            for word in words:
                if '@' in word:
                    data.email = word.strip()
        
        # Extract phone
        if any(char.isdigit() for char in message) and not data.phone:
            import re
            phone = re.sub(r'[^\d+]', '', message)
            if len(phone) >= 10:
                data.phone = phone
        
        # Extract skills
        if 'skill' in msg_lower or (data.name and data.email and data.phone and not data.skills):
            skills = [s.strip() for s in message.replace(',', ' ').split() if len(s.strip()) > 2]
            if skills and len(skills) >= 2:
                data.skills = skills[:10]
        
        # Extract experience
        if any(word in msg_lower for word in ['work', 'job', 'company', 'experience', 'worked']):
            if not any(exp.get('company', '').lower() in msg_lower for exp in data.experience):
                data.experience.append({
                    'company': 'Company',
                    'position': 'Position',
                    'duration': '2020-2023',
                    'description': message
                })
        
        # Extract education
        if any(word in msg_lower for word in ['university', 'college', 'degree', 'bachelor', 'master', 'education']):
            if not data.education:
                data.education.append({
                    'institution': 'University',
                    'degree': 'Degree',
                    'year': '2020',
                    'details': message
                })
        
        return data
