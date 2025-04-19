# PyPI Distribution

This guide explains how to distribute and install the aidev CLI Assistant via PyPI.

## Installation from PyPI

Once the package is published to PyPI, users can install it with pip:

```bash
# Install from PyPI
pip install aidev

# Install a specific version
pip install aidev==0.1.0
```

## Development Installation

For development work, install the package in editable mode:

```bash
# Clone the repository
git clone https://github.com/yourusername/aidev.git
cd aidev

# Install in development mode
pip install -e .
```

## Publishing to PyPI

### Prerequisites

- A PyPI account
- Proper packaging tools installed:
  ```bash
  pip install build twine
  ```

### Manual Publishing Steps

1. Update version in `pyproject.toml`
2. Clean previous builds:
   ```bash
   rm -rf build/ dist/ *.egg-info/
   ```
3. Build the package:
   ```bash
   python -m build
   ```
4. Check the distribution:
   ```bash
   twine check dist/*
   ```
5. Upload to TestPyPI (optional):
   ```bash
   twine upload --repository testpypi dist/*
   ```
6. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

### Using the Publishing Script

We provide a script to automate the publishing process:

```bash
# Publish to PyPI
python scripts/publish.py

# Publish to TestPyPI instead
python scripts/publish.py --test
```

### First-time Setup

If this is your first time publishing to PyPI, you can configure your PyPI credentials in a `.pypirc` file in your home directory:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = your-pypi-api-token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = your-testpypi-api-token
```

Replace `your-pypi-api-token` and `your-testpypi-api-token` with your actual API tokens.

## Installing from TestPyPI

To test the package from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ aidev
```

The `--extra-index-url` ensures dependencies come from the main PyPI repository. 