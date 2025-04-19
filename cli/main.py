"""AI-powered CLI assistant for developers."""
import importlib.metadata

import typer
from rich import print

from cli.commands import api, code, docs, git, terminal

__version__ = importlib.metadata.version("aidev")

app = typer.Typer(help="AI-powered CLI assistant for developers")

# Add subcommands
app.add_typer(code.app, name="code", help="Generate and manage code snippets")
app.add_typer(terminal.app, name="terminal", help="Get help with terminal commands")
app.add_typer(git.app, name="git", help="Git operations assistance")
app.add_typer(docs.app, name="docs", help="Search and summarize documentation")
app.add_typer(api.app, name="api", help="Test and format API requests")


@app.command()
def hello() -> None:
    """Simple command to test the CLI assistant for developers."""
    print("[bold green]Hello! AI CLI Assistant is ready to help you.[/bold green]")
    print("\nAvailable commands:")
    print("  [blue]code[/blue]      - Generate and manage code snippets")
    print("  [blue]terminal[/blue]  - Get help with terminal commands")
    print("  [blue]git[/blue]       - Git operations assistance")
    print("  [blue]docs[/blue]      - Search and summarize documentation")
    print("  [blue]api[/blue]       - Test and format API requests")
    print("\nRun [yellow]aidev --help[/yellow] for more information.")


@app.callback()
def callback(
    version: bool = typer.Option(
        False, "--version", "-v", help="Show the application version"
    )
) -> None:
    """Handle top-level CLI options."""
    if version:
        print(f"AI CLI Assistant version: {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
