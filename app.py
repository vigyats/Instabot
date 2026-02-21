import os
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from src.models import ConversationState
from src.gemini_service import GeminiAI
from src.pdf_generator import ATSResumePDF

load_dotenv()

app = Flask(__name__)
state = ConversationState()
ai = GeminiAI()
pdf_gen = ATSResumePDF()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        user_id = f"web_{session_id}"
        resume_data = state.get_or_create(user_id)
        
        if message.lower() in ['reset', 'restart', 'start over']:
            state.clear(user_id)
            return jsonify({
                'response': "Hi! 😊 I'm Cypher, your AI resume builder. Let's create an ATS-friendly resume for Big4 & FAANG! What's your full name?",
                'pdf_ready': False
            })
        
        response_text, updated_data = ai.extract_resume_info(message, resume_data)
        
        if updated_data.is_complete():
            pdf_buffer = pdf_gen.generate(updated_data)
            pdf_dir = '/tmp'
            pdf_path = f"{pdf_dir}/{user_id}_resume.pdf"
            with open(pdf_path, 'wb') as f:
                f.write(pdf_buffer.read())
            
            return jsonify({
                'response': response_text + "\n\n✅ Your resume is ready!",
                'pdf_ready': True,
                'pdf_url': f'/download/{user_id}'
            })
        
        return jsonify({
            'response': response_text,
            'pdf_ready': False
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<user_id>')
def download_pdf(user_id):
    pdf_path = f"/tmp/{user_id}_resume.pdf"
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name='resume.pdf')
    return jsonify({'error': 'PDF not found'}), 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
