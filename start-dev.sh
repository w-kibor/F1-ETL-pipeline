#!/bin/bash

# F1 ETL Pipeline - Development Server Startup Script
# Starts both backend and frontend servers

echo "🚀 Starting F1 ETL Pipeline (Development Mode)"
echo "================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "📥 Checking dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Start backend
echo ""
echo "🔙 Starting Backend Server..."
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
python backend/main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Start frontend
echo ""
echo "🎨 Starting Frontend Server..."
echo "   Frontend: http://localhost:5173"
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📥 Installing frontend dependencies..."
    npm install > /dev/null 2>&1
fi

npm run dev &
FRONTEND_PID=$!

echo ""
echo "================================================"
echo "✅ Both servers are running!"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "================================================"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
