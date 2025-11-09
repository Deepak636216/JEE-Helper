# 🚀 Quick Deployment Guide

Deploy to Render.com in 10 minutes!

---

## Step 1: Push to GitHub (2 min)

```bash
git init
git add .
git commit -m "Ready for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/jee-physics-tutor.git
git push -u origin main
```

---

## Step 2: Deploy on Render (5 min)

### Option A: Blueprint (Easiest - Recommended)

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect GitHub repo
4. Click **"Apply"**
5. Done! ✅

### Option B: Manual

**Backend:**
1. New → Web Service
2. Build: `cd backend && pip install -r requirements.txt`
3. Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

**Frontend:**
1. New → Static Site
2. Build: `cd frontend && npm install && npm run build`
3. Publish: `frontend/dist`

---

## Step 3: Set Environment Variables (3 min)

### Backend Service
```
GOOGLE_API_KEY = your_gemini_api_key_here
```

### Frontend Service
```
VITE_API_BASE_URL = https://your-backend-url.onrender.com
```

---

## Step 4: Redeploy & Test

1. Click "Manual Deploy" on both services
2. Wait 2-3 minutes
3. Open frontend URL
4. Test with a physics question
5. ✅ Done!

---

## URLs You'll Get

- **Backend:** `https://jee-physics-tutor-backend.onrender.com`
- **Frontend:** `https://jee-physics-tutor-frontend.onrender.com`
- **Health:** `https://jee-physics-tutor-backend.onrender.com/health`

---

## Troubleshooting

**Frontend can't reach backend?**
- Check `VITE_API_BASE_URL` is set correctly
- Verify backend is running (visit /health endpoint)

**AI not responding?**
- Verify `GOOGLE_API_KEY` is set in backend
- Check backend logs for errors

**404 on page refresh?**
- Add redirect in frontend: `/*` → `/index.html` (Rewrite)

---

## Free Tier Limits

- ✅ Backend: Free (spins down after 15 min idle)
- ✅ Frontend: Free unlimited
- ⏱️ Cold start: 30-60 seconds on first request

---

**That's it! For detailed guide, see [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)**
