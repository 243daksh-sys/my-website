#!/bin/bash
echo "========================================="
echo "Chilli Leaf AI Setup Script"
echo "========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "[INFO] Python 3 is not installed."
    echo "[INFO] Please install Python 3.11+ using your package manager (e.g., brew install python3, or sudo apt install python3)"
    exit 1
else
    echo "[INFO] Python 3 is already installed."
fi

# Create Virtual Environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[INFO] Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "[INFO] Virtual environment already exists."
fi

# Activate the environment and install dependencies
echo "[INFO] Activating virtual environment and installing dependencies..."
source venv/bin/activate

python3 -m pip install --upgrade pip
pip install -r requirements.txt

echo "========================================="
echo "[SUCCESS] Setup is complete!"
echo "========================================="
echo "To start using the project:"
echo "1. Activate the environment: source venv/bin/activate"
echo "2. Train the model: python train.py"
echo "3. Run the web app: cd app && python app.py"
echo "========================================="
