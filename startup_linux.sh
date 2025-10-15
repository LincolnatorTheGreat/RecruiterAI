#!/bin/bash

# Set GEMINI_API_KEY (replace with your actual key)
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" == "YOUR_GEMINI_API_KEY_HERE" ]; then
    echo "ERROR: GEMINI_API_KEY is not set. Please edit this script and replace 'YOUR_GEMINI_API_KEY_HERE' with your actual Gemini API key."
    exit 1
fi

echo "Starting Streamlit application..."
python3 -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false &
STREAMLIT_PID=$!
echo "Streamlit app is running (PID: $STREAMLIT_PID). Opening in browser..."
sleep 5 # Give Streamlit a moment to start
xdg-open "http://localhost:8501" || gnome-open "http://localhost:8501" || open "http://localhost:8501" # Cross-desktop open

# Optional: Trap to kill streamlit on script exit
# trap "kill $STREAMLIT_PID" EXIT