@echo off
REM Verify installation of aidev CLI Assistant for Windows

echo Verifying aidev installation...
echo.

REM Check Python version
echo Python: 
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('python --version') do echo %%i
) else (
    echo Not found - Please install Python 3.8 or higher
    exit /b 1
)

REM Check if aidev is installed
echo aidev package: 
python -c "import importlib.metadata; print(importlib.metadata.version('aidev'))" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Not installed - Please install with: pip install aidev
    exit /b 1
)

REM Check if aidev command works
echo aidev command: 
where aidev >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('aidev --version') do echo %%i
) else (
    echo Not found - The 'aidev' command was not found in your PATH
    echo Try reinstalling the package or check your PATH settings
    exit /b 1
)

REM Check Ollama
echo Ollama: 
where ollama >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Installed
    echo Available models:
    ollama list
) else (
    echo Not installed - Please install Ollama from https://ollama.ai
    exit /b 1
)

echo.
echo All components verified!
echo Try running 'aidev hello' to get started. 