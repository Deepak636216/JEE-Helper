# React + FastAPI Setup Guide

## Architecture Overview

```
Frontend (React)          Backend (FastAPI)
Port: 3000               Port: 8000
─────────────            ─────────────
   User Interface   →    API Endpoints
   Vite + React          Python + Gemini AI
```

---

## Backend Setup (FastAPI)

### 1. Install Dependencies

```bash
cd D:\Projects\NCERT

# Install FastAPI requirements
pip install fastapi uvicorn python-multipart
```

### 2. Make sure .env file exists

```bash
# Should already exist at D:\Projects\NCERT\.env
GOOGLE_API_KEY=your_key_here
```

### 3. Run FastAPI Server

```bash
# From D:\Projects\NCERT directory
python backend/main.py

# Or using uvicorn directly
uvicorn backend.main:app --reload --port 8000
```

**API will run at:** `http://localhost:8000`

**Test it:** Open `http://localhost:8000` in browser

---

## Frontend Setup (React)

### 1. Install Node.js Dependencies

```bash
cd D:\Projects\NCERT\frontend

# Install all packages
npm install
```

### 2. Run React Development Server

```bash
npm run dev
```

**React app will run at:** `http://localhost:3000`

---

## Running Both Together

**Terminal 1 (Backend):**
```bash
cd D:\Projects\NCERT
python backend/main.py
```

**Terminal 2 (Frontend):**
```bash
cd D:\Projects\NCERT\frontend
npm run dev
```

**Then open:** `http://localhost:3000`

---

## API Endpoints Documentation

### Health Check
```
GET http://localhost:8000/health
```

### Submit Question
```
POST http://localhost:8000/api/question/submit
Body: {
  "text": "A ball is thrown...",
  "type": "numerical",
  "topic": "Projectile Motion",
  "difficulty": "medium"
}
```

### Chat with AI
```
POST http://localhost:8000/api/chat
Body: {
  "problem": {...},
  "conversation_history": [...],
  "user_message": "The range"
}
```

### Request Hint
```
POST http://localhost:8000/api/hint
Body: {
  "problem": {...},
  "conversation_history": [...],
  "hint_level": 1
}
```

### Get Solution
```
POST http://localhost:8000/api/solution
Body: {
  "problem": {...}
}
```

### Get Sample Problems
```
GET http://localhost:8000/api/problems/samples?topic=Friction
```

---

## Request/Response Logging

### Backend Logs

**File:** `D:\Projects\NCERT\api_requests.log`

**What's logged:**
- Every API request (method, URL, body)
- Response status and duration
- Errors with stack traces
- Timestamp for each request

**Example log:**
```
2025-01-19 10:30:45 - REQUEST [1705652445000] POST /api/chat
2025-01-19 10:30:45 - REQUEST BODY [1705652445000]: {
  "problem": {...},
  "conversation_history": [...],
  "user_message": "The range"
}
2025-01-19 10:30:47 - RESPONSE [1705652445000] Status: 200 Duration: 2.15s
```

### Frontend Logs

**Browser Console:** Open DevTools (F12) → Console tab

**What's logged:**
- API requests before sending
- API responses after receiving
- Errors

**Example:**
```
[API REQUEST] POST /api/chat {problem: {...}, ...}
[API RESPONSE] /api/chat {response: "Great! What is...", ...}
```

---

## Project Structure

```
NCERT/
├── backend/
│   ├── main.py                # FastAPI application
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── tutorApi.js   # API client with logging
│   │   ├── components/
│   │   │   ├── QuestionForm.jsx
│   │   │   ├── ChatInterface.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── App.jsx            # Main React component
│   │   └── main.jsx           # Entry point
│   ├── package.json
│   └── vite.config.js
├── ai_tutor.py                # AI tutor logic (shared)
├── utils.py                   # Problem loader (shared)
├── .env                       # API keys
└── api_requests.log           # Auto-generated logs
```

---

## Benefits of React + FastAPI

### vs Streamlit:

**React + FastAPI:**
✅ Full API logging (every request/response)
✅ Professional UI with better UX
✅ Separate frontend/backend
✅ Can deploy independently
✅ Better performance
✅ Custom components
✅ Production-ready architecture

**Streamlit:**
❌ Limited request logging
❌ Less customizable UI
❌ Tightly coupled
❌ Harder to scale
❌ Widget-based limitations

---

## Troubleshooting

### Backend won't start
- Check if port 8000 is free
- Verify .env file exists with API key
- Check Python virtual environment is activated

### Frontend won't start
- Run `npm install` first
- Check if port 3000 is free
- Verify Node.js is installed (`node --version`)

### CORS errors
- Make sure backend is running
- Check CORS settings in `backend/main.py`
- Frontend proxy configured in `vite.config.js`

### API requests failing
- Check backend logs in `api_requests.log`
- Check browser console for frontend errors
- Verify API key is valid in `.env`

---

## Testing API with cURL

```bash
# Health check
curl http://localhost:8000/health

# Submit question
curl -X POST http://localhost:8000/api/question/submit \
  -H "Content-Type: application/json" \
  -d '{"text":"A ball is thrown from 45m cliff at 20 m/s. Find range.","type":"numerical","topic":"Projectile Motion"}'

# Get topics
curl http://localhost:8000/api/topics
```

---

## Next Steps

1. ✅ Start both servers
2. ✅ Open http://localhost:3000
3. ✅ Test question submission
4. ✅ Check API logs in `api_requests.log`
5. ✅ Monitor browser console for frontend logs
6. 🚀 Build and deploy to production!

---

## Production Deployment

### Backend:
- Deploy FastAPI to Render, Railway, or AWS
- Use Gunicorn/Uvicorn for production
- Set environment variables

### Frontend:
- Build: `npm run build`
- Deploy static files to Vercel, Netlify, or Cloudflare Pages
- Update API_BASE_URL to production backend URL

**You now have a professional, production-ready application!** 🎉
