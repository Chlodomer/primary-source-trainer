#!/bin/bash

# Primary Source Trainer - Quick Start Script
# This script starts both backend and frontend servers

echo "🚀 Starting Primary Source Trainer..."
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Start backend
echo "📚 Starting backend server..."
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate venv and install dependencies
source venv/bin/activate
pip install -q -r requirements.txt

# Start backend in background
python main.py &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID) on http://localhost:8000"

cd ..

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start frontend in background
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID) on http://localhost:3000"

cd ..

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎓 Primary Source Trainer is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
