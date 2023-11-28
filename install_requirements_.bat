@echo off

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b
)

REM Install required Python packages
pip install tkinter
pip install pypiwin32
pip install random
pip install string

echo Requirements installed successfully.
pause
exit /b
