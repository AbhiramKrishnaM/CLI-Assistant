#!/usr/bin/env python
"""
Script to check if aidev is installed and get its version.

Run this script after installation to verify that everything is working correctly.
"""

import importlib.metadata
import subprocess
import sys


def check_installation() -> bool:
    """Check if aidev is installed and get its version."""
    try:
        # Check if package is installed
        version = importlib.metadata.version("aidev")
        print(f"✅ aidev is installed (version {version})")

        # Check if entry point is working
        result = subprocess.run(["aidev", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 'aidev' command is working: {result.stdout.strip()}")
        else:
            print("❌ 'aidev' command failed to run")
            print(f"Error: {result.stderr}")

        # Check for Ollama
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is installed and accessible")
            models = result.stdout.strip().split("\n")
            if len(models) > 1:  # Header row + at least one model
                print(f"📋 Available models: {len(models)-1}")
            else:
                print(
                    "⚠️ No Ollama models found. You should install at least one model."
                )
                print("   Try: ollama pull deepseek-r1: 7b")
        else:
            print("❌ Ollama is not installed or not accessible")
            print("Please install Ollama from https: //ollama.ai")

        return True

    except importlib.metadata.PackageNotFoundError:
        print("❌ aidev is not installed")
        print("Install it with: pip install aidev")
        return False
    except Exception as e:
        print(f"❌ Error checking installation: {e}")
        return False


def main() -> None:
    """Main function to check installation status."""
    # Add implementation here


if __name__ == "__main__":
    success = check_installation()
    sys.exit(0 if success else 1)
