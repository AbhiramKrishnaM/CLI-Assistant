#!/bin/bash
# Script to format Python code with black and isort

set -e

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual environment not activated. Activating venv..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "Virtual environment not found. Please create one first."
        echo "Run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        exit 1
    fi
fi

# Check if black and isort are installed
if ! command -v black &> /dev/null || ! command -v isort &> /dev/null; then
    echo "Installing black and isort..."
    pip install black isort
fi

echo "Formatting code with black..."
black .

echo "Sorting imports with isort..."
isort .

echo "All done! ✨ 🍰 ✨"
echo "Your code is now properly formatted."
