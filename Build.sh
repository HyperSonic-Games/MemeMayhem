#!/bin/bash

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python not found. Installing Python..."
    
    # Install Python (For Linux, using apt for Ubuntu/Debian-based systems)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update
        sudo apt install -y python3 python3-pip
    # For macOS, using Homebrew
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if ! command -v brew &>/dev/null; then
            echo "Homebrew not found, installing it..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            BREW_INSTALLED=1
        fi
        brew install python
    else
        echo "Unsupported OS"
        exit 1
    fi
    
    PYTHON_INSTALLED=1
else
    PYTHON_INSTALLED=0
fi

# Install required pip packages
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Build the project
echo "Building Meme-Mayhem..."
python3 build.py

# Cleanup
if [[ "$PYTHON_INSTALLED" -eq 1 ]]; then
    echo "Uninstalling pip packages..."
    pip3 freeze | xargs pip3 uninstall -y
    
    echo "Uninstalling Python..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get remove --purge -y python3 python3-pip
        sudo apt-get autoremove -y
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew uninstall python
        if [[ "$BREW_INSTALLED" -eq 1 ]]; then
            echo "Uninstalling Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
        fi
    fi
fi

echo "Build complete. Cleaning up..."
rm -rf __pycache__

echo "Done."
exit 0
