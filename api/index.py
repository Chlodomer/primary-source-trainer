import sys
import os
from pathlib import Path

# Add backend to path
backend_path = str(Path(__file__).parent.parent / 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import the app
from main import app
from mangum import Mangum

# Create the handler - Vercel expects this exact variable name
app_handler = Mangum(app, lifespan="off")

# Vercel entry point
def handler(event, context):
    return app_handler(event, context)
