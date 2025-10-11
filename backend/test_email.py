"""
Test script for email functionality.
Run this to verify SendGrid is configured correctly.
"""

from datetime import datetime
from models import SessionSubmission, ScenarioResult, GradingResult
from email_service import send_results_email
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create test data
test_submission = SessionSubmission(
    student_name="Test Student",
    student_email="test@example.com",
    timestamp=datetime.now(),
    scenario_results=[
        ScenarioResult(
            scenario_id="test_scenario_1",
            score=8,
            max_score=10,
            topic_label="Carolingian Renaissance",
            results=[
                GradingResult(
                    node_id="node_1",
                    student_answer="primary",
                    correct_answer="primary",
                    is_correct=True,
                    points=1,
                    feedback="Correct! This is a primary source."
                ),
                GradingResult(
                    node_id="node_2",
                    student_answer="secondary",
                    correct_answer="primary",
                    is_correct=False,
                    points=0,
                    feedback="Incorrect. This is actually a primary source."
                )
            ]
        )
    ]
)

print("Testing email functionality...")
print(f"Sending test email to: {os.getenv('INSTRUCTOR_EMAIL')}")
print(f"From: {os.getenv('SENDER_EMAIL')}")
print()

result = send_results_email(test_submission, os.getenv('INSTRUCTOR_EMAIL'))

print("Result:")
print(f"  Success: {result['success']}")
print(f"  Message: {result['message']}")

if result['success']:
    print("\n✅ Email sent successfully! Check your inbox at foxyaniv@gmail.com")
else:
    print("\n❌ Email failed. Check the error message above.")
