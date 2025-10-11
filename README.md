# Primary Source Trainer

An interactive web application for teaching students how to classify historical sources as primary or secondary based on their research questions.

## Overview

The Primary Source Trainer helps students understand that source classification depends on the research question. The same document can be primary for one inquiry and secondary for another. This application uses early medieval historical scenarios to teach this critical historical thinking skill.

## Features

- **5 Historical Scenarios**: Each scenario presents a historical event with multiple sources
- **Interactive Graph Visualization**: Shows source relationships with lost and extant sources
- **Timeline View**: Displays chronological relationships between sources
- **Contextual Classification**: Students classify sources based on specific research questions
- **Immediate Feedback**: Instant grading with detailed explanations
- **Progress Tracking**: Email results to instructor upon completion

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- SendGrid (email delivery)
- Pydantic (data validation)

### Frontend
- React 18
- Vite
- D3.js (visualizations)
- Axios

## Setup

### Prerequisites
- Python 3.12+
- Node.js 16+
- SendGrid API key

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Add your configuration to `.env`:
   ```
   SENDGRID_API_KEY=your_sendgrid_api_key
   INSTRUCTOR_EMAIL=your_email@example.com
   SENDER_EMAIL=verified_sender@example.com
   ```

6. Run the backend:
   ```bash
   python main.py
   ```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

The frontend will run on `http://localhost:3000`

## Usage

1. Enter your name to begin
2. Work through 5 historical scenarios
3. For each scenario:
   - Read about the historical event
   - View the source relationship graph
   - Classify each source as primary or secondary based on the research question
   - Submit and receive instant feedback
4. Complete all scenarios and email results to instructor

## Educational Philosophy

This tool emphasizes that:
- **Primary sources** are the closest extant documents to your research question
- Source classification is **contextual** - the same text can be primary or secondary depending on what you're studying
- Understanding **transmission chains** (including lost sources) is crucial for historical analysis

## License

Educational use only.

## Contact

For questions or support, contact: yaniv.fox@biu.ac.il
