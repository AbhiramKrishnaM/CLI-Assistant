#!/usr/bin/env python3
"""Script to run tests with different options."""
import subprocess
import argparse
import sys
import os

def run_tests(include_slow=False, tests_path="tests", verbose=False):
    """Run the tests with the specified options."""
    # Change to the root directory
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    
    # Build the command
    cmd = ["pytest", tests_path]
    
    # Add verbosity if requested
    if verbose:
        cmd.append("-v")
    
    # Skip slow tests if requested
    if not include_slow:
        cmd.append("-k")
        cmd.append("not slow")
    
    # Add color output
    cmd.append("--color=yes")
    
    # Print the command
    print(f"Running: {' '.join(cmd)}")
    print("=" * 80)
    
    # Run the tests
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests for the AI CLI Assistant")
    parser.add_argument(
        "--slow", 
        action="store_true", 
        help="Include slow tests that use real models"
    )
    parser.add_argument(
        "--path", 
        default="tests", 
        help="Path to test files or directories"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Run the tests
    returncode = run_tests(
        include_slow=args.slow,
        tests_path=args.path,
        verbose=args.verbose
    )
    
    # Exit with the test result code
    sys.exit(returncode) 