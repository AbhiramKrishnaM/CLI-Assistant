"""AI-powered CLI assistant for developers."""
import importlib.metadata
import os
from pathlib import Path
from typing import Optional

import typer
from rich import print
from typing_extensions import Annotated

from cli.commands import api, code, docs, git, terminal

# Try to get version from metadata, otherwise use a default
try:
    __version__ = importlib.metadata.version("aidev")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.1.0-dev"  # Fallback version for development

app = typer.Typer(help="AI-powered CLI assistant for developers", add_completion=True)

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


@app.command()
def install_completion(
    shell: Annotated[
        Optional[str],
        typer.Option(
            "--shell",
            "-s",
            help="Shell to install completion for (bash, zsh, fish)",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Force overwrite existing completion",
        ),
    ] = False,
) -> None:
    """Install shell completion for aidev.
    Supports bash, zsh, and fish shells.
    Example:
        $ aidev install-completion --shell bash
        $ aidev install-completion --shell zsh
        $ aidev install-completion --shell fish
    """
    if shell is None:
        # Try to detect the shell
        shell = os.environ.get("SHELL", "")
        if shell:
            shell = os.path.basename(shell)
            if shell == "bash":
                shell = "bash"
            elif shell == "zsh":
                shell = "zsh"
            elif shell == "fish":
                shell = "fish"
            else:
                shell = None

    if shell is None:
        print("[yellow]Could not detect shell. Please specify with --shell.[/yellow]")
        raise typer.Exit(1)

    if shell not in ["bash", "zsh", "fish"]:
        print(f"[red]Unsupported shell: {shell}[/red]")
        print("[yellow]Supported shells: bash, zsh, fish[/yellow]")
        raise typer.Exit(1)

    completion_file = None
    completion_path = None
    completion_content = None

    if shell == "bash":
        # For bash, we need to add the completion to ~/.bash_completion
        home = Path.home()
        completion_path = home / ".bash_completion"
        if not force and completion_path.exists():
            with open(completion_path, "r") as f:
                if "aidev" in f.read():
                    print(
                        "[yellow]Completion already installed for bash. Use --force to overwrite.[/yellow]"
                    )
                    raise typer.Exit(0)

        # Get the completion for bash
        completion_content = (
            "_AIDEV_COMPLETE=bash_source aidev > ~/.aidev-complete.bash\n"
        )
        completion_content += "source ~/.aidev-complete.bash\n"

    elif shell == "zsh":
        # For zsh, we need to add the completion to ~/.zshrc
        home = Path.home()
        completion_path = home / ".zshrc"

        if not force and completion_path.exists():
            with open(completion_path, "r") as f:
                if "aidev" in f.read():
                    print(
                        "[yellow]Completion already installed for zsh. Use --force to overwrite.[/yellow]"
                    )
                    raise typer.Exit(0)

        # Get the completion for zsh
        completion_content = "# AIDEV completion\n"
        completion_content += "autoload -U compinit\n"
        completion_content += "compinit\n"
        completion_content += (
            "_AIDEV_COMPLETE=zsh_source aidev > ~/.aidev-complete.zsh\n"
        )
        completion_content += "source ~/.aidev-complete.zsh\n"

    elif shell == "fish":
        # For fish, we add to ~/.config/fish/completions/aidev.fish
        home = Path.home()
        completion_dir = home / ".config" / "fish" / "completions"
        completion_dir.mkdir(parents=True, exist_ok=True)
        completion_path = completion_dir / "aidev.fish"

        # Get the completion for fish
        completion_content = "_AIDEV_COMPLETE=fish_source aidev > ~/.config/fish/completions/aidev.fish\n"

    if completion_path and completion_content:
        # If we're not appending to an existing file, we'll create the file
        # Otherwise, we'll append to the existing file
        if shell in ["bash", "zsh"]:
            # Append to the file
            with open(completion_path, "a") as f:
                f.write("\n" + completion_content)
        else:
            # Create or overwrite the file
            with open(completion_path, "w") as f:
                f.write(completion_content)

        print(f"[green]Successfully installed completion for {shell}![/green]")
        print(
            f"[yellow]Restart your shell or run 'source {completion_path}' to enable completion.[/yellow]"
        )
    else:
        print("[red]Failed to install completion.[/red]")
        raise typer.Exit(1)


@app.callback()
def callback(
    version: Annotated[
        bool,
        typer.Option("--version", "-v", help="Show the application version"),
    ] = False,
) -> None:
    """Handle top-level CLI options."""
    if version:
        print(f"AI CLI Assistant version: {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
