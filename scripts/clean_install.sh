#!/bin/bash
# Script to perform a clean installation of aidev with minimal dependencies
# This helps avoid dependency issues with conflicting package versions

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'  # No Color

echo -e "${GREEN}Starting clean installation of aidev...${NC}"

# Check if virtualenv is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Create and activate a fresh virtual environment
echo -e "${YELLOW}Creating a new virtual environment...${NC}"
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install minimal dependencies directly from pyproject.toml
echo -e "${YELLOW}Installing aidev with minimal dependencies...${NC}"
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