# AI-Powered CLI Assistant

An AI-powered command-line assistant for developers that provides code generation, terminal command suggestions, documentation search, git assistance, and API testing capabilities - all running locally using Hugging Face's open-source models.

## Features

- **Code Generation**: Generate code snippets from natural language descriptions
- **Terminal Commands**: Get suggestions and explanations for complex terminal operations
- **Documentation Search**: Search and summarize documentation locally
- **Git Assistance**: Generate commit messages and PR descriptions
- **API Testing**: Test and format API requests easily

## Installation

### Prerequisites

- Python 3.8+
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-cli-assistant.git
   cd ai-cli-assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install the CLI tool in development mode:
   ```bash
   pip install -e .
   ```

## Usage

You can use the CLI tool with the `aidev` command or by running the Python module directly with `python -m cli.main`.

### Basic Commands

```bash
# Show help and available commands
aidev --help

# Test that the CLI is working
aidev hello
```

### Code Generation

```bash
# Generate a Python function to parse JSON
aidev code generate "Create a function that parses a JSON file and returns a dictionary"

# Generate JavaScript code and save to a file
aidev code generate "Create a React component that displays a todo list" --language javascript --output todo.js

# Explain existing code
aidev code explain path/to/file.py
```

### Terminal Command Help

```bash
# Get command suggestions based on what you want to do
aidev terminal suggest "find all files containing a specific text"

# Explain what a command does
aidev terminal explain ls -la
aidev terminal explain "grep -r pattern ."
```

### Git Operations

```bash
# Generate commit messages based on your changes
aidev git generate-commit

# Generate a pull request description
aidev git pr-description
```

### Documentation Search

```bash
# Search documentation for specific terms
aidev docs search list python

# Limit search to a specific language
aidev docs search function --language javascript

# Summarize a documentation file
aidev docs summarize README.md
```

### API Testing

```bash
# Make a simple GET request
aidev api request https://jsonplaceholder.typicode.com/posts/1

# Make a POST request with data
aidev api request https://jsonplaceholder.typicode.com/posts --method POST --data '{"title":"foo","body":"bar","userId":1}'

# Save a request for future use
aidev api request https://jsonplaceholder.typicode.com/posts/1 --save my-request

# List saved requests
aidev api list-saved

# Load and execute a saved request
aidev api load my-request --execute
```

## Development

### Project Structure

```
ai-cli-assistant/
├── cli/                 # CLI interface code
│   ├── commands/        # Command implementations
│   ├── utils/           # Utilities
│   └── main.py          # Entry point
├── backend/             # FastAPI backend service
├── shared/              # Shared code
└── tests/               # Tests
```

### Running Tests

```bash
pytest
```

### Linting and Formatting

```bash
# Format code with Black
black .

# Check imports with isort
isort .

# Run linting checks
flake8

# Type checking
mypy cli backend
```

## License

MIT License