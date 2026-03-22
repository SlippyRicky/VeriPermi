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
echo "[INFO] To stop the server, press Ctrl+C in this terminal."
echo ""

# Start a background process to open the browser once the server is ready
(
    # Wait for the server to be responsive
    MAX_ATTEMPTS=30
    for (( i=1; i<=$MAX_ATTEMPTS; i++ )); do
        if curl -s "http://localhost:$PORT" > /dev/null; then
            echo "[INFO] Server is up, opening browser..."
            APP_URL="http://localhost:$PORT"
            
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS: Prioritize Chromium as requested, then Edge, then default
                if [ -d "/Applications/Chromium.app" ]; then
                    echo "[INFO] Opening in Chromium..."
                    open -n -a "Chromium" --args --app="$APP_URL"
                    # Give it a moment to launch then force it to the front
                    sleep 2
                    osascript -e 'tell application "Chromium" to activate'
                elif [ -d "/Applications/Microsoft Edge.app" ]; then
                    echo "[INFO] Opening in Microsoft Edge..."
                    open -n -a "Microsoft Edge" --args --app="$APP_URL"
                    sleep 2
                    osascript -e 'tell application "Microsoft Edge" to activate'
                else
                    open "$APP_URL"
                fi
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                # Linux: Try chromium-browser or google-chrome
                if command -v chromium-browser &> /dev/null; then
                    chromium-browser --app="$APP_URL" &
                elif command -v google-chrome &> /dev/null; then
                    google-chrome --app="$APP_URL" &
                else
                    xdg-open "$APP_URL" &
                fi
            fi
            exit 0
        fi
        sleep 1
    done
    echo "[ERROR] Server failed to start within $MAX_ATTEMPTS seconds."
) &
BROWSER_PID=$!

# Run Streamlit in the foreground so we can see any errors
# We use the explicit path to the venv streamlit to avoid any path issues
VENV_STREAMLIT="./venv/bin/streamlit"
if [ ! -f "$VENV_STREAMLIT" ]; then
    VENV_STREAMLIT="python3 -m streamlit"
fi

if ! $VENV_STREAMLIT run App/app.py --server.port $PORT --server.headless true; then
    echo ""
    echo "==================================================="
    echo "       CRITICAL ERROR: APPLICATION CRASHED"
    echo "==================================================="
    echo "The application server has stopped unexpectedly."
    echo "Check if the 'App' directory and 'App/app.py' exist."
    echo ""
    read -p "Press Enter to close this window..."
fi

# Cleanup
kill $BROWSER_PID 2>/dev/null
