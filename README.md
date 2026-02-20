# 🤖 Cypher - AI Resume Builder Bot

Free AI-powered chatbot for WhatsApp & Instagram that creates ATS-friendly resume PDFs.

## ✨ Features

- 💬 Conversational AI using Groq (free LLM)
- 📱 WhatsApp integration via Twilio
- 📸 Instagram DM integration via Meta Graph API
- 📄 ATS-friendly PDF generation
- 🆓 100% Free deployment on Render

## 🚀 Quick Setup

### 1. Get Free API Keys

#### Groq API (Free LLM)
1. Go to https://console.groq.com/
2. Sign up with Google/GitHub
3. Go to API Keys → Create API Key
4. Copy the key

#### Twilio (WhatsApp)
1. Go to https://www.twilio.com/try-twilio
2. Sign up (free trial with $15 credit)
3. Get your Account SID & Auth Token from dashboard
4. Go to Messaging → Try it out → Send a WhatsApp message
5. Use the Twilio Sandbox number: `whatsapp:+14155238886`

#### Instagram (Optional)
1. Go to https://developers.facebook.com/
2. Create an app → Business → Messenger
3. Get Page Access Token
4. Set up webhooks

### 2. Deploy on Render (Free)

1. **Push to GitHub:**
   ```bash
   cd cypher-bot
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com/
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render will auto-detect `render.yaml`
   - Add environment variables:
     - `GROQ_API_KEY`
     - `TWILIO_ACCOUNT_SID`
     - `TWILIO_AUTH_TOKEN`
     - `TWILIO_WHATSAPP_NUMBER` (e.g., `whatsapp:+14155238886`)
     - `INSTAGRAM_ACCESS_TOKEN` (optional)
     - `INSTAGRAM_VERIFY_TOKEN` (optional)
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment

3. **Get Your Webhook URL:**
   - After deployment, copy your Render URL (e.g., `https://cypher-bot.onrender.com`)

### 3. Configure Webhooks

#### Twilio WhatsApp:
1. Go to Twilio Console → Messaging → Settings → WhatsApp Sandbox
2. Set "When a message comes in" to: `https://YOUR_RENDER_URL/whatsapp`
3. Save

#### Instagram (Optional):
1. Go to Facebook Developers → Your App → Messenger → Settings
2. Set Callback URL: `https://YOUR_RENDER_URL/instagram`
3. Set Verify Token: (same as `INSTAGRAM_VERIFY_TOKEN` in env)
4. Subscribe to `messages` webhook

## 📱 Usage

### WhatsApp:
1. Send "join [sandbox-keyword]" to `+1 415 523 8886` on WhatsApp
2. Start chatting with Cypher!
3. Type "reset" to start over

### Example Conversation:
```
You: Hi
Cypher: Hi! I'm Cypher, your AI resume builder. Let's create your ATS-friendly resume! What's your full name?

You: John Doe
Cypher: Great! What's your email address?

You: john@email.com
Cypher: Perfect! What's your phone number?

You: +1234567890
Cypher: Got it! Tell me about your skills (e.g., Python, JavaScript, etc.)

You: Python, JavaScript, React, Node.js, AWS
Cypher: Excellent! Now tell me about your work experience...

[Continue conversation...]

Cypher: ✅ Your resume is ready! Generating PDF...
[Sends PDF]
```

## 🛠️ Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Run locally
python app.py

# Use ngrok for webhook testing
ngrok http 5000
# Use ngrok URL in Twilio/Instagram webhook settings
```

## 📋 Project Structure

```
cypher-bot/
├── app.py                      # Main Flask app
├── requirements.txt            # Dependencies
├── render.yaml                 # Render deployment config
├── .env.example               # Environment variables template
├── src/
│   ├── models.py              # Resume data models
│   ├── ai_service.py          # Groq AI integration
│   ├── pdf_generator.py       # ATS-friendly PDF generator
│   ├── whatsapp_service.py    # Twilio WhatsApp integration
│   └── instagram_service.py   # Meta Instagram integration
└── README.md
```

## 💰 Cost Breakdown (FREE!)

- **Groq API**: Free tier (30 requests/min)
- **Twilio**: Free trial ($15 credit, ~1000 messages)
- **Instagram**: Free
- **Render**: Free tier (750 hours/month)
- **Total**: $0/month

## 🔧 Troubleshooting

**Bot not responding on WhatsApp:**
- Check Twilio webhook URL is correct
- Verify environment variables on Render
- Check Render logs for errors

**PDF not generating:**
- Ensure all required fields are collected
- Check Render logs for PDF generation errors

**Render app sleeping:**
- Free tier sleeps after 15 min inactivity
- First message may take 30-60 seconds
- Consider using UptimeRobot (free) to ping every 5 min

## 🎯 Next Steps

1. Customize resume template in `src/pdf_generator.py`
2. Add more resume sections (certifications, projects, etc.)
3. Improve AI prompts in `src/ai_service.py`
4. Add resume preview before PDF generation
5. Support multiple resume templates

## 📝 License

MIT License - Free to use and modify!

---

Built with ❤️ using free tools only!
