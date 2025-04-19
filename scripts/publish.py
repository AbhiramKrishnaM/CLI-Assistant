#!/usr/bin/env python
"""Script to build and publish the package to PyPI.

Usage:
    python scripts/publish.py [--test]

Options:
    --test: Publish to TestPyPI instead of PyPI
"""

import os
import shutil
import subprocess
import sys


def clean_build_dirs() -> None:
    """Clean build directories."""
    print("Cleaning build directories...")
    for dir_name in ["build", "dist", "ai_cli_assistant.egg-info"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)


def check_version_format(version: str) -> bool:
    """Check if the version string is valid (e.g., 1.0.0)."""
    import re

    return bool(re.match(r"^\d+\.\d+\.\d+$", version))


def update_version(new_version: str) -> None:
    """Update the version in all necessary files."""
    # Update version in pyproject.toml
    with open("pyproject.toml", "r") as f:
        content = f.read()

    import re

    updated_content = re.sub(
        r'version = "[^"]+"', f'version = "{new_version}"', content
    )

    with open("pyproject.toml", "w") as f:
        f.write(updated_content)

    print(f"Updated version to {new_version} in pyproject.toml")


def build_package() -> None:
    """Build the package using Poetry."""
    import subprocess

    print("Building package...")
    subprocess.run(["poetry", "build"], check=True)


def verify_package() -> None:
    """Verify the package with twine."""
    print("Verifying package...")
    subprocess.run([sys.executable, "-m", "twine", "check", "dist/*"], check=True)


def publish_package(test: bool = False) -> bool:
    """Publish the package to PyPI or TestPyPI."""
    repository = "--repository testpypi" if test else ""
    print(f"Publishing package to {'TestPyPI' if test else 'PyPI'}...")
    cmd = f"{sys.executable} -m twine upload {repository} dist/*"

    print(f"Running: {cmd}")
    if input("Proceed? (y/n): ").lower() != "y":
        print("Aborting.")
        return False

    os.system(cmd)  # Using os.system to ensure password prompt works correctly
    return True


def main() -> None:
    """Main function for building and publishing the package."""
    import argparse

    parser = argparse.ArgumentParser(description="Build and publish Python package")
    parser.add_argument(
        "--version", required=True, help="Version to publish (e.g., 1.0.0)"
    )
    args = parser.parse_args()

    if not check_version_format(args.version):
        print("Error: Version must be in format X.Y.Z (e.g., 1.0.0)")
        return

    update_version(args.version)
    build_package()
    verify_package()

    # Ask for confirmation before publishing
    response = input("Do you want to publish to PyPI? (y/n): ")
    if response.lower() == "y":
        if publish_package():
            print(f"Successfully published version {args.version}")
            print("Creating git tag...")
            import subprocess

            subprocess.run(["git", "tag", f"v{args.version}"])
            subprocess.run(["git", "push", "--tags"])
        else:
            print("Failed to publish package")


if __name__ == "__main__":
    main()
