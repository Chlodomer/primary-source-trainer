"""
FastAPI backend for Primary Source Trainer.
Main application with API endpoints.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
from dotenv import load_dotenv

from models import (
    Scenario, Submission, ScenarioResult, GradingResult,
    SessionSubmission, Topic
)
from scenarios import generate_scenarios
from grading import classify_sources, grade_submission, get_node_feedback

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Primary Source Trainer API",
    description="Backend for early medieval source classification training",
    version="1.0.0"
)

# CORS middleware for frontend
# Allow localhost for development and Vercel domains for production
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://primary-source-trainer.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for scenarios (could move to database later)
SCENARIOS: List[Scenario] = generate_scenarios()


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "message": "Primary Source Trainer API",
        "version": "1.0.0",
        "scenarios_available": len(SCENARIOS)
    }


@app.get("/api/scenarios", response_model=List[Scenario])
def get_all_scenarios():
    """
    Get all available scenarios.
    Returns list of 10 scenarios for the training session.
    """
    return SCENARIOS


@app.get("/api/scenario/{scenario_id}", response_model=Scenario)
def get_scenario(scenario_id: str):
    """Get a specific scenario by ID."""
    scenario = next((s for s in SCENARIOS if s.id == scenario_id), None)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario


@app.post("/api/grade", response_model=ScenarioResult)
def grade_scenario(submission: Submission):
    """
    Grade a student's submission for a single scenario.

    Request body:
        - scenario_id: ID of the scenario
        - student_name: Student's name
        - classifications: List of {node_id, classification, justification}
        - topic_id: Which topic was used for classification
    """
    try:
        # Find scenario
        scenario = next((s for s in SCENARIOS if s.id == submission.scenario_id), None)
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")

        # Find topic
        topic = next((t for t in scenario.topics if t.id == submission.topic_id), None)
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")

        # Grade the submission
        score, max_score, results = grade_submission(
            scenario=scenario,
            topic=topic,
            classifications=submission.classifications
        )

        return ScenarioResult(
            scenario_id=submission.scenario_id,
            score=score,
            max_score=max_score,
            results=results,
            topic_label=topic.label
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error grading submission: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Grading error: {str(e)}")


@app.post("/api/classify/{scenario_id}/{topic_id}")
def get_classification(scenario_id: str, topic_id: str):
    """
    Get the correct classification for a scenario/topic combo.
    Useful for showing answers after grading.
    """
    scenario = next((s for s in SCENARIOS if s.id == scenario_id), None)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    topic = next((t for t in scenario.topics if t.id == topic_id), None)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    primary, secondary = classify_sources(scenario, topic)

    return {
        "scenario_id": scenario_id,
        "topic_id": topic_id,
        "topic_label": topic.label,
        "primary_sources": list(primary),
        "secondary_sources": list(secondary)
    }


@app.get("/api/feedback/{scenario_id}/{node_id}/{topic_id}")
def get_detailed_feedback(scenario_id: str, node_id: str, topic_id: str):
    """
    Get detailed feedback explaining why a node is primary/secondary.
    """
    scenario = next((s for s in SCENARIOS if s.id == scenario_id), None)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    topic = next((t for t in scenario.topics if t.id == topic_id), None)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    feedback = get_node_feedback(scenario, node_id, topic)

    return {
        "scenario_id": scenario_id,
        "node_id": node_id,
        "topic_id": topic_id,
        "feedback": feedback
    }


@app.post("/api/submit-session")
def submit_session(submission: SessionSubmission):
    """
    Submit complete session results and generate downloadable report.

    Request body:
        - student_name: Student's name
        - student_email: (optional) Student's email
        - scenario_results: List of ScenarioResult objects
    """
    import hashlib
    import json
    from datetime import datetime

    # Calculate total score
    total_score = sum(r.score for r in submission.scenario_results)
    max_score = sum(r.max_score for r in submission.scenario_results)
    percentage = round((total_score / max_score * 100) if max_score > 0 else 0, 1)

    # Create verification code (hash of student name + timestamp + secret)
    timestamp = datetime.now().isoformat()
    secret = "primary-source-trainer-2025"  # Secret key for verification
    verification_string = f"{submission.student_name}{timestamp}{secret}"
    verification_code = hashlib.sha256(verification_string.encode()).hexdigest()[:12]

    # Build report data
    report_data = {
        "student_name": submission.student_name,
        "student_email": submission.student_email,
        "submission_timestamp": timestamp,
        "verification_code": verification_code.upper(),
        "instructor_email": "yaniv.fox@biu.ac.il",
        "total_score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "scenarios_completed": len(submission.scenario_results),
        "scenario_results": [
            {
                "scenario_id": r.scenario_id,
                "score": r.score,
                "max_score": r.max_score,
                "topic": r.topic_label,
                "results": [
                    {
                        "node_id": res.node_id,
                        "correct": res.correct,
                        "student_classification": res.student_classification,
                        "correct_classification": res.correct_classification,
                        "feedback": res.feedback
                    }
                    for res in r.results
                ]
            }
            for r in submission.scenario_results
        ]
    }

    return {
        "success": True,
        "message": "Results ready for download",
        "report_data": report_data,
        "filename": f"primary-source-results-{verification_code.upper()}.json"
    }


@app.post("/api/generate-report")
def generate_text_report(submission: SessionSubmission):
    """
    Generate plain text report (backup if email fails).
    Returns text that student can copy and email manually.
    """
    report = format_plain_text_report(submission)

    return {
        "report": report,
        "instructor_email": os.getenv("INSTRUCTOR_EMAIL", "yaniv.fox@biu.ac.il")
    }


@app.get("/api/stats")
def get_stats():
    """
    Get statistics about available scenarios.
    Useful for showing progress (e.g., "3/10 scenarios completed").
    """
    difficulties = {}
    total_topics = 0

    for scenario in SCENARIOS:
        diff = scenario.difficulty
        difficulties[diff] = difficulties.get(diff, 0) + 1
        total_topics += len(scenario.topics)

    return {
        "total_scenarios": len(SCENARIOS),
        "difficulties": difficulties,
        "total_topics": total_topics,
        "avg_topics_per_scenario": round(total_topics / len(SCENARIOS), 1)
    }


# Development server startup
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
