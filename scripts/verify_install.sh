#!/bin/bash
# Verify installation of aidev CLI Assistant

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo "Verifying aidev installation..."
echo

# Check Python version
echo -n "Python: "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}$PYTHON_VERSION${NC}"
else
    echo -e "${RED}Not found${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if aidev is installed
echo -n "aidev package: "
if python3 -c "import importlib.metadata; print(importlib.metadata.version('aidev'))" 2>/dev/null; then
    echo -e "${GREEN}Installed${NC}"
else
    echo -e "${RED}Not installed${NC}"
    echo "Please install with: pip install aidev"
    exit 1
fi

# Check if aidev command works
echo -n "aidev command: "
if command -v aidev &> /dev/null; then
    AIDEV_VERSION=$(aidev --version)
    echo -e "${GREEN}$AIDEV_VERSION${NC}"
else
    echo -e "${RED}Not found${NC}"
    echo "The 'aidev' command was not found in your PATH"
    echo "Try reinstalling the package or check your PATH settings"
    exit 1
fi

# Check Ollama
echo -n "Ollama: "
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}Installed${NC}"
    echo "Available models:"
    ollama list
else
    echo -e "${RED}Not installed${NC}"
    echo "Please install Ollama from https://ollama.ai"
    exit 1
fi

echo
echo -e "${GREEN}All components verified!${NC}"
echo "Try running 'aidev hello' to get started."
