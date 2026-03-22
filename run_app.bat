@echo off
SETLOCAL EnableDelayedExpansion

echo ===================================================
echo   Permis de Conduire - Flashcard App Initializer
echo ===================================================
echo.

:: Navigate to the directory containing this script
cd /d "%~dp0"

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

:: 5. Handle Port conflicts
set PORT=8501
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /R /C:"TCP.*:%PORT% "') do (
    if "%%a" NEQ "0" (
        echo [INFO] Stopping existing app instance on port %PORT% ^(PID: %%a^)...
        taskkill /F /PID %%a >nul 2>&1
        timeout /t 1 /nobreak >nul
    )
)

:: 6. Launch Application
echo [INFO] Starting the application server...
echo [INFO] To stop the server, press Ctrl+C in this terminal.
echo.

:: Start a background process to open the browser after a delay
set APP_URL=http://localhost:%PORT%
start /B cmd /c "timeout /t 4 /nobreak >nul & (start chrome --app="%APP_URL%" 2>nul || start msedge --app="%APP_URL%" 2>nul || start "" "%APP_URL%")"

:: Run Streamlit in the foreground so we can see any errors
set VENV_STREAMLIT=venv\Scripts\streamlit.exe
if not exist "%VENV_STREAMLIT%" (
    set VENV_STREAMLIT=python -m streamlit
)

%VENV_STREAMLIT% run App\app.py --server.port %PORT% --server.headless true
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ===================================================
    echo        CRITICAL ERROR: APPLICATION CRASHED
    echo ===================================================
    echo The application server has stopped unexpectedly.
    echo Please check the error messages above.
    echo.
    pause
)
