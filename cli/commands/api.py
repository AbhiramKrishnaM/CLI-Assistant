"""API request testing and formatting."""

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

import typer
from rich import print
from rich.table import Table

from cli.ai_agent_models.ollama_deepseek_r1_7b import OllamaDeepSeekModel
from cli.utils.api import api_request, get_available_local_models
from cli.utils.config import get_config_value, set_config_value
from cli.utils.formatting import print_error, print_info, print_json, print_success

app = typer.Typer(help="Test and configure Ollama model settings")

# Directory to store saved requests
REQUESTS_DIR = os.path.expanduser("~/.aidev/requests")

# Check if Ollama is available
OLLAMA_AVAILABLE = OllamaDeepSeekModel.is_available()


@app.command()
def request(
    prompt: str = typer.Argument(..., help="Text prompt to send to Ollama"),
    model: str = typer.Option(
        "deepseek-r1:7b", "--model", "-m", help="Ollama model to use"
    ),
    temperature: float = typer.Option(
        0.7, "--temperature", "-t", help="Temperature for generation (0.0-1.0)"
    ),
    no_stream: bool = typer.Option(
        False, "--no-stream", help="Disable streaming for local models"
    ),
) -> None:
    """Make a direct request to Ollama for text generation."""
    if not OLLAMA_AVAILABLE:
        print_error("Ollama is not available. Make sure it's installed and running.")
        print_info("Install instructions: https://github.com/ollama/ollama")
        return

    print(f"Generating text with model {model} (Temperature: {temperature})")

    # Make the request
    response = api_request(
        endpoint="/text/generate",
        method="POST",
        data={
            "prompt": prompt,
            "temperature": temperature,
            "stream": not no_stream,
        },
        loading_message=f"Generating text with {model}...",
        use_local_model=True,
        local_model_name=model,
    )

    # Display the response
    if "error" in response:
        print_error("Request failed")
        print_error(response.get("message", "Unknown error"))
    else:
        print_success("Request successful")
        if no_stream:
            print_json(response, "Response")


@app.command()
def config(
    show_all: bool = typer.Option(False, "--all", help="Show all config values"),
    set_ollama_url: Optional[str] = typer.Option(
        None, "--set-ollama-url", help="Set the Ollama API URL"
    ),
    set_ollama_model: Optional[str] = typer.Option(
        None, "--set-ollama-model", help="Set the default Ollama model"
    ),
    set_ollama_timeout: Optional[int] = typer.Option(
        None, "--set-ollama-timeout", help="Set the Ollama API timeout"
    ),
) -> None:
    """Configure Ollama API settings."""
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

    # Show configuration
    table = Table(title="Ollama Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    # Ollama settings
    ollama_url = get_config_value("ollama.url", "http://localhost:11434/api")
    ollama_model = get_config_value("ollama.default_model", "deepseek-r1:7b")
    ollama_timeout = get_config_value("ollama.timeout", 60)

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
        print_info(
            "To update settings, use the options like --set-ollama-url or --set-ollama-model"
        )
        if not OLLAMA_AVAILABLE:
            print_info(
                "Ollama is not available. Make sure Ollama is installed and running."
            )
            print_info("Install instructions: https://github.com/ollama/ollama")


@app.command()
def models() -> None:
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
        print_info(
            f"Default model ({default_model}) is not available. You might want to update it."
        )
        if models:
            print_info(f"You can use: api config --set-ollama-model {models[0]}")


@app.command()
def list_saved() -> None:
    """List all saved API requests."""
    _ensure_requests_dir()

    saved_requests = []
    for filename in os.listdir(REQUESTS_DIR):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(REQUESTS_DIR, filename), "r") as f:
                    request_data = json.load(f)
                name = filename[:-5]  # Remove .json extension
                saved_requests.append(
                    (
                        name,
                        request_data.get("method", ""),
                        request_data.get("url", ""),
                        request_data.get("timestamp", ""),
                    )
                )
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
    execute: bool = typer.Option(
        False, "--execute", "-e", help="Execute the request after loading"
    ),
) -> None:
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
                prompt=data.get("prompt", ""),
                model=data.get("model", "deepseek-r1:7b"),
                temperature=data.get("temperature", 0.7),
                no_stream=data.get("stream", False),
            )

    except (json.JSONDecodeError, IOError) as e:
        typer.echo(f"Error loading request: {str(e)}", err=True)


def _ensure_requests_dir() -> None:
    """Ensure the requests directory exists."""
    if not os.path.exists(REQUESTS_DIR):
        os.makedirs(REQUESTS_DIR, exist_ok=True)


def _save_request(
    name: str,
    method: str,
    url: str,
    headers: Dict[str, str],
    data: Dict[str, Any],
    response: Any,
) -> None:
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
        },
    }

    try:
        with open(file_path, "w") as f:
            json.dump(request_data, f, indent=2)
        typer.echo(f"\nRequest saved as '{name}'")
    except IOError as e:
        typer.echo(f"Error saving request: {str(e)}", err=True)
