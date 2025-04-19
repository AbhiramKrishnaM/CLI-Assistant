#!/usr/bin/env python
"""Fix mypy module mapping issues.

This script adds a mypy.ini file to the project to properly configure
module mapping and resolve the "Source file found twice under different module names" error.
"""

import os
from pathlib import Path


def create_mypy_ini() -> None:
    """Create a mypy.ini file with proper configuration."""
    content = """# Global options
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
strict_optional = True

# Set explicit_package_bases to handle duplicate module issues
explicit_package_bases = True

# Keep namespace packages (without __init__.py) working
namespace_packages = True

# Ignore import errors for certain modules
[mypy.plugins.numpy.*]
ignore_missing_imports = True

[mypy-pytest.*]
ignore_missing_imports = True

[mypy-requests.*]
ignore_missing_imports = True
"""

    # Write the mypy.ini file
    with open("mypy.ini", "w", encoding="utf-8") as f:
        f.write(content)

    print("Created mypy.ini file with explicit_package_bases=True")
    print(
        "This should resolve the 'Source file found twice under different module names' error"
    )


def main() -> None:
    """Main function."""
    # Check if we're in the project root directory
    if os.path.exists("cli") and os.path.exists("scripts"):
        create_mypy_ini()
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)

        # Change to the project root directory
        os.chdir(project_root)
        create_mypy_ini()

    # Check if cli directory has __init__.py
    cli_dir = Path("cli")
    if cli_dir.exists() and cli_dir.is_dir():
        init_file = cli_dir / "__init__.py"
        if not init_file.exists():
            # Create empty __init__.py file
            init_file.touch()
            print(f"Created {init_file} file")

        # Check if cli/utils directory has __init__.py
        utils_dir = cli_dir / "utils"
        if utils_dir.exists() and utils_dir.is_dir():
            utils_init_file = utils_dir / "__init__.py"
            if not utils_init_file.exists():
                # Create empty __init__.py file
                utils_init_file.touch()
                print(f"Created {utils_init_file} file")


if __name__ == "__main__":
    main()
