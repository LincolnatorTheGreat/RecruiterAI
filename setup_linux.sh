#!/bin/bash

# Check if Python is installed (basic check)
if ! command -v python3 &> /dev/null
then
    echo "Python 3 not found. Please install Python 3.x and rerun this script."
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install streamlit google-generativeai PyPDF2 pypandoc

# Install Pandoc
echo "Installing Pandoc..."
if ! command -v pandoc &> /dev/null
then
    # Install Pandoc using apt (for Debian/Ubuntu) or yum/dnf (for Fedora/RHEL)
    if command -v apt &> /dev/null
then
        sudo apt update
        sudo apt install -y pandoc
    elif command -v yum &> /dev/null
then
        sudo yum install -y pandoc
    elif command -v dnf &> /dev/null
then
        sudo dnf install -y pandoc
    else
        echo "Could not determine package manager. Please install Pandoc manually from https://pandoc.org/installing.html"
    fi
else
    echo "Pandoc is already installed."
fi

# Create desktop shortcut for startup_linux.sh
echo "Creating desktop shortcut..."
DESKTOP_FILE="$HOME/Desktop/RecruiterAI_Start.desktop"
CURRENT_DIR=$(pwd)
STARTUP_SCRIPT="$CURRENT_DIR/startup_linux.sh"

echo "[Desktop Entry]" > "$DESKTOP_FILE"
echo "Version=1.0" >> "$DESKTOP_FILE"
echo "Type=Application" >> "$DESKTOP_FILE"
echo "Name=RecruiterAI Start" >> "$DESKTOP_FILE"
echo "Exec=bash \"$STARTUP_SCRIPT\"" >> "$DESKTOP_FILE"
echo "Icon=utilities-terminal" >> "$DESKTOP_FILE" # Generic icon
echo "Terminal=true" >> "$DESKTOP_FILE" # Run in terminal
echo "Path=$CURRENT_DIR" >> "$DESKTOP_FILE"
chmod +x "$DESKTOP_FILE"
echo "Desktop shortcut 'RecruiterAI_Start.desktop' created. You might need to make it executable or trust it depending on your desktop environment."

echo "Installation complete. You can now run the application using the desktop shortcut." 
