# AI-Powered CLI Assistant

An AI-powered command-line assistant for developers that provides code generation, terminal command suggestions, documentation search, git assistance, and API testing capabilities - all running locally using Hugging Face's open-source models or Ollama's local LLM models.

## Features

- **Code Generation**: Generate code snippets from natural language descriptions
- **Terminal Commands**: Get suggestions and explanations for complex terminal operations
- **Documentation Search**: Search and summarize documentation locally
- **Git Assistance**: Generate commit messages and PR descriptions
- **API Testing**: Test and format API requests easily

## Architecture

This CLI tool can operate in two modes:

1. **Standalone Mode** (recommended): Uses local AI models directly without requiring a backend server. This is the default mode and uses models like DeepSeek and other Ollama-compatible models.

2. **Client-Server Mode**: Connects to a backend FastAPI service that hosts Hugging Face models. This mode is optional and can be used if you prefer to use Hugging Face models or need advanced features.

The standalone mode is simpler and faster to set up, while the client-server mode provides more flexibility.

## Installation

### Prerequisites

- Python 3.8+
- Git
- Ollama (optional but recommended for standalone mode)

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

5. (Optional) For standalone mode with Ollama:
   ```bash
   # Install Ollama from https://ollama.ai
   # Then pull the DeepSeek model
   ollama pull deepseek-r1:7b
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

### Using Local Models with Ollama

All commands now use local LLM models by default via Ollama. To use the backend API instead, use the `--api` flag:

```bash
# Generate code using local model (default)
aidev code generate "Create a Python function to calculate factorial"

# Generate code using the backend API
aidev code generate --api "Create a Python function to calculate factorial"

# Get terminal command suggestions locally (default)
aidev terminal suggest "find files modified in the last week"

# Search documentation with a local model (default)
aidev docs search "async functions in javascript"

# Generate commit message using local model (default)
aidev git generate-commit
```

Additional options:

```bash
# Select a specific Ollama model
aidev terminal suggest --model "deepseek-r1:7b" "find large files"

# Disable streaming output
aidev code generate --no-stream "Create a binary search function"

# Hide model thinking process
aidev terminal explain --no-thinking "grep -r pattern ."
```

For Ollama setup and more details, see [docs/ollama.md](docs/ollama.md).

## Adding New Models

The CLI tool has a modular architecture that makes it easy to add new AI models:

1. Create a new model implementation in `cli/ai_agent_models/`
2. Register the model in `cli/ai_agent_models/__init__.py`
3. Use the model by specifying it with the `--model` flag

For detailed instructions, see [cli/ai_agent_models/README.md](cli/ai_agent_models/README.md).

## Development

### Project Structure

```
ai-cli-assistant/
├── cli/                   # CLI interface code
│   ├── commands/          # Command implementations
│   ├── utils/             # Utilities
│   ├── ai_agent_models/   # AI model implementations
│   │   ├── base_model.py  # Base abstract class for models
│   │   └── ollama_*.py    # Model implementations
│   └── main.py            # Entry point
├── backend/               # Optional FastAPI backend service
│   ├── api/               # API endpoints
│   ├── models/            # Data models
│   ├── services/          # Business logic and services
│   └── main.py            # FastAPI application
├── shared/                # Shared code between CLI and backend
├── tests/                 # Test suite
│   ├── conftest.py        # Pytest fixtures
│   ├── test_api.py        # Backend API tests
│   ├── test_cli.py        # CLI interface tests
│   └── test_models.py     # Model integration tests
└── requirements.txt       # Project dependencies
```

### Running Tests

You can run tests using the provided script or directly with pytest:

```bash
# Run fast tests (skipping those that use real AI models)
python tests/run_tests.py

# Run all tests including slow ones
python tests/run_tests.py --slow

# Run with verbose output
python tests/run_tests.py -v

# Run a specific test file
python tests/run_tests.py --path tests/test_cli.py

# Using pytest directly
pytest -k "not slow"  # Skip slow tests
pytest                # Run all tests
pytest -v             # Verbose output
pytest tests/test_api.py::test_health_endpoint  # Run specific test
```

For more information about testing, see the [tests/README.md](tests/README.md) file.

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