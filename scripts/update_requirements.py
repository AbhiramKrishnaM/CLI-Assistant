#!/usr/bin/env python
"""
Script to generate requirements.txt with pinned versions from the current environment.
This helps ensure consistent installations across different environments.

Usage:
    python scripts/update_requirements.py
"""

import subprocess
import sys
from pathlib import Path


def generate_requirements() -> None:
    """Generate requirements.txt with pinned versions."""
    print("Generating requirements.txt with pinned versions...")

    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Path to the requirements.txt file
    requirements_path = project_root / "requirements.txt"

    # Run pip freeze to get installed packages
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True,
        text=True,
        check=True,
    )

    # Get packages from pip freeze
    packages = result.stdout.strip().split("\n")

    # Filter out packages with '@' as they're typically editable installs
    # and packages that start with '-e' which are also editable installs
    packages = [pkg for pkg in packages if not pkg.startswith("-e") and "@" not in pkg]

    # If we have an existing requirements.txt, preserve comments and formatting
    try:
        with open(requirements_path, "r") as f:
            existing_lines = f.readlines()

        # Extract comments and blank lines
        comments_and_blanks = []
        for line in existing_lines:
            line = line.strip()
            if not line or line.startswith("#"):
                comments_and_blanks.append(line)
    except FileNotFoundError:
        comments_and_blanks = []

    # Write the updated requirements.txt
    with open(requirements_path, "w") as f:
        # Write header comment
        f.write("# Generated requirements for aidev\n")
        f.write("# This file contains exact versions for reproducible builds\n\n")

        # Write preserved comments
        for comment in comments_and_blanks:
            if comment:
                f.write(f"{comment}\n")

        # Write packages
        for package in sorted(packages):
            f.write(f"{package}\n")

    print(f"Requirements file updated: {requirements_path}")
    print(f"Total packages: {len(packages)}")


def update_requirements() -> None:
    """Update the requirements.txt file based on the current environment."""
    # Add implementation here


if __name__ == "__main__":
    generate_requirements()
