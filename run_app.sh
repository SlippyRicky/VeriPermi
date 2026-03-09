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

# Determine OS for opening browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS: Open in default browser
    open "http://localhost:$PORT"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux: Try xdg-open
    if command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:$PORT" &
    fi
fi

# Run Streamlit (blocking)
streamlit run App/app.py --server.port $PORT --server.headless true
