# AI Tutor Setup Guide

## Get Your Google Gemini API Key

### Step 1: Get API Key (Free)
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

### Step 2: Add API Key to Project

Create a file named `.env` in the project root (D:\Projects\NCERT\.env):

```bash
GOOGLE_API_KEY=AIzaSy...your_key_here...
```

**Important:**
- The file should be named `.env` (with a dot at the start)
- No quotes around the key
- One line only

### Step 3: Restart the App

```bash
# Stop the current app (Ctrl+C in terminal)
# Then restart:
streamlit run app.py
```

## Verify It's Working

1. Enter a physics question in the app
2. Click "Start Learning"
3. You should see the AI tutor's first message
4. Start chatting!

## Troubleshooting

### Error: "API key missing"
- Make sure `.env` file exists in the project root
- Check the file name is exactly `.env` (not `env.txt` or `.env.txt`)
- Verify the API key is correct

### Error: "API call failed"
- Check your internet connection
- Verify the API key is valid
- Make sure you haven't exceeded free tier limits

### AI responses are slow
- This is normal - Gemini API takes 2-5 seconds
- Be patient, the AI is thinking!

## Free Tier Limits

Google Gemini Free Tier:
- ✅ 15 requests per minute
- ✅ 1500 requests per day
- ✅ Completely FREE

This is more than enough for personal use!

## Example .env File

```bash
# Google Gemini API Key
GOOGLE_API_KEY=AIzaSyDExampleKey123456789AbCdEfGhIjK
```

That's it! You're ready to use the AI tutor! 🎉
