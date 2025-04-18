# AI CLI Assistant - Command Line Interface

This directory contains the CLI component of the AI-powered assistant for developers.

## Running the CLI

There are two ways to run the CLI tool:

1. **Using the installed entry point**:
   ```bash
   # After installing with pip install -e .
   aidev [command]
   ```

2. **Directly with Python**:
   ```bash
   # From the project root
   python -m cli.main [command]
   
   # From within the cli directory
   python main.py [command]
   ```

## Command Groups

The CLI is organized into several command groups:

- `code`: Code generation and explanation
- `terminal`: Terminal command suggestions and explanations
- `git`: Git operation assistance
- `docs`: Documentation search and summarization
- `api`: API request testing and formatting

## Testing Commands

Here are some examples to test each feature:

### Basic

```bash
# Show the welcome message and available commands
python -m cli.main hello

# Show help for all commands
python -m cli.main --help
```

### Code Commands

```bash
# Generate Python code
python -m cli.main code generate "function to calculate Fibonacci sequence"

# Generate JavaScript and save to file
python -m cli.main code generate "function to sort an array" --language javascript --output sort.js

# Explain code in a file
python -m cli.main code explain cli/main.py
```

### Terminal Commands

```bash
# Get command suggestions
python -m cli.main terminal suggest "find files modified in the last 24 hours"

# Get command suggestions for Windows
python -m cli.main terminal suggest "list running processes" --platform windows

# Explain a command
python -m cli.main terminal explain grep -r "pattern" .
```

### Git Commands

```bash
# Generate commit message
python -m cli.main git generate-commit

# Generate descriptive commit message with files
python -m cli.main git generate-commit --message-type descriptive --files

# Generate PR description
python -m cli.main git pr-description
```

### Documentation Commands

```bash
# Search docs for a term
python -m cli.main docs search function

# Search with language filter
python -m cli.main docs search array --language javascript --max 3

# Summarize a README file
python -m cli.main docs summarize README.md --length short
```

### API Commands

```bash
# Make a GET request
python -m cli.main api request https://jsonplaceholder.typicode.com/posts/1

# Make a POST request
python -m cli.main api request https://jsonplaceholder.typicode.com/posts \
  --method POST \
  --data '{"title":"Test Post","body":"This is a test","userId":1}'

# Save the request
python -m cli.main api request https://jsonplaceholder.typicode.com/posts/1 --save test-api

# List saved requests
python -m cli.main api list-saved

# Load a saved request
python -m cli.main api load test-api
```

## Command Structure

Each command follows a consistent structure:

```
aidev [command_group] [command] [arguments] [options]
```

For example:
```
aidev code generate "description of code" --language python --output file.py
```

Where:
- `code` is the command group
- `generate` is the command
- `"description of code"` is a positional argument
- `--language` and `--output` are options

## Development

When adding new commands:

1. Create a module in the `commands` directory
2. Define a Typer app in that module
3. Add commands with `@app.command()` decorator
4. Import and add to `main.py` using `app.add_typer()` 