"""
WSGI configuration for PythonAnywhere deployment.

PythonAnywhere uses WSGI, but FastAPI is an ASGI application.
This file uses the WSGIMiddleware adapter to bridge them.
"""

import sys
import os
from pathlib import Path

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/primary-source-trainer/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
from dotenv import load_dotenv
env_path = Path(project_home) / '.env'
load_dotenv(dotenv_path=env_path)

# Import the FastAPI app
from main import app

# Wrap the ASGI app with WSGIMiddleware for PythonAnywhere
from fastapi.middleware.wsgi import WSGIMiddleware

# This creates a WSGI-compatible application
application = WSGIMiddleware(app)
