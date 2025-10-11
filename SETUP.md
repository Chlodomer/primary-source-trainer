# Local Development Setup

## Prerequisites

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

## Quick Start (5 minutes)

### 1. Install Backend Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Backend Environment

```bash
# Still in backend/ directory
cp .env.example .env
```

Edit `.env` and add your SendGrid API key (optional for local testing):
```
SENDGRID_API_KEY=your_key_here
INSTRUCTOR_EMAIL=foxyaniv@gmail.com
```

**Note:** Email functionality is optional for local testing. The app will still work without it.

### 3. Start Backend Server

```bash
# Still in backend/ directory with venv activated
python main.py
```

Backend will run on `http://localhost:8000`

You can test it by visiting: `http://localhost:8000` (should show API info)

### 4. Install Frontend Dependencies

Open a **new terminal window**:

```bash
cd frontend
npm install
```

### 5. Start Frontend Server

```bash
# Still in frontend/ directory
npm run dev
```

Frontend will run on `http://localhost:3000`

### 6. Open the App

Visit `http://localhost:3000` in your browser!

---

## Testing the App Locally

1. **Load scenarios** - Should see 10 scenarios
2. **Classify sources** - Click Primary/Secondary/Depends on Topic
3. **Add justification** - Write why you chose that classification
4. **Submit & Grade** - See your score
5. **Complete all 10** - Get final summary
6. **Send to instructor** - Email will only work if SendGrid is configured

---

## Project Structure

```
Primary sources/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # API endpoints
│   ├── models.py           # Data models
│   ├── scenarios.py        # 10 historical scenarios
│   ├── grading.py          # Classification algorithm
│   ├── email_service.py    # SendGrid integration
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── Timeline.jsx          # D3 timeline visualization
│   │   │   ├── SourceCard.jsx        # Source classification UI
│   │   │   ├── ScenarioView.jsx      # Main scenario interface
│   │   │   └── FinalSummary.jsx      # Session results
│   │   ├── styles/
│   │   │   └── App.css     # Main styles
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   ├── index.html          # HTML template
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
│
├── README.md               # Project overview
├── SETUP.md               # This file
├── DEPLOYMENT.md          # Vercel deployment guide
├── Primary_Source_Trainer_PRD.md  # Product requirements
└── permissions.md         # Development permissions
```

---

## Common Commands

### Backend

```bash
# Activate virtual environment
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start dev server
python main.py

# Start with auto-reload (alternative)
uvicorn main:app --reload

# Install new package
pip install package_name
pip freeze > requirements.txt
```

### Frontend

```bash
# Start dev server
cd frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Install new package
npm install package_name
```

---

## Environment Variables

### Backend (`.env`)
```bash
SENDGRID_API_KEY=your_sendgrid_api_key_here
INSTRUCTOR_EMAIL=foxyaniv@gmail.com
DATABASE_URL=sqlite:///./primary_sources.db  # Not used yet (future)
```

### Frontend (`.env`)
```bash
VITE_API_URL=http://localhost:8000
```

---

## API Endpoints

Once backend is running, you can test these endpoints:

- `GET /` - Health check
- `GET /api/scenarios` - Get all 10 scenarios
- `GET /api/scenario/{id}` - Get specific scenario
- `POST /api/grade` - Grade a submission
- `POST /api/submit-session` - Submit complete session & email results
- `GET /api/stats` - Get scenario statistics

Test in browser or with curl:
```bash
curl http://localhost:8000/api/scenarios
```

---

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.10+)
- Make sure virtual environment is activated (should see `(venv)` in terminal)
- Check if port 8000 is already in use

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is already in use

### "Cannot connect to backend" error
- Make sure backend is running on port 8000
- Check frontend `.env` has correct `VITE_API_URL`
- Try accessing `http://localhost:8000` directly

### Email not sending
- Check SendGrid API key is set in backend `.env`
- For local testing, you can skip email - just check console for output
- Email is optional for development

---

## Development Tips

### Hot Reload
Both frontend and backend support hot reload:
- **Frontend:** Changes to `.jsx` files reload automatically
- **Backend:** Use `uvicorn main:app --reload` for auto-reload

### Checking Logs
- **Backend:** Check terminal where `python main.py` is running
- **Frontend:** Check browser console (F12)

### Modifying Scenarios
Edit `backend/scenarios.py` to:
- Change scenario content
- Add new scenarios
- Adjust difficulty levels

### Styling
Edit `frontend/src/styles/App.css` to change:
- Colors (see `:root` CSS variables)
- Layout
- Component styles

---

## Next Steps

1. ✅ Get app running locally
2. Test with a complete scenario
3. Review [DEPLOYMENT.md](DEPLOYMENT.md) to deploy to Vercel
4. Share deployment URL with students!

---

## Getting Help

- Check the [PRD](Primary_Source_Trainer_PRD.md) for feature details
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for hosting
- Check browser console and terminal for error messages
