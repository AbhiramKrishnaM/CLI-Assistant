"""API request testing and formatting."""
import json
import os
import typer
import requests
from typing import Dict, Optional
from datetime import datetime
from rich import print
from rich.table import Table
from cli.utils.api import api_request, OLLAMA_AVAILABLE, get_available_local_models
from cli.utils.formatting import print_json, print_error, print_success, print_info
from cli.utils.config import get_config_value, set_config_value

app = typer.Typer(help="Test and format API requests")

# Directory to store saved requests
REQUESTS_DIR = os.path.expanduser("~/.aidev/requests")

@app.command()
def request(
    endpoint: str = typer.Argument(..., help="API endpoint to request"),
    method: str = typer.Option("GET", "--method", "-m", help="HTTP method to use"),
    data: Optional[str] = typer.Option(None, "--data", "-d", help="JSON data payload"),
    query: Optional[str] = typer.Option(None, "--query", "-q", help="URL query parameters as JSON"),
    use_local: bool = typer.Option(False, "--local", "-l", help="Use local Ollama model (only for text generation)"),
    model: str = typer.Option(None, "--model", help="Model to use for local generation"),
):
    """Make a direct request to the API."""
    print(f"Making {method} request to {endpoint}")
    
    # Parse data and query if provided
    data_dict = None
    if data:
        try:
            data_dict = json.loads(data)
        except json.JSONDecodeError:
            print_error("Invalid JSON in data payload")
            return
    
    query_dict = None
    if query:
        try:
            query_dict = json.loads(query)
        except json.JSONDecodeError:
            print_error("Invalid JSON in query parameters")
            return
    
    # Make the request
    response = api_request(
        endpoint=endpoint,
        method=method,
        data=data_dict,
        params=query_dict,
        use_local_model=use_local,
        local_model_name=model
    )
    
    # Display the response
    if "error" in response:
        print_error("Request failed")
        print(response.get("message", "Unknown error"))
    else:
        print_success("Request successful")
        print_json(response, "Response")

@app.command()
def config(
    show_all: bool = typer.Option(False, "--all", help="Show all config values"),
    set_ollama_url: Optional[str] = typer.Option(None, "--set-ollama-url", help="Set the Ollama API URL"),
    set_ollama_model: Optional[str] = typer.Option(None, "--set-ollama-model", help="Set the default Ollama model"),
    set_ollama_timeout: Optional[int] = typer.Option(None, "--set-ollama-timeout", help="Set the Ollama API timeout"),
    toggle_ollama: Optional[bool] = typer.Option(None, "--ollama-enabled", help="Enable or disable Ollama integration"),
):
    """Configure API settings including Ollama integration."""
    changes_made = False
    
    # Apply any changes
    if set_ollama_url is not None:
        set_config_value("ollama.url", set_ollama_url)
        print_success(f"Set Ollama API URL to: {set_ollama_url}")
        changes_made = True
        
    if set_ollama_model is not None:
        set_config_value("ollama.default_model", set_ollama_model)
        print_success(f"Set default Ollama model to: {set_ollama_model}")
        changes_made = True
    
    if set_ollama_timeout is not None:
        set_config_value("ollama.timeout", set_ollama_timeout)
        print_success(f"Set Ollama timeout to: {set_ollama_timeout} seconds")
        changes_made = True
    
    if toggle_ollama is not None:
        set_config_value("ollama.enabled", toggle_ollama)
        print_success(f"{'Enabled' if toggle_ollama else 'Disabled'} Ollama integration")
        changes_made = True
    
    # Show configuration
    table = Table(title="API Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    # API settings
    backend_url = get_config_value("backend.url")
    backend_timeout = get_config_value("backend.timeout")
    
    table.add_row("Backend URL", backend_url)
    table.add_row("Backend Timeout", str(backend_timeout) + " seconds")
    
    # Ollama settings
    ollama_enabled = get_config_value("ollama.enabled", True)
    ollama_url = get_config_value("ollama.url", "http://localhost:11434/api")
    ollama_model = get_config_value("ollama.default_model", "deepseek-r1:7b")
    ollama_timeout = get_config_value("ollama.timeout", 60)
    
    table.add_row("Ollama Enabled", "✅ Yes" if ollama_enabled else "❌ No")
    table.add_row("Ollama API URL", ollama_url)
    table.add_row("Default Ollama Model", ollama_model)
    table.add_row("Ollama Timeout", str(ollama_timeout) + " seconds")
    
    # Ollama status
    if OLLAMA_AVAILABLE:
        table.add_row("Ollama Status", "✅ Connected")
        models = get_available_local_models()
        if models:
            table.add_row("Available Models", ", ".join(models))
        else:
            table.add_row("Available Models", "None found")
    else:
        table.add_row("Ollama Status", "❌ Not connected")
    
    print(table)
    
    if not changes_made:
        print_info("To update settings, use the options like --set-ollama-url or --ollama-enabled")
        if not OLLAMA_AVAILABLE and ollama_enabled:
            print_info("Ollama is enabled in config but not available. Make sure Ollama is installed and running.")
            print_info("Install instructions: https://github.com/ollama/ollama")

@app.command()
def ollama_models():
    """List available models from Ollama."""
    if not OLLAMA_AVAILABLE:
        print_error("Ollama is not available. Make sure it's installed and running.")
        print_info("Install instructions: https://github.com/ollama/ollama")
        return
    
    models = get_available_local_models()
    
    if not models:
        print_info("No models found in Ollama.")
        print_info("You can pull models with: ollama pull <model-name>")
        print_info("Example: ollama pull deepseek-r1:7b")
        return
    
    table = Table(title="Available Ollama Models")
    table.add_column("Model Name", style="cyan")
    
    for model in models:
        table.add_row(model)
    
    print(table)
    
    default_model = get_config_value("ollama.default_model", "deepseek-r1:7b")
    if default_model in models:
        print_success(f"Default model is set to: {default_model}")
    else:
        print_info(f"Default model ({default_model}) is not available. You might want to update it.")
        if models:
            print_info(f"You can use: api config --set-ollama-model {models[0]}")

@app.command()
def list_saved():
    """List all saved API requests."""
    _ensure_requests_dir()
    
    saved_requests = []
    for filename in os.listdir(REQUESTS_DIR):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(REQUESTS_DIR, filename), "r") as f:
                    request_data = json.load(f)
                name = filename[:-5]  # Remove .json extension
                saved_requests.append((
                    name,
                    request_data.get("method", ""),
                    request_data.get("url", ""),
                    request_data.get("timestamp", "")
                ))
            except (json.JSONDecodeError, IOError):
                pass
    
    if not saved_requests:
        typer.echo("No saved requests found.")
        return
    
    typer.echo("Saved API Requests:")
    for name, method, url, timestamp in sorted(saved_requests):
        typer.echo(f"  - {name}: [{method}] {url} ({timestamp})")

@app.command()
def load(
    name: str = typer.Argument(..., help="Name of the saved request to load"),
    execute: bool = typer.Option(False, "--execute", "-e", help="Execute the request after loading"),
):
    """Load a saved API request."""
    _ensure_requests_dir()
    
    file_path = os.path.join(REQUESTS_DIR, f"{name}.json")
    if not os.path.exists(file_path):
        typer.echo(f"Error: Request '{name}' not found.", err=True)
        return
    
    try:
        with open(file_path, "r") as f:
            request_data = json.load(f)
        
        typer.echo(f"Loaded request: {name}")
        typer.echo(f"Method: {request_data.get('method', 'GET')}")
        typer.echo(f"URL: {request_data.get('url', '')}")
        
        headers = request_data.get("headers", {})
        if headers:
            typer.echo("\nHeaders:")
            for key, value in headers.items():
                typer.echo(f"  {key}: {value}")
        
        data = request_data.get("data")
        if data:
            typer.echo("\nData:")
            typer.echo(json.dumps(data, indent=2))
        
        if execute:
            typer.echo("\nExecuting request...")
            request(
                endpoint=request_data.get("url", ""),
                method=request_data.get("method", "GET"),
                data=json.dumps(data) if data else None,
                query=json.dumps(request_data.get("query", {})) if request_data.get("query") else None,
            )
    
    except (json.JSONDecodeError, IOError) as e:
        typer.echo(f"Error loading request: {str(e)}", err=True)

def _ensure_requests_dir():
    """Ensure the requests directory exists."""
    if not os.path.exists(REQUESTS_DIR):
        os.makedirs(REQUESTS_DIR, exist_ok=True)

def _save_request(name: str, method: str, url: str, headers: Dict, data: Dict, response):
    """Save a request for future use."""
    _ensure_requests_dir()
    
    file_path = os.path.join(REQUESTS_DIR, f"{name}.json")
    
    request_data = {
        "method": method,
        "url": url,
        "headers": headers,
        "data": data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "response": {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.text,
        }
    }
    
    try:
        with open(file_path, "w") as f:
            json.dump(request_data, f, indent=2)
        typer.echo(f"\nRequest saved as '{name}'")
    except IOError as e:
        typer.echo(f"Error saving request: {str(e)}", err=True) 