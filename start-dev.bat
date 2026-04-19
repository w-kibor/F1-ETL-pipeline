@echo off
REM F1 ETL Pipeline - Development Server Startup Script (Windows)
REM Starts both backend and frontend servers

echo.
echo ========================================================
echo Rocket Starting F1 ETL Pipeline ^(Development Mode^)
echo ========================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Checking dependencies...
pip install -r requirements.txt >nul 2>&1

REM Start backend in new terminal
echo.
echo Starting Backend Server...
echo    API: http://localhost:8000
echo    Docs: http://localhost:8000/docs
start cmd /k "python backend/main.py"

REM Wait for backend to start
timeout /t 2 /nobreak >nul

REM Start frontend in new terminal
echo.
echo Starting Frontend Server...
echo    Frontend: http://localhost:5173
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install >nul 2>&1
)

start cmd /k "npm run dev"

echo.
echo ========================================================
echo Both servers are running!
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo To stop the servers, close the command windows manually.
echo ========================================================
echo.
