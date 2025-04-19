@echo off
REM Script to perform a clean installation of aidev with minimal dependencies
REM This helps avoid dependency issues with conflicting package versions

echo Starting clean installation of aidev...

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in your PATH. Please install Python 3.8 or higher.
    exit /b 1
)

REM Create and activate a fresh virtual environment
echo Creating a new virtual environment...
python -m venv .venv
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install minimal dependencies directly from pyproject.toml
echo Installing aidev with minimal dependencies...
pip install -e .

REM Verify installation
echo Verifying installation...
where aidev >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('aidev --version') do set VERSION=%%i
    echo aidev installed successfully: %VERSION%
) else (
    echo Installation failed. The 'aidev' command is not available.
    exit /b 1
)

echo.
echo Installation complete!
echo To use aidev, make sure the virtual environment is activated:
echo     call .venv\Scripts\activate.bat
echo Try running 'aidev hello' to get started. 