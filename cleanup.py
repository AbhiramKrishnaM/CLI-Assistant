#!/usr/bin/env python
"""
Cleanup script to update all command files to use the new model framework.
This script will modify the import statements and OLLAMA_AVAILABLE checks
in all command files to match the new framework.
"""
import os
import re
import glob

# Find all command files
command_files = glob.glob("cli/commands/*.py")

for file_path in command_files:
    print(f"Processing {file_path}...")
    
    # Read the file content
    with open(file_path, "r") as f:
        content = f.read()
    
    # Update the import statements
    content = content.replace(
        "from cli.utils.api import api_request, OLLAMA_AVAILABLE, get_available_local_models",
        "from cli.utils.api import api_request, get_available_local_models"
    )
    
    # Update the option flags for using local models
    content = re.sub(
        r'use_local: bool = typer\.Option\(False, "--local", "-l", help="Use local Ollama model instead of API backend"\)',
        r'use_local: bool = typer.Option(True, "--local/--api", help="Use local AI model instead of API backend")',
        content
    )
    
    # Update the model option flags
    content = re.sub(
        r'model: str = typer\.Option\("deepseek-r1:7b", "--model", "-m", help="Specify which local model to use \(requires --local\)"\)',
        r'model: str = typer.Option("deepseek-r1:7b", "--model", "-m", help="Specify which local model to use")',
        content
    )
    
    # Remove the OLLAMA_AVAILABLE checks
    content = re.sub(
        r'\s+if use_local and not OLLAMA_AVAILABLE:.*?\s+use_local = False',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Update the warning messages
    content = content.replace(
        "No local models found in Ollama. Falling back to API backend.",
        "No local models available. Falling back to API backend."
    )
    
    content = content.replace(
        "Model '{model}' not found in Ollama.",
        "Model '{model}' not found."
    )
    
    # Remove the "if use_local else None" in local_model_name
    content = re.sub(
        r'local_model_name=model if use_local else None',
        r'local_model_name=model',
        content
    )
    
    # Write the updated content back to the file
    with open(file_path, "w") as f:
        f.write(content)
    
    print(f"Updated {file_path}")

print("\nAll command files updated successfully!")
print("You should manually check each file to ensure the updates are correct.")
print("Then, run the tests to verify everything still works as expected.") 