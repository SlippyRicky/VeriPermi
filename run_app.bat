@echo off
SETLOCAL EnableDelayedExpansion

echo ===================================================
echo   Permis de Conduire - Flashcard App Initializer
echo ===================================================
echo.

:: 1. Check for Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in your system PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

:: 2. Setup Virtual Environment
IF NOT EXIST "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)

:: 3. Activate Virtual Environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

:: 4. Install Dependencies
echo [INFO] Installing required packages...
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

:: 5. Launch Application
echo [INFO] Starting the application...
echo [INFO] A browser window should open automatically.
echo [INFO] Leave this window open while using the app.
echo.

:: Run Streamlit in the background
start /B "" streamlit run App\app.py --server.port 8501 --server.headless true

echo [INFO] Waiting for Streamlit server to start...
timeout /t 4 /nobreak >nul

:: Open browser in "App Mode" (Standalone window without URL bar)
set APP_URL=http://localhost:8501

:: Try Chrome first, then Edge, then default
start chrome --app="%APP_URL%" 2>nul || start msedge --app="%APP_URL%" 2>nul || start "" "%APP_URL%"

pause
