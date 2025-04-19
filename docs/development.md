# Development Guide

This guide provides information for developers who want to contribute to the AIDEV project.

## Setting Up the Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/AbhiramKrishnaM/aidev.git
   cd aidev
   ```

2. Use the clean installation script to set up a development environment:
   ```bash
   ./scripts/clean_install.sh
   ```

   This will create a virtual environment, install all dependencies, and set up pre-commit hooks.

3. Alternatively, set up manually:
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Install in development mode
   pip install -e .

   # Set up pre-commit hooks
   ./scripts/setup_hooks.sh
   ```

## Project Structure

```
aidev/
├── cli/                   # CLI interface code
│   ├── commands/          # Command implementations
│   │   ├── api.py         # API testing commands
│   │   ├── code.py        # Code generation commands
│   │   ├── docs.py        # Documentation commands
│   │   ├── git.py         # Git assistance commands
│   │   └── terminal.py    # Terminal command help
│   ├── utils/             # Utilities
│   │   ├── api.py         # API client utilities
│   │   ├── config.py      # Configuration management
│   │   └── formatting.py  # Output formatting
│   ├── ai_agent_models/   # AI model implementations
│   │   ├── base_model.py            # Base abstract class for models
│   │   ├── ollama_deepseek_r1_7b.py # Ollama model implementation
│   │   ├── model_factory.py         # Model instantiation factory
│   │   └── __init__.py              # Model registration
│   └── main.py            # Entry point
├── tests/                 # Test suite
├── docs/                  # Documentation
└── scripts/               # Helper scripts
```

## Pre-commit Hooks

We use pre-commit hooks to ensure code quality and consistency. These hooks run automatically when you commit changes.

### Available Hooks

Our pre-commit configuration includes:

1. **Code Formatting**
   - **black**: Formats Python code according to the Black code style
   - **isort**: Sorts imports according to the PEP8 style guide

2. **Code Quality**
   - **flake8**: Checks for PEP8 compliance and common errors
   - **mypy**: Performs static type checking

3. **General Checks**
   - Trailing whitespace removal
   - End of file fixing
   - YAML/TOML syntax checking
   - Debug statement checks

### Running Pre-commit Manually

You can run the pre-commit checks manually:

```bash
# Run on all files
pre-commit run --all-files

# Run on specific files
pre-commit run --files path/to/file1.py path/to/file2.py

# Run specific hook
pre-commit run black --all-files
```

## Coding Standards

We follow these coding standards:

1. **Code Formatting**
   - Follow Black code style (88 character line length)
   - Use isort for import sorting
   - Use f-strings for string formatting

2. **Documentation**
   - All modules, classes, and functions should have docstrings
   - Use Google-style docstrings
   - Keep documentation up-to-date with code changes

3. **Type Annotations**
   - Use type annotations for all function parameters and return values
   - Use `Optional[]` for optional parameters
   - Use `Union[]` for multiple possible types
   - Run mypy to check type consistency

4. **Error Handling**
   - Use proper exception handling
   - Provide clear error messages to users
   - Use the formatting utilities for consistent output

## Adding New Model Implementations

To add a new LLM model:

1. Create a new model class in `cli/ai_agent_models/`:
   ```python
   from .base_model import BaseAIModel

   class NewModel(BaseAIModel):
       @property
       def model_name(self) -> str:
           return "new-model-name"

       @classmethod
       def is_available(cls) -> bool:
           # Check if the model is available
           ...

       def generate_text(self, prompt: str, **kwargs) -> dict:
           # Implement text generation
           ...

       # Implement other required methods
   ```

2. Register the model in `cli/ai_agent_models/__init__.py`:
   ```python
   from .new_model import NewModel

   MODEL_CLASSES = {
       "existing-model": ExistingModel,
       "new-model-name": NewModel,
   }
   ```

3. Test your implementation:
   ```bash
   # Run type checking
   mypy cli/ai_agent_models/new_model.py

   # Run unit tests
   pytest -xvs tests/test_models.py
   ```

## Development Workflow

1. Create a feature branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes and run tests:
   ```bash
   # Format code
   black .
   isort .

   # Run type checking
   mypy cli

   # Run tests
   pytest
   ```

3. Commit your changes (pre-commit hooks will run automatically)

4. Push your branch and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Common Development Tasks

```bash
# Run the CLI in development mode
python -m cli.main hello

# Format all code
black . && isort .

# Check types
mypy cli

# Run tests
pytest -v

# Check a specific command
python -m cli.main terminal suggest "find large files"
```

## Troubleshooting

- **Import errors:** Make sure you've installed the package in development mode (`pip install -e .`)
- **Pre-commit hook failures:** Run `pre-commit run --all-files` to see detailed error messages
- **Type checking errors:** Ensure all functions have proper return type annotations
- **Dependency issues:** Try using the clean install script (`./scripts/clean_install.sh`)
