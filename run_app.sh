#!/bin/bash

echo "==================================================="
echo "  Permis de Conduire - Flashcard App Initializer"
echo "==================================================="
echo ""

# Navigate to the directory containing this script
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# 1. Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 could not be found."
    echo "Please install Python 3 (https://www.python.org/downloads/) or via Homebrew/APT."
    exit 1
fi

# 2. Setup Virtual Environment
if [ ! -d "venv" ]; then
    echo "[INFO] Creating Python virtual environment..."
    python3 -m venv venv
fi

# 3. Activate Virtual Environment
echo "[INFO] Activating virtual environment..."
source venv/bin/activate

# 4. Install Dependencies
echo "[INFO] Installing required packages..."
python3 -m pip install --upgrade pip -q
pip install -r requirements.txt -q

# 5. Handle Port conflicts
PORT=8501
PID=$(lsof -t -i :$PORT 2>/dev/null)
if [ ! -z "$PID" ]; then
    echo "[INFO] Stopping existing app instance on port $PORT..."
    kill -9 $PID
    sleep 1
fi

# 6. Launch Application
echo "[INFO] Starting the application server..."
echo "[INFO] A browser window should open automatically."
echo "[INFO] To stop the server, press Ctrl+C in this terminal."
echo ""

# Determine OS for opening browser in APP mode (no URL bar, standalone window)
APP_URL="http://localhost:$PORT"

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS: Try Chrome first, then Edge, then default
    if [ -d "/Applications/Google Chrome.app" ]; then
        open -n -a "Google Chrome" --args --app="$APP_URL"
    elif [ -d "/Applications/Microsoft Edge.app" ]; then
        open -n -a "Microsoft Edge" --args --app="$APP_URL"
    else
        open "$APP_URL"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux: Try google-chrome
    if command -v google-chrome &> /dev/null; then
        google-chrome --app="$APP_URL" &
    else
        xdg-open "$APP_URL" &
    fi
fi

# Run Streamlit (blocking)
streamlit run App/app.py --server.port $PORT --server.headless true
