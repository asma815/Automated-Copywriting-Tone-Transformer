@echo off
title Automated Copywriting & Tone Transformer
cd /d "%~dp0"

echo ==============================================
echo  DecodeLabs Project 2 - Copywriting Transformer
echo ==============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found. Install Python and enable "Add Python to PATH".
    pause
    exit /b 1
)

where ollama >nul 2>nul
if errorlevel 1 (
    echo WARNING: Ollama command was not found in PATH.
    echo Please open/check the Ollama app. The app needs Ollama running.
    echo.
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating the project's Python environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Could not create the virtual environment.
        pause
        exit /b 1
    )
)

echo Installing/checking required packages...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Package installation failed. Check your internet connection.
    pause
    exit /b 1
)

echo.
echo Starting Streamlit...
".venv\Scripts\python.exe" -m streamlit run app.py
echo.
echo App stopped. You can close this window.
pause
