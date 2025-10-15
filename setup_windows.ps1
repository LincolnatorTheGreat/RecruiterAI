# Check if Python is installed (basic check)
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Please install Python 3.x from python.org and rerun this script." -ForegroundColor Red
    exit 1
}

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Green
python -m pip install --upgrade pip
python -m pip install streamlit google-generativeai PyPDF2 pypandoc

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