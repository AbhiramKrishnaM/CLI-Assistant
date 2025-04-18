"""Terminal command suggestions and explanations."""
import typer
from typing import List, Optional
from rich import print
from cli.utils.api import api_request

app = typer.Typer(help="Get help with terminal commands")

@app.command()
def suggest(
    description: str = typer.Argument(..., help="What you want to accomplish"),
    platform: str = typer.Option("auto", help="Platform (linux, mac, windows, or auto)"),
):
    """Suggest terminal commands based on a description."""
    if platform == "auto":
        import platform as plt
        system = plt.system().lower()
        if "darwin" in system:
            platform = "mac"
        elif "linux" in system:
            platform = "linux"
        elif "windows" in system:
            platform = "windows"
        else:
            platform = "linux"  # Default to Linux
    
    print(f"Suggesting commands for '{description}' on {platform}:")
    
    # Request command suggestions from the API
    response = api_request(
        endpoint="/text/generate",
        method="POST",
        data={
            "prompt": f"Suggest terminal commands for: {description}\nPlatform: {platform}",
            "temperature": 0.3,
            "max_length": 512
        },
        loading_message=f"Finding terminal commands for {platform}..."
    )
    
    if "error" in response:
        print("[bold red]Failed to get command suggestions.[/bold red]")
        # Fallback to mock suggestions
        if "list" in description.lower() and "files" in description.lower():
            print("\nCommand: ls -la" if platform != "windows" else "\nCommand: dir /a")
            print("This command lists all files including hidden ones in detailed format.")
        elif "search" in description.lower():
            print("\nCommand: grep -r 'search_term' ." if platform != "windows" else 
                 "\nCommand: findstr /s /i 'search_term' *.*")
            print("This command recursively searches for a term in the current directory.")
        else:
            print("\nI need more specific information to suggest a command. Try describing what you want to do with files, directories, or system resources.")
    else:
        # Display the AI-generated suggestions
        suggestions = response.get("text", "No suggestions generated")
        print("\n[bold green]Suggested Commands:[/bold green]")
        print(suggestions)

@app.command()
def explain(
    command: List[str] = typer.Argument(..., help="Command to explain")
):
    """Explain what a terminal command does."""
    full_command = " ".join(command)
    print(f"Explaining command: [bold]{full_command}[/bold]")
    
    # Request command explanation from the API
    response = api_request(
        endpoint="/text/generate",
        method="POST",
        data={
            "prompt": f"Explain the following terminal command in detail: {full_command}",
            "temperature": 0.3,
            "max_length": 512
        },
        loading_message=f"Analyzing command..."
    )
    
    if "error" in response:
        print("[bold red]Failed to get command explanation.[/bold red]")
        # Fallback to mock explanations
        if full_command.startswith("ls"):
            print("\nThe 'ls' command lists files and directories.")
            if "-la" in full_command:
                print("The '-l' flag shows detailed information in long format.")
                print("The '-a' flag shows hidden files (those starting with '.').")
        elif full_command.startswith("grep"):
            print("\nThe 'grep' command searches for patterns in files.")
            if "-r" in full_command:
                print("The '-r' flag makes the search recursive through directories.")
        elif full_command.startswith("git"):
            print("\nThis is a git command for version control.")
            if "commit" in full_command:
                print("The 'commit' subcommand records changes to the repository.")
        else:
            print("\nThis command would be explained by the AI model. Currently using mock explanations for demonstration.")
    else:
        # Display the AI-generated explanation
        explanation = response.get("text", "No explanation generated")
        print("\n[bold green]Explanation:[/bold green]")
        print(explanation) 