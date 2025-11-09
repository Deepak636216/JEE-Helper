@echo off
echo Starting JEE Physics AI Tutor Backend...
cd /d "%~dp0\.."

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
)

REM Start the FastAPI server from backend directory
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
