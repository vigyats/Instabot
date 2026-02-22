import os
import google.generativeai as genai
from src.models import ResumeData
import json

class GeminiAI:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def extract_resume_info(self, user_message, current_data):
        try:
            missing = current_data.get_missing_fields()
            
            prompt = f"""You are Cypher, a friendly AI resume builder assistant.

Current resume data:
- Name: {current_data.full_name or 'Missing'}
- Email: {current_data.email or 'Missing'}
- Phone: {current_data.phone or 'Missing'}
- Skills: {', '.join(current_data.skills) if current_data.skills else 'Missing'}
- Experience: {'Provided' if current_data.experience else 'Missing'}
- Education: {'Provided' if current_data.education else 'Missing'}

User message: "{user_message}"

Task:
1. Understand if the user is providing information or asking a question
2. If asking a question, answer it helpfully
3. If providing info, acknowledge it and ask for the next missing field: {missing[0] if missing else 'nothing'}
4. Extract any resume data from the message and return it in JSON format

Respond in this format:
RESPONSE: [your conversational response]
DATA: {{"field": "value"}} or {{}}

Be friendly and conversational. Keep responses short."""

            response = self.model.generate_content(prompt)
            text = response.text
            
            # Parse response
            if 'RESPONSE:' in text and 'DATA:' in text:
                parts = text.split('DATA:')
                ai_response = parts[0].replace('RESPONSE:', '').strip()
                try:
                    data_str = parts[1].strip()
                    # Extract JSON from markdown code blocks if present
                    if '```' in data_str:
                        data_str = data_str.split('```')[1].replace('json', '').strip()
                    extracted = json.loads(data_str)
                    current_data = self._update_from_dict(extracted, current_data)
                except:
                    pass
            else:
                ai_response = text
            
            return ai_response, current_data
            
        except Exception as e:
            # Simple fallback
            missing = current_data.get_missing_fields()
            if missing:
                return f"Could you provide your {missing[0]}?", current_data
            return "Great! Your resume is ready.", current_data
    
    def _update_from_dict(self, data_dict, resume_data):
        if 'name' in data_dict or 'full_name' in data_dict:
            resume_data.full_name = data_dict.get('name') or data_dict.get('full_name')
        if 'email' in data_dict:
            resume_data.email = data_dict['email']
        if 'phone' in data_dict:
            resume_data.phone = data_dict['phone']
        if 'skills' in data_dict:
            resume_data.skills = data_dict['skills'] if isinstance(data_dict['skills'], list) else data_dict['skills'].split(',')
        if 'experience' in data_dict:
            resume_data.experience.append(data_dict['experience'])
        if 'education' in data_dict:
            resume_data.education.append(data_dict['education'])
        return resume_data
