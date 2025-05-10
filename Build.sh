#!/bin/bash

# Exit on errors
set -e

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python not found. Installing Python..."

    # For Linux (Debian/Ubuntu)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update
        sudo apt install -y python3 python3-pip

    # For macOS
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if ! command -v brew &>/dev/null; then
            echo "Homebrew not found. Installing..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            BREW_INSTALLED=1
        fi
        brew install python
    else
        echo "Unsupported OS."
        exit 1
    fi

    PYTHON_INSTALLED=1
else
    PYTHON_INSTALLED=0
fi

# Install required pip packages
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Run the Python build system with all passed arguments
echo "Building Meme-Mayhem..."
python3 __BUILD_SYS__.py "$@"

# Optional cleanup if Python was installed by the script
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

# Clean up build artifacts
echo "Cleaning up artifacts..."
rm -rf __pycache__
rm -f Main.spec Server.spec Client.spec
rm -rf build

echo "Done."
exit 0
