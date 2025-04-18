# Testing the AI CLI Assistant

This directory contains tests for the AI CLI Assistant. The tests are written using pytest and cover both the CLI interface and the backend API.

## Test Structure

The test suite is organized as follows:

- `test_models.py`: Tests for the model integration and model manager
- `test_api.py`: Tests for the FastAPI backend endpoints
- `test_cli.py`: Tests for the Typer CLI interface
- `test_cli_utils.py`: Tests for CLI utility functions
- `conftest.py`: Pytest fixtures for testing
- `run_tests.py`: Script to run the tests with various options

## Running Tests

### Using the run_tests.py Script

#### Quick Tests (No Real Models)

To run all tests except those that require real AI models:

```bash
python tests/run_tests.py
```

#### Full Tests (Including Real Models)

To run all tests, including those that use actual AI models (marked with `@pytest.mark.slow`):

```bash
python tests/run_tests.py --slow
```

#### Specific Test Files

To run tests from a specific file:

```bash
python tests/run_tests.py --path tests/test_cli.py
```

#### Verbose Output

For more detailed test output:

```bash
python tests/run_tests.py -v
```

### Using Pytest Directly

If you prefer to use pytest directly:

```bash
# Run all tests except slow ones
pytest -k "not slow"

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_api.py

# Run a specific test function
pytest tests/test_api.py::test_health_endpoint

# Run with coverage report
pytest --cov=backend --cov=cli --cov-report=term
```

## Test Categories

1. **Fast Tests**: Default tests that use mocks and don't require actual model loading.
2. **Slow Tests**: Tests marked with `@pytest.mark.slow` that load actual AI models.

## Fixtures

The following fixtures are available for tests:

- `mock_model_manager`: Mocks the model manager for faster tests
- `temp_code_file`: Creates a temporary Python file for testing code-related functionality

## Adding New Tests

When adding new tests:

1. Follow the existing naming conventions (`test_*.py` for files, `test_*` for functions)
2. Use fixtures from `conftest.py` when possible
3. Mark tests that use real models with `@pytest.mark.slow`
4. Write docstrings for all test functions

## Testing Guidelines

- **Unit Tests**: Test individual functions in isolation.
- **Integration Tests**: Test the interaction between components.
- **Mock External Services**: Use mocks for external services and APIs.
- **Test Coverage**: Aim for high test coverage, especially for critical components.
- **Test Edge Cases**: Include tests for edge cases and error handling. 