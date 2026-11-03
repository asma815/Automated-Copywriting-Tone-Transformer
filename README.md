# Automated Copywriting & Tone Transformer

**DecodeLabs Generative AI Internship — Project 2**

## Goal
Generate marketing copy from a raw product description for LinkedIn, Instagram, or Email.

## Features
- Product name and description inputs
- Platform selection: LinkedIn, Instagram, Email
- Tone selection: Professional, Friendly, Creative, Persuasive, Informative
- Dynamic prompt template using user-provided variables
- Temperature and Top-P inference settings
- Automatically detects models already installed in Ollama
- Download generated copy as a `.txt` file
- No paid API key required

## Requirements
- Windows
- Python installed and available as `python`
- Ollama installed and running
- At least one model already downloaded in Ollama

## Run
1. Keep the Ollama application running.
2. Double-click `run_project.bat`.
3. Wait for the app to open in your browser.

If the batch file does not open, open PowerShell in this folder and run:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

To check your installed Ollama models:
```powershell
ollama list
```

If no model is installed, you can download a small model, for example:
```powershell
ollama pull qwen2.5:1.5b
```

## Notes
- This application uses the local Ollama API; it does not call a paid cloud API.
- The first installation of Python packages requires internet access.
- The Ollama model must be installed on the computer before generation.
- Output quality and speed depend on the local model and computer.
