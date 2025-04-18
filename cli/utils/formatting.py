"""Formatting utilities for the CLI output."""
from typing import Any, Dict, List, Optional
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table
from rich.panel import Panel

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