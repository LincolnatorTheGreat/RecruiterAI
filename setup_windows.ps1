# Check if Python is installed (basic check)
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Please install Python 3.x from python.org and rerun this script." -ForegroundColor Red
    exit 1
}

# Create a virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Green
python -m venv recruiterAIhost

# Activate the virtual environment and install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Green
.\recruiterAIhost\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# API Key setup
$apiKey = [System.Environment]::GetEnvironmentVariable('GEMINI_API_KEY_RECAI', 'User')
if ($apiKey) {
    $response = Read-Host "GEMINI_API_KEY_RECAI is already set. Do you want to change it? (y/n)"
    if ($response -eq 'y' -or $response -eq 'yes') {
        $newApiKey = Read-Host "Enter your new Gemini API key"
        setx GEMINI_API_KEY_RECAI $newApiKey
    }
} else {
    $newApiKey = Read-Host "Enter your Gemini API key"
    setx GEMINI_API_KEY_RECAI $newApiKey
}

# Install Pandoc
Write-Host "Installing Pandoc..." -ForegroundColor Green
# Check if Pandoc is already installed
if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    # Download and install Pandoc (using winget for simplicity if available, otherwise direct download)
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id Pandoc.Pandoc --source winget
    } else {
        Write-Host "winget not found. Please install Pandoc manually from https://pandoc.org/installing.html" -ForegroundColor Yellow
    }
} else {
    Write-Host "Pandoc is already installed." -ForegroundColor Green
}

# Create desktop shortcut for startup_windows.ps1
Write-Host "Creating desktop shortcut..." -ForegroundColor Green
$shell = New-Object -ComObject WScript.Shell
$shortcutPath = "$env:USERPROFILE\Desktop\RecruiterAI_Start.lnk"
$targetPath = (Get-Location).Path + "\startup_windows.ps1"
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$targetPath`""
$shortcut.Description = "Start RecruiterAI Streamlit App"
$shortcut.WorkingDirectory = (Get-Location).Path
$shortcut.Save()
Write-Host "Desktop shortcut 'RecruiterAI_Start.lnk' created." -ForegroundColor Green

Write-Host "Installation complete. You can now run the application using the desktop shortcut." -ForegroundColor Green