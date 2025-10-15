# Activate the virtual environment
.\recruiterAIhost\Scripts\Activate.ps1

# Set GEMINI_API_KEY from GEMINI_API_KEY_RECAI
$env:GEMINI_API_KEY = [System.Environment]::GetEnvironmentVariable('GEMINI_API_KEY_RECAI', 'User')

if (-not $env:GEMINI_API_KEY) {
    Write-Host "ERROR: GEMINI_API_KEY is not set. Please run the setup script to set it." -ForegroundColor Red
    exit 1
}

Write-Host "Starting Streamlit application..." -ForegroundColor Green
Start-Process python -ArgumentList "-m", "streamlit", "run", "app.py", "--server.port", "8501", "--browser.gatherUsageStats", "false" -NoNewWindow
Write-Host "Streamlit app is running. Opening in browser..." -ForegroundColor Green
Start-Sleep -Seconds 5 # Give Streamlit a moment to start
Start-Process "http://localhost:8501"