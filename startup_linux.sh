#!/bin/bash

# Activate the virtual environment
source recruiterAIhost/bin/activate

# Check if the virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "ERROR: Python virtual environment is not activated. Please run the setup script."
    exit 1
fi

# Set GEMINI_API_KEY_RECAI from GEMINI_API_KEY_RECAI
export GEMINI_API_KEY_RECAI="$GEMINI_API_KEY_RECAI"

if [ -z "$GEMINI_API_KEY_RECAI" ]; then
    echo "ERROR: GEMINI_API_KEY_RECAI is not set. Please run the setup script to set it."
    exit 1
fi

echo "Starting Streamlit application..."
python3 -m streamlit run app.py --server.runOnSave true --server.port 8501 --browser.gatherUsageStats false &
STREAMLIT_PID=$!
echo "Streamlit app is running (PID: $STREAMLIT_PID). Opening in browser..."
sleep 5 # Give Streamlit a moment to start
xdg-open "http://localhost:8501" || gnome-open "http://localhost:8501" || open "http://localhost:8501" # Cross-desktop open

# Optional: Trap to kill streamlit on script exit
# trap "kill $STREAMLIT_PID" EXIT
