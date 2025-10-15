# Set GEMINI_API_KEY (replace with your actual key)
$env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

if (-not $env:GEMINI_API_KEY -or $env:GEMINI_API_KEY -eq "YOUR_GEMINI_API_KEY_HERE") {
    Write-Host "ERROR: GEMINI_API_KEY is not set. Please edit this script and replace 'YOUR_GEMINI_API_KEY_HERE' with your actual Gemini API key." -ForegroundColor Red
    exit 1
}

Write-Host "Starting Streamlit application..." -ForegroundColor Green
Start-Process python -ArgumentList "-m", "streamlit", "run", "app.py", "--server.port", "8501", "--browser.gatherUsageStats", "false" -NoNewWindow
Write-Host "Streamlit app is running. Opening in browser..." -ForegroundColor Green
Start-Sleep -Seconds 5 # Give Streamlit a moment to start
Start-Process "http://localhost:8501"