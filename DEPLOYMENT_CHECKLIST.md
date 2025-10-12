# PythonAnywhere Deployment Checklist for Chilperic

This is your personalized deployment checklist with all your specific information.

## Your Configuration

- **PythonAnywhere Username:** Chilperic
- **Instructor Email:** yaniv.fox@biu.ac.il
- **SendGrid API Key:** Already configured in .env
- **Your API URL will be:** https://Chilperic.pythonanywhere.com

---

## Step-by-Step Deployment

### ✅ Step 1: Push Code to GitHub (if not already done)

```bash
cd "/Users/yanivfox/Desktop/AI Initiatives/Primary sources"
git add .
git commit -m "Prepare for PythonAnywhere deployment"
git push origin main
```

**Note:** If you don't have a GitHub repo yet, create one first at github.com/new

---

### ✅ Step 2: Sign Up for PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Click "Start running Python online in less than a minute!"
3. Create a **Beginner** (free) account with username: **Chilperic**
4. Verify your email

---

### ✅ Step 3: Clone Your Repository

1. In PythonAnywhere dashboard, click **"Open Bash console"**
2. Run these commands:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/primary-source-trainer.git
cd primary-source-trainer
ls -la
```

**Expected output:** You should see `backend`, `frontend`, `README.md`, etc.

---

### ✅ Step 4: Set Up Virtual Environment

In the same Bash console:

```bash
cd ~/primary-source-trainer/backend
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**This will take 2-3 minutes.** You should see all packages installing.

**Important:** Check that a2wsgi installed successfully (it's in requirements.txt)

---

### ✅ Step 5: Create .env File

Still in the Bash console:

```bash
cd ~/primary-source-trainer/backend
nano .env
```

Paste this exact content (replace YOUR_SENDGRID_API_KEY with your actual key):

```
SENDGRID_API_KEY=YOUR_SENDGRID_API_KEY
INSTRUCTOR_EMAIL=yaniv.fox@biu.ac.il
SENDER_EMAIL=foxyaniv@gmail.com
```

**Note:** Use your actual SendGrid API key (starts with SG.)

Press `Ctrl+X`, then `Y`, then `Enter` to save.

Verify it saved correctly:
```bash
cat .env
```

---

### ✅ Step 6: Create Web App

1. Go to the **"Web"** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Click **"Next"** (keep your domain: chilperic.pythonanywhere.com)
4. Select **"Manual configuration"** (NOT Flask/Django!)
5. Select **"Python 3.12"**
6. Click **"Next"** to finish setup

---

### ✅ Step 7: Configure Virtual Environment

Still in the "Web" tab:

1. Scroll to the **"Virtualenv"** section
2. In the input field, enter:
   ```
   /home/Chilperic/primary-source-trainer/backend/venv
   ```
3. Press Enter
4. You should see a green checkmark ✓

---

### ✅ Step 8: Configure WSGI File

1. In the "Web" tab, find the **"Code"** section
2. Click on the WSGI configuration file link (something like `/var/www/Chilperic_pythonanywhere_com_wsgi.py`)
3. **Delete ALL existing content**
4. Paste this exact code:

```python
import sys
import os
from pathlib import Path

# Add project directory to sys.path
project_home = '/home/Chilperic/primary-source-trainer/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
venv_path = '/home/Chilperic/primary-source-trainer/backend/venv'
activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')

# For Python 3.12
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Load environment variables
from dotenv import load_dotenv
env_path = Path(project_home) / '.env'
load_dotenv(dotenv_path=env_path)

# Import the FastAPI app
from main import app

# Convert ASGI (FastAPI) to WSGI (PythonAnywhere)
from a2wsgi import ASGIMiddleware

application = ASGIMiddleware(app)
```

5. Click **"Save"** (top right)

---

### ✅ Step 9: Reload Web App

1. Scroll to the top of the "Web" tab
2. Click the big green **"Reload chilperic.pythonanywhere.com"** button
3. Wait for it to finish (takes 5-10 seconds)

---

### ✅ Step 10: Test Your API

Open these URLs in your browser:

1. **Health check:** https://chilperic.pythonanywhere.com/
   - Should show: `{"message": "Primary Source Trainer API", "version": "1.0.0", ...}`

2. **Get scenarios:** https://chilperic.pythonanywhere.com/api/scenarios
   - Should show: JSON array with 10 scenarios

**If you see JSON responses, your backend is live! 🎉**

---

### ✅ Step 11: Check Error Log (if something went wrong)

If you get an error instead:

1. In the "Web" tab, click **"Error log"** (near the top)
2. Look at the last error message
3. Common issues:
   - **Import error:** Check WSGI file paths are correct
   - **Module not found:** Re-run `pip install -r requirements.txt`
   - **500 error:** Check error log for Python errors

---

### ✅ Step 12: Deploy Frontend (Vercel)

Your backend is ready! Now deploy your frontend:

1. Go to https://vercel.com
2. Sign up/login with GitHub
3. Click **"Add New Project"**
4. Import your GitHub repository
5. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** frontend
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
6. Add Environment Variable:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://chilperic.pythonanywhere.com`
7. Click **"Deploy"**

Wait 2-3 minutes for deployment to complete.

---

### ✅ Step 13: Update CORS (Backend)

Your frontend URL will be something like: `https://primary-source-trainer.vercel.app`

1. Go back to PythonAnywhere Bash console
2. Edit .env:
   ```bash
   cd ~/primary-source-trainer/backend
   nano .env
   ```
3. Add this line at the end:
   ```
   FRONTEND_URL=https://your-actual-frontend-url.vercel.app
   ```
4. Save (Ctrl+X, Y, Enter)
5. Go to "Web" tab and click **"Reload"**

---

### ✅ Step 14: Test Complete App

1. Visit your frontend URL
2. Enter your name
3. Complete a scenario
4. Submit results
5. Check **yaniv.fox@biu.ac.il** for the email!

---

## Troubleshooting

### Backend shows 502 Bad Gateway
- Check error log in "Web" tab
- Make sure virtual environment path is correct
- Verify all dependencies installed

### Email not sending
- Check SendGrid dashboard for errors
- Verify sender email (foxyaniv@gmail.com) is verified in SendGrid
- Check error log for email-related errors

### Frontend can't reach backend
- Make sure FRONTEND_URL is set in backend .env
- Verify API URL in Vercel environment variables
- Check browser console for CORS errors

### How to view logs
- **Error log:** Web tab → "Error log" link
- **Access log:** Web tab → "Access log" link
- **Server log:** Web tab → "Server log" link

---

## Updating Your Code

When you make changes:

```bash
# On PythonAnywhere Bash console
cd ~/primary-source-trainer
git pull origin main
cd backend
source venv/bin/activate
pip install -r requirements.txt  # If dependencies changed

# Then reload in Web tab
```

---

## Your Live URLs

Once deployed:
- **Backend API:** https://chilperic.pythonanywhere.com
- **Frontend:** https://your-app-name.vercel.app (you'll get this from Vercel)
- **Test endpoint:** https://chilperic.pythonanywhere.com/api/scenarios

---

## Questions?

If you run into issues:
1. Check the error log
2. Review PYTHONANYWHERE_DEPLOYMENT.md
3. Common issues are usually:
   - Wrong file paths
   - Missing environment variables
   - Dependencies not installed

**You're ready to deploy! Follow the steps above one by one. Good luck! 🚀**
