#!/bin/bash
# Install shell completion for AIDEV CLI

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
echo -e "${BLUE}=== AIDEV CLI Shell Completion Installer ===${NC}"
echo

# Detect shell
CURRENT_SHELL=$(basename "$SHELL")
echo -e "${YELLOW}Detected shell:${NC} $CURRENT_SHELL"

# Function to install completions
install_completion() {
    local shell=$1
    local force=$2

    # Ensure AIDEV is installed
    if ! command -v aidev &> /dev/null; then
        echo -e "${RED}Error: aidev command not found.${NC}"
        echo -e "Please install AIDEV first using: ${YELLOW}pip install aidev${NC}"
        exit 1
    fi

    local force_flag=""
    if [ "$force" = "true" ]; then
        force_flag="--force"
    fi

    echo -e "${YELLOW}Installing completions for $shell...${NC}"

    # Use aidev's built-in completion installer
    aidev install-completion --shell "$shell" $force_flag

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Completion installed successfully!${NC}"

        # Provide instructions
        if [ "$shell" = "bash" ]; then
            echo -e "${YELLOW}To enable completion, restart your terminal or run:${NC}"
            echo -e "  source ~/.bash_completion"
        elif [ "$shell" = "zsh" ]; then
            echo -e "${YELLOW}To enable completion, restart your terminal or run:${NC}"
            echo -e "  source ~/.zshrc"
        elif [ "$shell" = "fish" ]; then
            echo -e "${YELLOW}To enable completion, restart your terminal or run:${NC}"
            echo -e "  source ~/.config/fish/completions/aidev.fish"
        fi
    else
        echo -e "${RED}Failed to install completion.${NC}"
        exit 1
    fi
}

# Parse arguments
FORCE=false
SHELL_OVERRIDE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --force|-f)
            FORCE=true
            shift
            ;;
        --shell|-s)
            SHELL_OVERRIDE="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --shell, -s SHELL  Specify shell (bash, zsh, fish)"
            echo "  --force, -f        Force overwrite existing completion"
            echo "  --help, -h         Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help to see available options"
            exit 1
            ;;
    esac
done

# Use shell override if provided
if [ -n "$SHELL_OVERRIDE" ]; then
    CURRENT_SHELL="$SHELL_OVERRIDE"
fi

# Install completion based on detected shell
case $CURRENT_SHELL in
    bash)
        install_completion "bash" "$FORCE"
        ;;
    zsh)
        install_completion "zsh" "$FORCE"
        ;;
    fish)
        install_completion "fish" "$FORCE"
        ;;
    *)
        echo -e "${RED}Unsupported shell: $CURRENT_SHELL${NC}"
        echo -e "Supported shells: ${YELLOW}bash, zsh, fish${NC}"
        echo -e "You can specify a supported shell with: ${YELLOW}$0 --shell SHELL${NC}"
        exit 1
        ;;
esac

echo
echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}Tab completion is now available for the AIDEV CLI!${NC}"
echo -e "Try typing ${YELLOW}aidev ${NC} and then press TAB to see available commands."
echo -e "${GREEN}=============================================${NC}"
