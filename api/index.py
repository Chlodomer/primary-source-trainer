from fastapi import FastAPI
from mangum import Mangum
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
sys.path.insert(0, backend_path)

# Import the app
from main import app

# Mangum handler for AWS Lambda/Vercel
handler = Mangum(app)
