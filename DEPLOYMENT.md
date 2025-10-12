# Deployment Guide

This guide covers multiple deployment options for your Primary Source Trainer app.

## Deployment Options

1. **[Vercel](#deploying-to-vercel)** - Recommended for frontend; serverless functions for backend
2. **[PythonAnywhere](#deploying-to-pythonanywhere)** - Traditional Python hosting; free tier available
3. **Render** - Alternative Python hosting (see Render-specific docs)

---

## Deploying to Vercel

### Prerequisites
1. GitHub account
2. Vercel account (free tier) - sign up at [vercel.com](https://vercel.com)
3. SendGrid account (free tier) for email functionality

### Step 1: Get SendGrid API Key

1. Sign up for SendGrid at [sendgrid.com](https://sendgrid.com) (free tier: 100 emails/day)
2. Go to Settings > API Keys
3. Click "Create API Key"
4. Name it "Primary Source Trainer"
5. Choose "Full Access"
6. Copy the API key (you'll only see it once!)

### Step 2: Push Code to GitHub

```bash
cd "/Users/yanivfox/Desktop/AI Initiatives/Primary sources"
git init
git add .
git commit -m "Initial commit: Primary Source Trainer"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 3: Deploy Frontend to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Configure project:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

4. Add Environment Variables:
   - Click "Environment Variables"
   - Add: `VITE_API_URL` = `https://YOUR-BACKEND-URL.vercel.app`
   - (You'll update this after deploying backend)

5. Click "Deploy"

### Step 4: Deploy Backend to Vercel

1. Create a new project in Vercel
2. Import the same GitHub repository
3. Configure project:
   - **Framework Preset:** Other
   - **Root Directory:** `backend`
   - **Build Command:** (leave empty)
   - **Output Directory:** (leave empty)

4. Add Environment Variables:
   - `SENDGRID_API_KEY` = your SendGrid API key from Step 1
   - `INSTRUCTOR_EMAIL` = `foxyaniv@gmail.com`

5. Click "Deploy"

### Step 5: Update Frontend Environment Variable

1. Copy the backend deployment URL (e.g., `https://primary-source-backend.vercel.app`)
2. Go to your frontend project in Vercel
3. Go to Settings > Environment Variables
4. Update `VITE_API_URL` to your backend URL
5. Redeploy the frontend

### Step 6: Test Your Deployment

1. Visit your frontend URL
2. Complete a scenario
3. Click "Finish & Send to Instructor"
4. Check foxyaniv@gmail.com for the results email

### Sharing with Students

Your app will be live at a URL like:
```
https://primary-source-trainer.vercel.app
```

Share this URL with your students!

---

## Alternative: Deploy as Single Vercel Project (Advanced)

You can also deploy both frontend and backend together:

1. Use the root `vercel.json` configuration
2. In Vercel project settings:
   - Root Directory: `.` (root)
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/dist`

3. Add environment variables:
   - `SENDGRID_API_KEY`
   - `INSTRUCTOR_EMAIL`
   - `VITE_API_URL` = `/api` (relative URL)

This approach keeps everything in one deployment.

---

## Troubleshooting

### Backend errors
- Check Vercel logs in the Functions tab
- Ensure all Python dependencies are in `requirements.txt`
- Verify environment variables are set correctly

### Email not sending
- Check SendGrid API key is correct
- Verify sender email is verified in SendGrid
- Check SendGrid dashboard for blocked emails

### CORS errors
- Ensure frontend URL is allowed in backend CORS settings
- Check that API_URL environment variable is correct

### Frontend can't reach backend
- Verify VITE_API_URL is set correctly
- Check that backend is deployed and accessible
- Test backend API directly at `/api/scenarios`

---

## Updating the App

To push updates:

```bash
git add .
git commit -m "Description of changes"
git push
```

Vercel will automatically redeploy both frontend and backend!

---

## Deploying to PythonAnywhere

For detailed PythonAnywhere deployment instructions, see **[PYTHONANYWHERE_DEPLOYMENT.md](PYTHONANYWHERE_DEPLOYMENT.md)**.

### Quick Overview

PythonAnywhere is a Python-specific hosting platform with a generous free tier, perfect for educational projects.

**Pros:**
- Free tier includes HTTPS
- Easy Python app hosting
- No credit card required
- Good for classroom use

**Cons:**
- Free tier has CPU limits
- Web app sleeps after 3 months of inactivity
- WSGI only (requires adapter for FastAPI)

**Quick Steps:**
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Clone your repo or upload files
3. Set up virtual environment
4. Configure WSGI file with a2wsgi adapter
5. Set environment variables
6. Your API will be at `https://YOUR_USERNAME.pythonanywhere.com`

See **[PYTHONANYWHERE_DEPLOYMENT.md](PYTHONANYWHERE_DEPLOYMENT.md)** for complete step-by-step instructions!
