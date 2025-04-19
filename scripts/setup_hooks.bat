@echo off
REM Script to install and configure pre-commit hooks for Windows

echo Setting up pre-commit hooks for aidev...

REM Check if pre-commit is installed
where pre-commit >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo pre-commit is not installed. Installing...
    pip install pre-commit
    
    where pre-commit >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install pre-commit. Please install it manually with 'pip install pre-commit'
        exit /b 1
    )
) else (
    echo pre-commit is already installed.
)

REM Check if .pre-commit-config.yaml exists
if not exist .pre-commit-config.yaml (
    echo .pre-commit-config.yaml not found. Please ensure you're running this script from the project root.
    exit /b 1
)

REM Ensure we're in the project root (where .git directory exists)
if not exist .git (
    echo .git directory not found. Please ensure you're running this script from the project root.
    exit /b 1
)

REM Install the pre-commit hooks
echo Installing pre-commit hooks...
pre-commit install

REM Install additional dependencies for hooks
echo Installing additional dependencies for hooks...
pip install black flake8 flake8-docstrings isort mypy types-requests

REM Run pre-commit once against all files to ensure everything is set up correctly
echo Running initial pre-commit check against all files...
pre-commit run --all-files

echo.
echo Pre-commit hooks have been successfully installed!
echo The following checks will now run automatically on commit:
echo   - Trailing whitespace removal
echo   - End of file fixer
echo   - YAML syntax checking
echo   - Large file checks
echo   - Debug statement checks
echo   - TOML syntax checking
echo   - Merge conflict detection
echo   - Black (code formatting)
echo   - isort (import sorting)
echo   - flake8 (linting)
echo   - mypy (type checking)
echo.
echo You can manually run these checks with: pre-commit run --all-files 