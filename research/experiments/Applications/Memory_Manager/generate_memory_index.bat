@echo off
REM This script generates the memory index for Lyra's vector-based memory system

echo Setting up memory index generation environment...

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or later.
    exit /b 1
)

echo Installing required packages...
pip install -r "%~dp0\core\discord_bot_requirements.txt"

echo.
echo Generating memory index...
cd "%~dp0"
python "%~dp0\generate_memory_index.py"

echo.
echo Process complete. Press any key to exit.
pause > nul
