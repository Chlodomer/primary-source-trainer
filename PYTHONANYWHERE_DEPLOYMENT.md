# PythonAnywhere Deployment Guide

## Prerequisites
- PythonAnywhere account (free tier available at [pythonanywhere.com](https://www.pythonanywhere.com))
- SendGrid API key for email functionality
- Git repository with your code

## Step-by-Step Deployment

### 1. Sign Up and Create Account
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free Beginner account
3. Note your username (you'll need it later)

### 2. Upload Your Code

#### Option A: Using Git (Recommended)
1. Open a Bash console from your PythonAnywhere dashboard
2. Clone your repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/primary-source-trainer.git
   cd primary-source-trainer
   ```

#### Option B: Upload Files
1. Use the "Files" tab in PythonAnywhere
2. Upload your `backend` folder

### 3. Set Up Virtual Environment

In your PythonAnywhere Bash console:

```bash
cd ~/primary-source-trainer/backend
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** PythonAnywhere free tier supports Python 3.12, which matches your `runtime.txt`.

### 4. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
cd ~/primary-source-trainer/backend
nano .env
```

Add your configuration:
```
SENDGRID_API_KEY=your_sendgrid_api_key_here
INSTRUCTOR_EMAIL=foxyaniv@gmail.com
SENDER_EMAIL=verified_sender@sendgrid.com
FRONTEND_URL=https://your-frontend-url.vercel.app
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

### 5. Configure Web App

1. Go to the "Web" tab in your PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select **Python 3.12**
5. Click through the setup wizard

### 6. Configure WSGI File

1. In the "Web" tab, find the "Code" section
2. Click on the WSGI configuration file link (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **Delete all the existing content**
4. Replace with the following:

```python
import sys
import os
from pathlib import Path

# IMPORTANT: Replace YOUR_USERNAME with your actual PythonAnywhere username
project_home = '/home/YOUR_USERNAME/primary-source-trainer/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
venv_path = '/home/YOUR_USERNAME/primary-source-trainer/backend/venv'
activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')

# For Python 3.12, we need to use exec with open
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Load environment variables
from dotenv import load_dotenv
env_path = Path(project_home) / '.env'
load_dotenv(dotenv_path=env_path)

# Import the FastAPI app
from main import app

# PythonAnywhere uses WSGI, FastAPI is ASGI
# We use a2wsgi library to bridge them
from a2wsgi import ASGIMiddleware

application = ASGIMiddleware(app)
```

5. Click "Save"

### 7. Install a2wsgi

The a2wsgi library is needed to convert ASGI (FastAPI) to WSGI (PythonAnywhere).

In your Bash console:
```bash
source ~/primary-source-trainer/backend/venv/bin/activate
pip install a2wsgi
```

### 8. Update requirements.txt

Add a2wsgi to your requirements.txt:

```bash
cd ~/primary-source-trainer/backend
echo "a2wsgi==1.10.0" >> requirements.txt
```

### 9. Configure Virtual Environment Path

Back in the "Web" tab:

1. Find the "Virtualenv" section
2. Enter the path to your virtual environment:
   ```
   /home/YOUR_USERNAME/primary-source-trainer/backend/venv
   ```
3. The system will validate the path

### 10. Configure Static Files (Optional)

If you want to serve static files, add:
- URL: `/static/`
- Directory: `/home/YOUR_USERNAME/primary-source-trainer/backend/static`

### 11. Reload Web App

1. Scroll to the top of the "Web" tab
2. Click the big green **"Reload"** button
3. Wait for the reload to complete

### 12. Test Your API

Your API will be available at:
```
https://YOUR_USERNAME.pythonanywhere.com
```

Test it by visiting:
```
https://YOUR_USERNAME.pythonanywhere.com/
https://YOUR_USERNAME.pythonanywhere.com/api/scenarios
```

You should see JSON responses!

### 13. Configure Frontend

Update your frontend's API URL environment variable:
- In Vercel (or your frontend hosting): Set `VITE_API_URL` to `https://YOUR_USERNAME.pythonanywhere.com`
- Redeploy your frontend

### 14. Update CORS Settings

Make sure your backend allows your frontend URL. In `main.py`, the CORS middleware already includes:
```python
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://primary-source-trainer.vercel.app",
    os.getenv("FRONTEND_URL", "")
]
```

This will use the `FRONTEND_URL` from your `.env` file.

---

## Troubleshooting

### Error: "No module named 'main'"
- Check that your WSGI file has the correct path
- Verify the virtual environment is activated
- Make sure all files are in the right directory

### Error: "No module named 'a2wsgi'"
- Run: `pip install a2wsgi` in your activated virtual environment
- Reload the web app

### Error: "Import Error: cannot import name 'app'"
- Check that `main.py` exists in your backend directory
- Verify the virtual environment has all dependencies installed
- Check the error log in the "Web" tab

### CORS Errors
- Verify `FRONTEND_URL` is set in your `.env` file
- Check that it matches your actual frontend URL
- Reload the web app after changes

### Email Not Working
- Verify `SENDGRID_API_KEY` is correct in `.env`
- Check SendGrid dashboard for blocked emails
- Verify sender email is authenticated in SendGrid

### 502 Bad Gateway
- Check the error log (link in "Web" tab)
- Usually means there's a Python error in your code
- Fix the error and reload

---

## Viewing Logs

PythonAnywhere provides three types of logs in the "Web" tab:
1. **Access log**: Shows all requests to your app
2. **Error log**: Shows Python errors and stack traces
3. **Server log**: Shows web server issues

Check these if something isn't working!

---

## Updating Your Code

When you make changes:

```bash
cd ~/primary-source-trainer
git pull origin main
cd backend
source venv/bin/activate
pip install -r requirements.txt  # If dependencies changed
```

Then click **Reload** in the Web tab.

---

## Free Tier Limitations

PythonAnywhere free tier includes:
- ✅ One web app
- ✅ Python 3.12 support
- ✅ 512 MB disk space
- ✅ HTTPS included
- ⚠️ CPU seconds limited (100 seconds/day for web apps)
- ⚠️ Only whitelisted sites for external API calls (SendGrid is whitelisted!)
- ⚠️ Web app sleeps after 3 months of inactivity

For a classroom app with moderate use, the free tier should work fine!

---

## Alternative: Paid Account Benefits

If you need more resources:
- Hacker plan ($5/month): More CPU, multiple web apps
- No whitelist restrictions
- More storage
- Always-on apps

---

## Summary

Your Primary Source Trainer backend is now live at:
```
https://YOUR_USERNAME.pythonanywhere.com/api/scenarios
```

Students can access it through your frontend, which should point to this URL!
