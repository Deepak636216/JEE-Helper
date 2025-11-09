# Deployment Guide - Render.com

Complete guide to deploying the JEE Physics AI Tutor on Render.com

---

## Prerequisites

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Render Account** - Sign up at https://render.com (free tier available)
3. **Google Gemini API Key** - Get from https://makersuite.google.com/app/apikey

---

## Project Structure

```
NCERT/
├── backend/              # Python FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   └── app/
├── frontend/             # React + Vite frontend
│   ├── package.json
│   ├── vite.config.js
│   └── src/
├── render.yaml          # Render configuration (auto-deploy)
└── docs/
```

---

## Deployment Options

### Option 1: Blueprint Deploy (Recommended - Easiest)

This deploys both backend and frontend automatically using `render.yaml`.

#### Step 1: Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/jee-physics-tutor.git
git push -u origin main
```

#### Step 2: Create New Blueprint in Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Select the repository: `YOUR_USERNAME/jee-physics-tutor`
5. Render will detect `render.yaml` automatically
6. Click **"Apply"**

#### Step 3: Set Environment Variables

After deployment starts, go to each service:

**Backend Service:**
1. Go to **"Environment"** tab
2. Add environment variable:
   - **Key:** `GOOGLE_API_KEY`
   - **Value:** Your Gemini API key from Google
3. Click **"Save Changes"**

**Frontend Service:**
1. Go to **"Environment"** tab
2. Update `VITE_API_BASE_URL`:
   - **Value:** `https://jee-physics-tutor-backend.onrender.com`
   - (Replace with your actual backend URL)
3. Click **"Save Changes"**

#### Step 4: Redeploy (if needed)

If you added env vars after initial deploy:
1. Go to each service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

### Option 2: Manual Deploy (More Control)

Deploy backend and frontend separately.

#### Backend Deployment

1. **Create Web Service:**
   - Go to https://dashboard.render.com
   - Click **"New +"** → **"Web Service"**
   - Connect GitHub repository
   - Configure:
     - **Name:** `jee-physics-tutor-backend`
     - **Runtime:** `Python 3`
     - **Build Command:** `cd backend && pip install -r requirements.txt`
     - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type:** Free

2. **Add Environment Variable:**
   - Go to **"Environment"** tab
   - Add: `GOOGLE_API_KEY` = `your_api_key_here`

3. **Health Check:**
   - Path: `/health`
   - This ensures Render knows your service is running

4. **Deploy:**
   - Click **"Create Web Service"**
   - Note your backend URL: `https://jee-physics-tutor-backend.onrender.com`

#### Frontend Deployment

1. **Create Static Site:**
   - Click **"New +"** → **"Static Site"**
   - Connect GitHub repository
   - Configure:
     - **Name:** `jee-physics-tutor-frontend`
     - **Build Command:** `cd frontend && npm install && npm run build`
     - **Publish Directory:** `frontend/dist`

2. **Add Environment Variable:**
   - Go to **"Environment"** tab
   - Add: `VITE_API_BASE_URL` = `https://jee-physics-tutor-backend.onrender.com`
   - (Use your actual backend URL from previous step)

3. **Configure Redirects (for React Router):**
   - Go to **"Redirects/Rewrites"**
   - Add rewrite rule:
     - **Source:** `/*`
     - **Destination:** `/index.html`
     - **Type:** `Rewrite`

4. **Deploy:**
   - Click **"Create Static Site"**

---

## Post-Deployment Configuration

### 1. Update CORS in Backend

The backend is already configured with CORS for local development. For production, you may want to update allowed origins in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://jee-physics-tutor-frontend.onrender.com"  # Add your frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then commit and push to trigger auto-deploy.

### 2. Test the Deployment

1. Open your frontend URL: `https://jee-physics-tutor-frontend.onrender.com`
2. Submit a test question
3. Check if AI responds
4. Click "Solution" to verify solution generation

### 3. Monitor Logs

**Backend Logs:**
- Go to backend service → **"Logs"** tab
- Check for any errors
- Verify API requests are being logged

**Frontend Logs:**
- Go to frontend service → **"Logs"** tab
- Check build logs for any issues

---

## Environment Variables Summary

### Backend (`jee-physics-tutor-backend`)
| Variable | Value | Required |
|----------|-------|----------|
| `GOOGLE_API_KEY` | Your Gemini API key | ✅ Yes |
| `PYTHON_VERSION` | 3.12.3 | Optional |

### Frontend (`jee-physics-tutor-frontend`)
| Variable | Value | Required |
|----------|-------|----------|
| `VITE_API_BASE_URL` | `https://your-backend.onrender.com` | ✅ Yes |

---

## Troubleshooting

### Issue 1: Backend Deployment Fails

**Problem:** Build command fails
**Solution:**
- Check `backend/requirements.txt` exists
- Ensure Python version is compatible
- Check logs for specific error messages

### Issue 2: Frontend Can't Connect to Backend

**Problem:** API requests fail with CORS error
**Solution:**
1. Verify `VITE_API_BASE_URL` is set correctly in frontend
2. Check CORS configuration in `backend/main.py`
3. Ensure backend service is running (check health endpoint)

### Issue 3: AI Not Responding

**Problem:** Solution generation fails
**Solution:**
1. Verify `GOOGLE_API_KEY` is set in backend environment variables
2. Check backend logs for API errors
3. Ensure API key is valid and not rate-limited

### Issue 4: 404 on Page Refresh

**Problem:** Refreshing page gives 404
**Solution:**
- Add redirect rule in frontend service:
  - Source: `/*`
  - Destination: `/index.html`
  - Type: Rewrite

---

## Free Tier Limits (Render.com)

**Web Services (Backend):**
- ✅ 750 hours/month (free)
- ⚠️ Spins down after 15 minutes of inactivity
- ⏱️ First request after spin-down: 30-60 seconds cold start

**Static Sites (Frontend):**
- ✅ Unlimited
- ✅ 100 GB bandwidth/month
- ✅ Global CDN
- ✅ Auto SSL certificates

**Tips to Reduce Cold Starts:**
- Use a service like UptimeRobot to ping your backend every 10 minutes
- Or upgrade to paid tier ($7/month) for always-on

---

## Updating Your Deployment

### Auto-Deploy (Recommended)

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push
   ```
3. Render automatically detects changes and redeploys

### Manual Deploy

1. Go to service dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## Custom Domain (Optional)

### Add Custom Domain to Frontend

1. Go to frontend service → **"Settings"**
2. Scroll to **"Custom Domain"**
3. Click **"Add Custom Domain"**
4. Enter your domain (e.g., `physics-tutor.yourdomain.com`)
5. Add DNS records as instructed by Render
6. Wait for SSL certificate to provision (automatic)

### Update Backend CORS

After adding custom domain, update CORS in `backend/main.py`:

```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:5173",
    "https://jee-physics-tutor-frontend.onrender.com",
    "https://physics-tutor.yourdomain.com"  # Your custom domain
]
```

---

## Cost Estimation

**Free Tier (Perfect for MVP/Testing):**
- Backend: Free (with cold starts)
- Frontend: Free
- Total: **$0/month**

**Paid Tier (Production-Ready):**
- Backend (Starter): $7/month (no cold starts)
- Frontend: Free
- Total: **$7/month**

---

## Monitoring & Analytics (Optional)

### Built-in Monitoring
- Render provides basic metrics dashboard
- View request counts, response times, errors

### Add Custom Monitoring
Consider adding:
- **Sentry** - Error tracking
- **Google Analytics** - User analytics
- **LogRocket** - Session replay

---

## Security Checklist

Before going live:

- [ ] ✅ HTTPS enabled (automatic with Render)
- [ ] ✅ Environment variables set (not hardcoded)
- [ ] ✅ CORS properly configured
- [ ] ✅ API key secured in backend only
- [ ] ✅ No sensitive data in frontend code
- [ ] ✅ Health check endpoint working
- [ ] ✅ Error handling in place

---

## Quick Reference

### Service URLs (Example)
- **Backend API:** `https://jee-physics-tutor-backend.onrender.com`
- **Frontend:** `https://jee-physics-tutor-frontend.onrender.com`
- **Health Check:** `https://jee-physics-tutor-backend.onrender.com/health`

### Important Files
- `render.yaml` - Deployment configuration
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node dependencies
- `backend/main.py` - FastAPI entry point

### Common Commands

**Local Development:**
```bash
# Backend
cd backend
python -m uvicorn main:app --reload

# Frontend
cd frontend
npm run dev
```

**Check Logs:**
```bash
# View recent logs
render logs -s jee-physics-tutor-backend

# Follow logs in real-time
render logs -s jee-physics-tutor-backend -f
```

---

## Next Steps After Deployment

1. ✅ Test all features thoroughly
2. 📧 Share the link with test users
3. 📊 Monitor usage and errors
4. 🔄 Iterate based on feedback
5. 🚀 Consider upgrading to paid tier when ready

---

## Support Resources

- **Render Docs:** https://render.com/docs
- **Render Community:** https://community.render.com
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/
- **Vite Production:** https://vitejs.dev/guide/build.html

---

**Deployment Status Checklist:**

- [ ] GitHub repository created and code pushed
- [ ] Backend service deployed on Render
- [ ] Frontend service deployed on Render
- [ ] `GOOGLE_API_KEY` set in backend
- [ ] `VITE_API_BASE_URL` set in frontend
- [ ] Health check responding
- [ ] Test question works end-to-end
- [ ] Solution generation works
- [ ] CORS properly configured
- [ ] URLs documented

---

**You're ready to deploy! 🚀**

Any issues? Check the troubleshooting section or Render's excellent documentation.
