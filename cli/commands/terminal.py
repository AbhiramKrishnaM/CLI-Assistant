"""Terminal command suggestions and explanations."""
import typer
from typing import List, Optional

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
    
    typer.echo(f"Suggesting commands for '{description}' on {platform}:")
    # Mock suggestions
    if "list" in description.lower() and "files" in description.lower():
        typer.echo("\nCommand: ls -la" if platform != "windows" else "\nCommand: dir /a")
        typer.echo("This command lists all files including hidden ones in detailed format.")
    elif "search" in description.lower():
        typer.echo("\nCommand: grep -r 'search_term' ." if platform != "windows" else 
                  "\nCommand: findstr /s /i 'search_term' *.*")
        typer.echo("This command recursively searches for a term in the current directory.")
    else:
        typer.echo("\nI need more specific information to suggest a command. Try describing what you want to do with files, directories, or system resources.")

@app.command()
def explain(
    command: List[str] = typer.Argument(..., help="Command to explain")
):
    """Explain what a terminal command does."""
    full_command = " ".join(command)
    typer.echo(f"Explaining command: {full_command}")
    
    # Mock explanations for common commands
    if full_command.startswith("ls"):
        typer.echo("\nThe 'ls' command lists files and directories.")
        if "-la" in full_command:
            typer.echo("The '-l' flag shows detailed information in long format.")
            typer.echo("The '-a' flag shows hidden files (those starting with '.').")
    elif full_command.startswith("grep"):
        typer.echo("\nThe 'grep' command searches for patterns in files.")
        if "-r" in full_command:
            typer.echo("The '-r' flag makes the search recursive through directories.")
    elif full_command.startswith("git"):
        typer.echo("\nThis is a git command for version control.")
        if "commit" in full_command:
            typer.echo("The 'commit' subcommand records changes to the repository.")
    else:
        typer.echo("\nThis command would be explained by the AI model. Currently using mock explanations for demonstration.") 