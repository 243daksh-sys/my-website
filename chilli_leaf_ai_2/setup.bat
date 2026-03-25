@echo off
setlocal enabledelayedexpansion

echo =========================================
echo Chilli Leaf AI Setup Script
echo =========================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Python is not installed. Downloading Python 3.11...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe -OutFile python_installer.exe"
    
    echo [INFO] Installing Python 3.11 silently...
    start /wait python_installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    del python_installer.exe
    
    :: Refresh path variables to detect python
    call refreshenv >nul 2>&1
    
    :: Verify installation
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Python. Please install it manually from https://www.python.org/downloads/
        pause
        exit /b 1
    )
) else (
    echo [INFO] Python is already installed.
)

:: Create Virtual Environment if it doesn't exist
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
) else (
    echo [INFO] Virtual environment already exists.
)

:: Activate the environment and install dependencies
echo [INFO] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt

echo =========================================
echo [SUCCESS] Setup is complete!
echo =========================================
echo To start using the project:
echo 1. Activate the environment: venv\Scripts\activate
echo 2. Train the model: python train.py
echo 3. Run the web app: cd app ^& python app.py
echo =========================================
pause
