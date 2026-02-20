# 🤖 Cypher - Instagram AI Resume Builder

Free AI chatbot for Instagram DMs that creates ATS-friendly resume PDFs.

## 🚀 Quick Setup (15 mins)

### Step 1: Get Instagram Access Token

1. **Create Facebook Page** (if you don't have one):
   - Go to https://www.facebook.com/pages/create
   - Create a business page

2. **Create Instagram Business Account**:
   - Link your Instagram account to the Facebook page
   - Convert to Business/Creator account in Instagram settings

3. **Create Facebook App**:
   - Go to https://developers.facebook.com/apps/create/
   - Select "Business" → "Next"
   - App name: "Cypher Bot"
   - Click "Create App"

4. **Set Up Instagram Messaging**:
   - In your app dashboard, click "Add Product"
   - Find "Messenger" → Click "Set Up"
   - Scroll to "Access Tokens"
   - Select your Facebook Page
   - Copy the "Page Access Token" (starts with EAAG...)
   - This token works for Instagram too!

5. **Connect Instagram**:
   - Go to Settings → Basic → Add Platform → Website
   - Add your site URL (use https://example.com for now)
   - Go to Messenger → Settings
   - Under "Instagram", click "Add or Remove Pages"
   - Connect your Instagram account

### Step 2: Deploy to Render (FREE)

1. **Push to GitHub**:
   ```bash
   cd f:\product-1\cypher-bot
   git init
   git add .
   git commit -m "Cypher Instagram bot"
   git branch -M main
   # Create repo on GitHub, then:
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to https://render.com
   - Sign up with GitHub (free)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render auto-detects settings
   - Add environment variables:
     - `GROQ_API_KEY` = `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`
     - `INSTAGRAM_ACCESS_TOKEN` = (your token from Step 1)
     - `INSTAGRAM_VERIFY_TOKEN` = `cypher_verify_123`
   - Click "Create Web Service"
   - Wait 5-10 minutes

3. **Copy Your Webhook URL**:
   - After deployment: `https://cypher-bot-xxxx.onrender.com`

### Step 3: Configure Instagram Webhook

1. Go to Facebook App → Messenger → Settings
2. Under "Webhooks", click "Add Callback URL"
3. **Callback URL**: `https://YOUR_RENDER_URL/instagram`
4. **Verify Token**: `cypher_verify_123`
5. Click "Verify and Save"
6. Subscribe to webhook fields:
   - ✅ messages
   - ✅ messaging_postbacks
7. Under "Instagram", subscribe your Instagram account to the webhook

### Step 4: Test It!

1. Send a DM to your Instagram Business account
2. Bot should respond: "Hi! I'm Cypher..."
3. Start chatting to build your resume!

## 💬 Example Conversation

```
You: Hi
Cypher: Hi! I'm Cypher, your AI resume builder. Let's create your ATS-friendly resume! What's your full name?

You: John Doe
Cypher: Great! What's your email address?

You: john@email.com
Cypher: Perfect! What's your phone number?

You: +1234567890
Cypher: Got it! Tell me about your skills

You: Python, JavaScript, React, AWS, Docker
Cypher: Excellent! Now tell me about your work experience. Include job title, company, duration, and what you did.

You: Software Engineer at Google, 2020-2023, Built scalable microservices
Cypher: Great! Any more work experience? Or tell me about your education.

You: Bachelor of Computer Science, MIT, 2020
Cypher: ✅ Your resume is ready! Check your messages for the PDF.
```

## 🛠️ Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Use ngrok for webhook testing
ngrok http 5000
# Use ngrok URL in Facebook webhook settings
```

## 🐛 Troubleshooting

**Bot not responding:**
- Check Render logs for errors
- Verify webhook is subscribed in Facebook App
- Ensure Instagram account is connected to Facebook Page
- Check access token is valid

**"Invalid token" error:**
- Token expires - regenerate in Facebook App
- Make sure you're using Page Access Token, not User Token

**Render app sleeping:**
- Free tier sleeps after 15 min inactivity
- First message takes 30-60 seconds to wake up
- Use UptimeRobot (free) to ping every 5 min

## 📝 Commands

- Type "reset" to start over
- Type "restart" to clear data

## 💰 100% FREE

- Groq API: Free (30 req/min)
- Instagram API: Free
- Render: Free tier (750 hrs/month)
- Total: $0/month

## 🎯 Next Steps

- Customize PDF template
- Add more resume sections
- Support multiple languages
- Add resume templates

---

Built with ❤️ - Completely FREE!
