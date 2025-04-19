#!/bin/bash
# Script to perform a clean installation of aidev with minimal dependencies

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'  # No Color

echo -e "${GREEN}Starting clean installation of aidev...${NC}"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Create and activate a fresh virtual environment
echo -e "${YELLOW}Creating a new virtual environment...${NC}"
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip and setuptools...${NC}"
pip install --upgrade pip setuptools wheel

# Install minimal core dependencies first
echo -e "${YELLOW}Installing core dependencies...${NC}"
pip install typer rich click httpx pydantic jinja2 requests shellingham

# Check if Ollama is installed
echo -e "${YELLOW}Checking for Ollama...${NC}"
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}Ollama is installed.${NC}"
    
    # Check if DeepSeek model is available
    if ollama list | grep -q "deepseek-r1:7b"; then
        echo -e "${GREEN}DeepSeek-R1 7B model is available.${NC}"
    else
        echo -e "${YELLOW}DeepSeek-R1 7B model is not found. Would you like to install it now? (y/n)${NC}"
        read -r answer
        if [[ "$answer" =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Installing DeepSeek-R1 7B model...${NC}"
            ollama pull deepseek-r1:7b
        else
            echo -e "${YELLOW}Skipping model installation. You'll need to install a model later with 'ollama pull <model-name>'${NC}"
        fi
    fi
else
    echo -e "${YELLOW}Ollama is not installed. This tool works best with Ollama.${NC}"
    echo -e "${YELLOW}Visit https://ollama.ai/ to install Ollama.${NC}"
fi

# Install aidev in development mode
echo -e "${YELLOW}Installing aidev...${NC}"
pip install -e .

# Verify installation
echo -e "${YELLOW}Verifying installation...${NC}"
if command -v aidev &> /dev/null; then
    VERSION=$(aidev --version)
    echo -e "${GREEN}aidev installed successfully: $VERSION${NC}"
else
    echo -e "${RED}Installation failed. The 'aidev' command is not available.${NC}"
    exit 1
fi

echo -e "${GREEN}Installation complete!${NC}"
echo -e "To use aidev, make sure the virtual environment is activated:"
echo -e "    source .venv/bin/activate"
echo -e "Try running 'aidev hello' to get started." 