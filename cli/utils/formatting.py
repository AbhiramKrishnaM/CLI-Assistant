"""Formatting utilities for the CLI output."""
from contextlib import contextmanager
from typing import Any, Dict, Generator, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

console = Console()


def print_code(code: str, language: str = "python") -> None:
    """Print formatted code with syntax highlighting."""
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    console.print(syntax)


def print_result(title: str, content: str, style: str = "green") -> None:
    """Print a result panel with a title."""
    panel = Panel(content, title=title, border_style=style, expand=False)
    console.print(panel)


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error: [/bold red] {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[bold yellow]Warning: [/bold yellow] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]Success: [/bold green] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[bold blue]Info: [/bold blue] {message}")


def print_table(
    headers: List[str], rows: List[List[Any]], title: Optional[str] = None
) -> None:
    """Print data as a formatted table."""
    table = Table(title=title)

    for header in headers:
        table.add_column(header, style="cyan", no_wrap=True)

    for row in rows:
        table.add_row(*[str(cell) for cell in row])

    console.print(table)


def print_json(data: Dict[str, Any], title: Optional[str] = None) -> None:
    """Print formatted JSON data."""
    import json

    json_str = json.dumps(data, indent=2)

    if title:
        console.print(f"[bold]{title}[/bold]")

    syntax = Syntax(json_str, "json", theme="monokai")
    console.print(syntax)


@contextmanager
def loading_spinner(
    text: str = "Loading...", spinner_style: str = "dots"
) -> Generator[None, None, None]:
    """
    Display a loading spinner while executing a block of code.

    Args:
        text: The text to display next to the spinner
        spinner_style: The style of spinner to use
    """
    with console.status(text, spinner=spinner_style) as status:
        try:
            yield
        finally:
            pass


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: The text to truncate
        max_length: Maximum length in characters

    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
