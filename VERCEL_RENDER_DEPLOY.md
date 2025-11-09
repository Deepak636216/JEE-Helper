# 🚀 Deploy Guide: Frontend (Vercel) + Backend (Render)

**Best setup:** Frontend on Vercel (faster, better CDN) + Backend on Render (free Python hosting)

---

## Why This Setup?

✅ **Vercel for Frontend:**
- Fastest global CDN
- Instant deployments (< 1 minute)
- Perfect for React/Vite apps
- Free SSL & custom domains
- Auto-deploy on git push

✅ **Render for Backend:**
- Best free Python hosting
- FastAPI support out-of-the-box
- Health check monitoring
- Easy environment variables
- Auto-deploy on git push

---

## Prerequisites

1. **GitHub Account** - Code in a repository
2. **Vercel Account** - Sign up at https://vercel.com (free)
3. **Render Account** - Sign up at https://render.com (free)
4. **Google Gemini API Key** - Get from https://makersuite.google.com/app/apikey

---

## Part 1: Deploy Backend on Render (5 minutes)

### Step 1: Push Code to GitHub

```bash
git init
git add .
git commit -m "Ready for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/jee-physics-tutor.git
git push -u origin main
```

### Step 2: Create Backend Service on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect GitHub"** and authorize
4. Select repository: `YOUR_USERNAME/jee-physics-tutor`

### Step 3: Configure Backend Service

Fill in the following:

| Field | Value |
|-------|-------|
| **Name** | `jee-physics-tutor-backend` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `cd backend && pip install -r requirements.txt` |
| **Start Command** | `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

### Step 4: Add Environment Variables

Scroll down to **"Environment Variables"** section:

Click **"Add Environment Variable"**:
- **Key:** `GOOGLE_API_KEY`
- **Value:** Your Gemini API key from Google MakerSuite

Click **"Add Environment Variable"** again:
- **Key:** `PYTHON_VERSION`
- **Value:** `3.12.3`

### Step 5: Configure Health Check

Scroll to **"Health Check Path"**:
- **Path:** `/health`

### Step 6: Create Web Service

1. Click **"Create Web Service"** (bottom of page)
2. Wait 3-5 minutes for deployment
3. Your backend URL will be: `https://jee-physics-tutor-backend.onrender.com`

### Step 7: Test Backend

Open in browser:
```
https://jee-physics-tutor-backend.onrender.com/health
```

You should see:
```json
{
  "status": "healthy",
  "ai_tutor": true,
  "problem_loader": true,
  "timestamp": "2025-11-09T..."
}
```

✅ **Backend is live!** Copy this URL - you'll need it for frontend.

---

## Part 2: Deploy Frontend on Vercel (3 minutes)

### Step 1: Go to Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**

### Step 2: Import GitHub Repository

1. Click **"Import Git Repository"**
2. Find and select: `YOUR_USERNAME/jee-physics-tutor`
3. Click **"Import"**

### Step 3: Configure Project

Vercel will auto-detect it's a Vite project. Update these settings:

**Framework Preset:** `Vite`

**Root Directory:** Click **"Edit"** and set to: `frontend`

**Build Settings:**
- **Build Command:** `npm run build` (auto-detected)
- **Output Directory:** `dist` (auto-detected)
- **Install Command:** `npm install` (auto-detected)

### Step 4: Add Environment Variables

Click **"Environment Variables"** section:

Add variable:
- **Name:** `VITE_API_BASE_URL`
- **Value:** `https://jee-physics-tutor-backend.onrender.com` (your backend URL from Render)
- **Environment:** Select all (Production, Preview, Development)

Click **"Add"**

### Step 5: Deploy

1. Click **"Deploy"** button
2. Wait 1-2 minutes (Vercel is fast! ⚡)
3. Your frontend URL will be: `https://jee-physics-tutor-xxx.vercel.app`

### Step 6: Test Frontend

1. Click the **"Visit"** button or open your Vercel URL
2. You should see the JEE Physics AI Tutor interface
3. Paste a physics question and test!

✅ **Frontend is live!**

---

## Part 3: Update Backend CORS (Important!)

Now that frontend is deployed, update CORS to allow Vercel domain.

### Step 1: Update Code

Edit `backend/main.py` line 42-48:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://jee-physics-tutor-xxx.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Step 2: Commit and Push

```bash
git add backend/main.py
git commit -m "Add Vercel domain to CORS"
git push
```

Render will automatically detect the push and redeploy (2-3 minutes).

---

## Configuration Files Reference

### Files Created

1. **`vercel.json`** - Vercel configuration (optional, auto-detected)
2. **`render-backend.yaml`** - Render backend config (optional)
3. **`frontend/.env.example`** - Environment variable template

### Environment Variables Summary

**Backend (Render):**
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
PYTHON_VERSION=3.12.3
```

**Frontend (Vercel):**
```bash
VITE_API_BASE_URL=https://jee-physics-tutor-backend.onrender.com
```

---

## Testing Your Deployment

### 1. Test Backend Directly

```bash
# Health check
curl https://jee-physics-tutor-backend.onrender.com/health

# Should return JSON with status: "healthy"
```

### 2. Test Frontend

1. Open your Vercel URL
2. Paste a test question:
   ```
   Two blocks of masses 10 kg and 4 kg are connected by a spring of negligible mass and placed on a frictionless horizontal surface. An impulse gives a velocity of 14 m/s to the heavier block in the direction of the lighter block. What is the velocity of the centre of mass?
   ```
3. Click "Start Learning"
4. Verify AI responds
5. Click "Solution" button
6. Verify solution appears on the right side

### 3. Check Browser Console

Press F12 → Console tab:
- ✅ No CORS errors
- ✅ No 404 errors
- ✅ API requests succeed (200 status)

---

## Custom Domains (Optional)

### Add Custom Domain to Vercel (Frontend)

1. Go to Vercel project → **"Settings"** → **"Domains"**
2. Click **"Add"**
3. Enter your domain: `physics-tutor.yourdomain.com`
4. Follow DNS instructions from Vercel
5. Wait for SSL certificate (automatic, 1-5 minutes)

### Add Custom Domain to Render (Backend)

1. Go to Render service → **"Settings"**
2. Scroll to **"Custom Domain"**
3. Click **"Add Custom Domain"**
4. Enter: `api.physics-tutor.yourdomain.com`
5. Add DNS records as shown
6. Update `VITE_API_BASE_URL` in Vercel to new domain

---

## Monitoring & Logs

### View Backend Logs (Render)

1. Go to Render dashboard
2. Click your backend service
3. Click **"Logs"** tab
4. See real-time logs

### View Frontend Logs (Vercel)

1. Go to Vercel dashboard
2. Click your project
3. Click **"Deployments"**
4. Click latest deployment
5. View **"Build Logs"** or **"Runtime Logs"**

### Set Up Alerts

**Render:**
- Automatically emails you if service crashes
- Health check failures trigger alerts

**Vercel:**
- Build failure notifications
- Error tracking via integrations (Sentry, etc.)

---

## Automatic Deployments

### How It Works

Both platforms auto-deploy when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update: feature description"
git push

# Automatic deployments:
# ✅ Vercel deploys frontend (1-2 min)
# ✅ Render deploys backend (3-5 min)
```

### Preview Deployments (Vercel Only)

Every git push creates a preview URL:
- Production: `main` branch → `your-app.vercel.app`
- Preview: other branches → `your-app-git-branchname.vercel.app`

Perfect for testing before merging!

---

## Troubleshooting

### Issue 1: Frontend Can't Connect to Backend

**Symptoms:** CORS errors in browser console

**Solution:**
1. Verify `VITE_API_BASE_URL` is set in Vercel
2. Check backend CORS includes Vercel domain
3. Verify backend is running (check health endpoint)
4. Redeploy frontend after updating env vars

### Issue 2: Backend Cold Starts (Slow First Request)

**Symptoms:** First request takes 30-60 seconds

**Reason:** Render free tier spins down after 15 minutes idle

**Solutions:**
- Upgrade to paid tier ($7/month) for always-on
- Use UptimeRobot to ping every 10 minutes (free)
- Accept cold starts (they're normal for free tier)

### Issue 3: Build Fails on Vercel

**Symptoms:** Deployment fails during build

**Solutions:**
1. Check build logs in Vercel dashboard
2. Verify `frontend` folder has `package.json`
3. Ensure `npm run build` works locally
4. Check for missing dependencies

### Issue 4: Environment Variables Not Working

**Symptoms:** API calls go to localhost instead of backend

**Solutions:**
1. Verify env vars are set in Vercel dashboard
2. Check env var names start with `VITE_`
3. Redeploy after adding env vars
4. Hard refresh browser (Ctrl+Shift+R)

### Issue 5: 404 on Page Refresh

**Symptoms:** Refreshing page shows 404

**Solution:**
- Vercel should auto-detect this
- If not, add `vercel.json` with rewrite rules (already created)
- Redeploy

---

## Performance Tips

### Frontend (Vercel)
- ✅ Automatically optimized
- ✅ Global CDN (super fast)
- ✅ Image optimization (if you add images)
- ✅ Automatic compression

### Backend (Render)
- ⚠️ Cold starts on free tier (30-60s first request)
- ✅ Upgrade to Starter ($7/mo) for always-on
- ✅ Add caching for common responses
- ✅ Use health checks to keep warm

---

## Cost Breakdown

### Free Tier (Perfect for MVP)

**Vercel (Frontend):**
- Bandwidth: 100 GB/month
- Builds: Unlimited
- Cost: **$0/month** ✅

**Render (Backend):**
- Hours: 750/month
- Bandwidth: 100 GB/month
- Cold starts: Yes (15 min idle)
- Cost: **$0/month** ✅

**Total: FREE! 🎉**

### Paid Tier (Production)

**Vercel Pro:**
- Everything unlimited
- Cost: **$20/month**

**Render Starter:**
- No cold starts
- Always-on
- Cost: **$7/month**

**Total: $27/month** (or $7 if keeping Vercel free)

---

## URLs Reference

After deployment, you'll have:

**Backend:**
- Health: `https://jee-physics-tutor-backend.onrender.com/health`
- API: `https://jee-physics-tutor-backend.onrender.com/api/*`

**Frontend:**
- Production: `https://jee-physics-tutor-xxx.vercel.app`
- Preview: `https://jee-physics-tutor-git-branch.vercel.app`

---

## Quick Commands

### Local Development
```bash
# Backend
cd backend
python -m uvicorn main:app --reload

# Frontend
cd frontend
npm run dev
```

### Deploy Updates
```bash
git add .
git commit -m "Update: description"
git push
# Both platforms auto-deploy!
```

### View Logs
```bash
# Render CLI (optional)
render logs -s jee-physics-tutor-backend -f

# Vercel CLI (optional)
vercel logs
```

---

## Deployment Checklist

### Backend (Render)
- [ ] Repository connected
- [ ] Build command set
- [ ] Start command set
- [ ] `GOOGLE_API_KEY` environment variable added
- [ ] Health check path set to `/health`
- [ ] Service deployed successfully
- [ ] Health endpoint responding
- [ ] Backend URL copied

### Frontend (Vercel)
- [ ] Repository connected
- [ ] Root directory set to `frontend`
- [ ] `VITE_API_BASE_URL` environment variable added
- [ ] Deployed successfully
- [ ] Can load the page
- [ ] Can submit a question
- [ ] AI responds correctly
- [ ] Solution displays on right side

### Post-Deployment
- [ ] CORS updated in backend with Vercel domain
- [ ] Backend redeployed with CORS changes
- [ ] End-to-end test completed
- [ ] URLs documented
- [ ] Custom domain configured (optional)

---

## Next Steps

1. ✅ Test thoroughly with real physics questions
2. 📧 Share with beta testers
3. 📊 Monitor logs for errors
4. 🔄 Iterate based on feedback
5. 💰 Consider upgrading when you get traction

---

## Support & Resources

### Vercel
- Docs: https://vercel.com/docs
- Discord: https://vercel.com/discord
- Status: https://vercel-status.com

### Render
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### This Project
- GitHub Issues: (your repo URL)
- Documentation: `docs/` folder

---

## Summary

**Deployment Time:** ~10 minutes total
- Backend (Render): 5 minutes
- Frontend (Vercel): 3 minutes
- CORS update: 2 minutes

**Result:**
- ✅ Fast global frontend (Vercel CDN)
- ✅ Reliable backend (Render Python)
- ✅ Free to start
- ✅ Auto-deploys on push
- ✅ Production-ready

**You're live! 🚀**

For detailed guides:
- Full deployment: `docs/DEPLOYMENT_GUIDE.md`
- Quick start: `DEPLOYMENT_QUICKSTART.md`
