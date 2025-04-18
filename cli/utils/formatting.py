"""Formatting utilities for the CLI output."""
from typing import Any, Dict, List, Optional, Callable
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text
import time
from contextlib import contextmanager

console = Console()

def print_code(code: str, language: str = "python"):
    """Print formatted code with syntax highlighting."""
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    console.print(syntax)

def print_result(title: str, content: str, style: str = "green"):
    """Print a result panel with a title."""
    panel = Panel(content, title=title, border_style=style, expand=False)
    console.print(panel)

def print_error(message: str):
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")

def print_warning(message: str):
    """Print a warning message."""
    console.print(f"[bold yellow]Warning:[/bold yellow] {message}")

def print_success(message: str):
    """Print a success message."""
    console.print(f"[bold green]Success:[/bold green] {message}")

def print_info(message: str):
    """Print an info message."""
    console.print(f"[bold blue]Info:[/bold blue] {message}")

def print_table(headers: List[str], rows: List[List[Any]], title: Optional[str] = None):
    """Print data as a formatted table."""
    table = Table(title=title)
    
    for header in headers:
        table.add_column(header, style="cyan", no_wrap=True)
    
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
    
    console.print(table)

def print_json(data: Dict[str, Any], title: Optional[str] = None):
    """Print formatted JSON data."""
    import json
    json_str = json.dumps(data, indent=2)
    
    if title:
        console.print(f"[bold]{title}[/bold]")
    
    syntax = Syntax(json_str, "json", theme="monokai")
    console.print(syntax)

@contextmanager
def loading_spinner(message: str = "Processing", spinner_style: str = "dots", color: str = "blue"):
    """
    Context manager that displays a loading spinner while executing code.
    
    Args:
        message: The message to display alongside the spinner
        spinner_style: The spinner style to use (dots, dots2, dots3, dots12, line, aesthetic, etc.)
        color: The color of the spinner and message text
        
    Example:
        with loading_spinner("Generating code...", spinner_style="aesthetic"):
            result = some_long_running_function()
    """
    # Dictionary of spinner styles
    spinner_styles = {
        "dots": "dots",
        "dots2": "dots2",
        "dots3": "dots3",
        "dots12": "dots12",
        "line": "line",
        "aesthetic": "aesthetic",
        "bounce": "point",
        "moon": "moon",
        "clock": "clock",
        "simple": "arrow",
        "thinking": "dots10"
    }
    
    # Get the spinner name (Rich uses predefined spinner names)
    spinner_name = spinner_styles.get(spinner_style, "dots")
    formatted_message = f"[bold {color}]{message}[/bold {color}]"
    
    with console.status(formatted_message, spinner=spinner_name) as status:
        try:
            yield
        finally:
            pass 