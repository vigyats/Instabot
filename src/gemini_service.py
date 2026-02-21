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
            # Fallback response based on what's missing
            if not current_data.full_name:
                return "What's your full name?", current_data
            elif not current_data.email:
                return "What's your email address?", current_data
            elif not current_data.phone:
                return "What's your phone number?", current_data
            elif not current_data.skills:
                return "List your skills (e.g., Python, JavaScript, React)", current_data
            elif not current_data.experience:
                return "Tell me about your work experience", current_data
            elif not current_data.education:
                return "What's your education background?", current_data
            else:
                return "Great! Your resume is ready.", current_data
    
    def _parse_and_update(self, message, data):
        msg_lower = message.lower()
        
        # Extract name (if no @ and no digits, likely a name)
        if not data.full_name and '@' not in message and not any(char.isdigit() for char in message):
            if len(message.split()) <= 5:
                data.full_name = message.strip()
                return data
        
        # Extract email
        if '@' in message:
            import re
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', message)
            if email_match:
                data.email = email_match.group(0)
                return data
        
        # Extract phone
        if any(char.isdigit() for char in message) and not data.phone:
            import re
            digits = re.sub(r'[^\d]', '', message)
            if len(digits) >= 10:
                data.phone = digits
                return data
        
        # Extract skills (comma separated or space separated)
        if not data.skills and (any(word in msg_lower for word in ['python', 'java', 'javascript', 'react', 'node', 'aws', 'sql']) or ',' in message):
            skills = [s.strip() for s in message.replace(',', ' ').split() if len(s.strip()) > 1]
            if skills:
                data.skills = skills[:15]
                return data
        
        # Extract experience
        if not data.experience and any(word in msg_lower for word in ['worked', 'work', 'job', 'company', 'developer', 'engineer', 'manager']):
            data.experience.append({
                'company': 'Company Name',
                'position': 'Position',
                'duration': '2020-2023',
                'description': message
            })
            return data
        
        # Extract education
        if not data.education and any(word in msg_lower for word in ['university', 'college', 'degree', 'bachelor', 'master', 'btech', 'mtech', 'bsc', 'msc']):
            data.education.append({
                'institution': 'University Name',
                'degree': 'Degree',
                'year': '2020',
                'details': message
            })
            return data
        
        return data
