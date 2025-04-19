#!/bin/bash
# Script to install and configure pre-commit hooks

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'  # No Color

echo -e "${GREEN}Setting up pre-commit hooks for aidev...${NC}"

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo -e "${YELLOW}pre-commit is not installed. Installing...${NC}"
    pip install pre-commit
    if ! command -v pre-commit &> /dev/null; then
        echo -e "${RED}Failed to install pre-commit. Please install it manually with 'pip install pre-commit'${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}pre-commit is already installed.${NC}"
fi

# Check if .pre-commit-config.yaml exists
if [ ! -f .pre-commit-config.yaml ]; then
    echo -e "${RED}.pre-commit-config.yaml not found. Please ensure you're running this script from the project root.${NC}"
    exit 1
fi

# Ensure we're in the project root (where .git directory exists)
if [ ! -d .git ]; then
    echo -e "${RED}.git directory not found. Please ensure you're running this script from the project root.${NC}"
    exit 1
fi

# Install the pre-commit hooks
echo -e "${YELLOW}Installing pre-commit hooks...${NC}"
pre-commit install

# Install additional dependencies for hooks
echo -e "${YELLOW}Installing additional dependencies for hooks...${NC}"
pip install black flake8 flake8-docstrings isort mypy types-requests

# Run pre-commit once against all files to ensure everything is set up correctly
echo -e "${YELLOW}Running initial pre-commit check against all files...${NC}"
pre-commit run --all-files || true

echo -e "${GREEN}Pre-commit hooks have been successfully installed!${NC}"
echo -e "The following checks will now run automatically on commit:"
echo -e "  - Trailing whitespace removal"
echo -e "  - End of file fixer"
echo -e "  - YAML syntax checking"
echo -e "  - Large file checks"
echo -e "  - Debug statement checks"
echo -e "  - TOML syntax checking"
echo -e "  - Merge conflict detection"
echo -e "  - Black (code formatting)"
echo -e "  - isort (import sorting)"
echo -e "  - flake8 (linting)"
echo -e "  - mypy (type checking)"
echo -e ""
echo -e "You can manually run these checks with: ${YELLOW}pre-commit run --all-files${NC}" 