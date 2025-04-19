# Development Guide

This guide provides information for developers who want to contribute to the aidev project.

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

## Pre-commit Hooks

We use pre-commit hooks to ensure code quality and consistency. These hooks run automatically when you commit changes, checking your code before it's committed.

### Installing Pre-commit Hooks

If you didn't use the clean installation script, you can set up the pre-commit hooks manually:

```bash
./scripts/setup_hooks.sh
```

### Available Hooks

Our pre-commit configuration includes:

1. **Code Formatting**
   - **black**: Formats Python code according to the Black code style
   - **isort**: Sorts imports according to the PEP8 style guide, compatible with Black

2. **Code Quality**
   - **flake8**: Checks for PEP8 compliance and common errors
   - **mypy**: Performs static type checking

3. **General Checks**
   - Trailing whitespace removal
   - End of file fixing
   - YAML/TOML syntax checking
   - Large file checks
   - Debug statement checks
   - Merge conflict detection

### Running Pre-commit Manually

You can run the pre-commit checks manually without committing:

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
   - Line length: 88 characters
   - Follow Black code style
   - Properly sorted imports using isort
   - Use f-strings for string formatting

2. **Documentation**
   - All modules, classes, and functions should have docstrings
   - Use Google-style docstrings
   - Keep docstrings clear and concise

3. **Type Annotations**
   - Use type annotations for all function parameters and return values
   - Use Optional[] for optional parameters
   - Use Union[] for multiple possible types

4. **Error Handling**
   - Use proper exception handling
   - Create custom exceptions when appropriate
   - Provide clear error messages

5. **Testing**
   - Write tests for all new features
   - Maintain high test coverage
   - Use pytest fixtures for common setup/teardown

## Submitting Changes

1. Create a new branch for your changes
2. Make your changes and commit them (pre-commit hooks will run automatically)
3. Push your branch to your fork
4. Submit a pull request to the main repository

## Development Commands

```bash
# Format code
black .
isort .

# Check types
mypy cli

# Run linting
flake8

# Run tests
pytest -v
```

## Additional Resources

- [Black Documentation](https://black.readthedocs.io/en/stable/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [Flake8 Documentation](https://flake8.pycqa.org/en/latest/)
- [MyPy Documentation](https://mypy.readthedocs.io/en/stable/)
- [Pre-commit Documentation](https://pre-commit.com/)
