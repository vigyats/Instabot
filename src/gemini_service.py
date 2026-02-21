import os
import google.generativeai as genai
from src.models import ResumeData

class GeminiAI:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def extract_resume_info(self, user_message, current_data):
        try:
            # Update data first
            updated_data = self._parse_and_update(user_message, current_data)
            
            # Generate AI response
            prompt = f"""You are a friendly resume builder assistant. 

Current info collected:
Name: {updated_data.full_name or 'Not provided'}
Email: {updated_data.email or 'Not provided'}
Phone: {updated_data.phone or 'Not provided'}
Skills: {', '.join(updated_data.skills) if updated_data.skills else 'Not provided'}

User said: "{user_message}"

Ask for the next missing field in a friendly way. Keep it short (1-2 sentences)."""

            response = self.model.generate_content(prompt)
            ai_response = response.text
            
            return ai_response, updated_data
        except Exception as e:
            # Fallback response
            if not current_data.full_name:
                return "Great! What's your email address?", current_data
            elif not current_data.email:
                return "Perfect! What's your phone number?", current_data
            elif not current_data.phone:
                return "Got it! Tell me your skills (e.g., Python, JavaScript)", current_data
            else:
                return "Tell me about your work experience.", current_data
    
    def _parse_and_update(self, message, data):
        msg_lower = message.lower()
        
        # Extract name
        if not data.full_name and len(message.split()) <= 4 and '@' not in message:
            data.full_name = message.strip()
        
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
        if 'skill' in msg_lower or (data.full_name and data.email and data.phone and not data.skills):
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
