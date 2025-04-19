#!/usr/bin/env python
"""Script to build and publish the package to PyPI.

Usage:
    python scripts/publish.py [--test]

Options:
    --test: Publish to TestPyPI instead of PyPI
"""

import os
import subprocess
import sys
import shutil

def clean_build_dirs():
    """Clean build directories."""
    print("Cleaning build directories...")
    for dir_name in ["build", "dist", "aidev.egg-info"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def build_package():
    """Build the package."""
    print("Building package...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "build", "twine"], check=True)
    subprocess.run([sys.executable, "-m", "build"], check=True)

def verify_package():
    """Verify the package with twine."""
    print("Verifying package...")
    subprocess.run([sys.executable, "-m", "twine", "check", "dist/*"], check=True)

def publish_package(test=False):
    """Publish the package to PyPI or TestPyPI."""
    repository = "--repository testpypi" if test else ""
    print(f"Publishing package to {'TestPyPI' if test else 'PyPI'}...")
    cmd = f"{sys.executable} -m twine upload {repository} dist/*"
    
    print(f"Running: {cmd}")
    if input("Proceed? (y/n): ").lower() != "y":
        print("Aborting.")
        return
    
    os.system(cmd)  # Using os.system to ensure password prompt works correctly

def main():
    """Main function."""
    test_mode = "--test" in sys.argv
    
    clean_build_dirs()
    build_package()
    verify_package()
    publish_package(test=test_mode)
    
    print("Done!")

if __name__ == "__main__":
    main() 