import os
from flask import Flask, request, send_file, jsonify
from dotenv import load_dotenv
from src.models import ConversationState
from src.ai_service import CypherAI
from src.pdf_generator import ATSResumePDF
from src.instagram_service import InstagramService

load_dotenv()

app = Flask(__name__)
state = ConversationState()
ai = CypherAI()
pdf_gen = ATSResumePDF()
instagram = InstagramService()

@app.route('/')
def home():
    return jsonify({
        "bot": "Cypher AI Resume Builder",
        "status": "running",
        "platform": "Instagram",
        "webhook": "/instagram"
    })

@app.route('/instagram', methods=['GET', 'POST'])
def instagram_webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        return instagram.verify_webhook(mode, token, challenge)
    
    data = request.json
    if data.get('object') == 'instagram':
        for entry in data.get('entry', []):
            for messaging_event in entry.get('messaging', []):
                sender_id = messaging_event['sender']['id']
                
                if 'message' in messaging_event:
                    message_text = messaging_event['message'].get('text', '')
                    
                    if not message_text:
                        continue
                    
                    user_id = f"ig_{sender_id}"
                    resume_data = state.get_or_create(user_id)
                    
                    if message_text.lower() in ['reset', 'restart', 'start over', 'रीसेट', 'पुनः सुरू करा']:
                        state.clear(user_id)
                        instagram.send_message(sender_id, "Hi! 😊 I'm Cypher, your friendly AI resume builder! Let's create an ATS-friendly resume for Big4 & FAANG companies! \n\nनमस्ते! 🙏 मैं Cypher हूँ! \n\nWhat's your full name? / आपका नाम क्या है?")
                        continue
                    
                    try:
                        response_text, updated_data = ai.extract_resume_info(message_text, resume_data)
                        
                        # Check if resume was already generated and user wants to edit
                        if resume_data.pdf_generated and not resume_data.is_editing:
                            edit_keywords = ['change', 'edit', 'update', 'modify', 'correct', 'badlo', 'sudhar', 'theek karo']
                            if any(keyword in message_text.lower() for keyword in edit_keywords):
                                updated_data.is_editing = True
                        
                        if updated_data.is_complete():
                            pdf_buffer = pdf_gen.generate(updated_data)
                            pdf_path = f"/tmp/{user_id}_resume.pdf"
                            with open(pdf_path, 'wb') as f:
                                f.write(pdf_buffer.read())
                            
                            if updated_data.is_editing:
                                success_msg = response_text + "\n\n✅ Updated resume ready! / अपडेट किया गया resume तैयार है! 🎉\n\n📝 Changes applied successfully!\n\nType 'edit' anytime to make more changes!"
                            else:
                                success_msg = response_text + "\n\n✅ Your Big4/FAANG optimized resume is ready! \n🎉 आपका resume तैयार है!\n\n📌 ATS-Friendly Format\n🎯 Optimized for Big4 & FAANG\n✨ Professional & Clean Design\n\nWant to edit something? Just say 'change my email' or 'naam badlo'!"
                            
                            instagram.send_message(sender_id, success_msg)
                            updated_data.pdf_generated = True
                            updated_data.is_editing = False
                        else:
                            instagram.send_message(sender_id, response_text)
                    
                    except Exception as e:
                        instagram.send_message(sender_id, "Sorry, I encountered an error. Please try again or type 'reset' to start over.")
    
    return jsonify({"status": "ok"})

@app.route('/pdf/<user_id>')
def get_pdf(user_id):
    pdf_path = f"/tmp/{user_id}_resume.pdf"
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name='resume.pdf')
    return jsonify({"error": "PDF not found"}), 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
