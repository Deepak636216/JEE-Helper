@echo off
echo Starting JEE Physics AI Tutor Frontend...
cd /d "%~dp0\.."
cd frontend

REM Install dependencies if needed
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

REM Start the Vite dev server
npm run dev

pause
