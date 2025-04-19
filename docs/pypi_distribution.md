# PyPI Distribution Guide

This guide explains how to package, publish, and install AIDEV via PyPI (Python Package Index).

## Installation from PyPI

Users can install AIDEV with pip:

```bash
# Install the latest version
pip install aidev

# Install a specific version
pip install aidev==0.1.0
```

## Package Structure

The distribution includes:

```
aidev/
├── cli/                # Main package code
├── pyproject.toml      # Package metadata and dependencies
└── README.md           # Package documentation
```

## Development Installation

For development work:

```bash
# Clone the repository
git clone https://github.com/AbhiramKrishnaM/aidev.git
cd aidev

# Install in development mode
pip install -e .
```

This creates an "editable" installation where changes to the source code take effect immediately without reinstalling.

## Publishing to PyPI

### Prerequisites

1. Create a PyPI account at [pypi.org](https://pypi.org/account/register/)
2. Install required tools:
   ```bash
   pip install build twine
   ```

### Publishing Process

#### Automated Publishing (Recommended)

Use the provided script:

```bash
# Run the publishing script
python scripts/publish.py

# Publish to TestPyPI for testing
python scripts/publish.py --test
```

The script handles:
- Version validation
- Cleaning old builds
- Building the package
- Running checks
- Uploading to PyPI

#### Manual Publishing

1. Update the version in `pyproject.toml`:
   ```toml
   [project]
   name = "aidev"
   version = "0.1.0"  # Update this
   ```

2. Clean previous builds:
   ```bash
   rm -rf build/ dist/ *.egg-info/
   ```

3. Build the package:
   ```bash
   python -m build
   ```

4. Check the package:
   ```bash
   twine check dist/*
   ```

5. Upload to PyPI:
   ```bash
   # Upload to TestPyPI first (recommended)
   twine upload --repository testpypi dist/*

   # Upload to PyPI when ready
   twine upload dist/*
   ```

## PyPI Authentication

### Method 1: .pypirc File (Recommended)

Create a `.pypirc` file in your home directory:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = testpypi-your-api-token-here
```

Replace `pypi-your-api-token-here` and `testpypi-your-api-token-here` with your actual API tokens.

### Method 2: Environment Variables

Set environment variables for authentication:

```bash
# For TestPyPI
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=testpypi-your-api-token-here
export TWINE_REPOSITORY=testpypi

# For PyPI
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-api-token-here
```

## Testing Your Package

### Test the Published Package

After publishing to TestPyPI, test the installation:

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ aidev

# Test the CLI
aidev --version
aidev hello
```

### Local Distribution Testing

Test the package locally before publishing:

```bash
# Build the package
python -m build

# Install locally from the built wheel
pip install dist/aidev-0.1.0-py3-none-any.whl

# Test the installation
aidev --help
```

## Version Numbering

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes
- **MINOR**: Add functionality (backwards-compatible)
- **PATCH**: Bug fixes (backwards-compatible)

Example: `1.2.3`

## Troubleshooting

### Common Publishing Issues

- **Version already exists**: You cannot publish the same version twice. Update the version in `pyproject.toml`.
- **Invalid classifiers**: Ensure all classifiers in `pyproject.toml` are from [PyPI's classifier list](https://pypi.org/classifiers/).
- **README rendering**: Ensure your README.md is properly formatted for PyPI.
- **Missing dependencies**: Check that all dependencies are correctly listed in `pyproject.toml`.

### Installation Issues

- **Package not found**: The package might not be available yet. PyPI can take a few minutes to index new packages.
- **Dependency conflicts**: Try installing in a fresh virtual environment.
- **Import errors after installation**: Ensure the package structure in `pyproject.toml` matches the actual code structure.
