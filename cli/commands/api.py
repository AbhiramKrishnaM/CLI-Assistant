"""API request testing and formatting."""
import json
import os
import typer
import requests
from typing import Dict, Optional
from datetime import datetime

app = typer.Typer(help="Test and format API requests")

# Directory to store saved requests
REQUESTS_DIR = os.path.expanduser("~/.aidev/requests")

@app.command()
def request(
    url: str = typer.Argument(..., help="API endpoint URL"),
    method: str = typer.Option("GET", "--method", "-m", help="HTTP method (GET, POST, PUT, DELETE)"),
    headers: Optional[str] = typer.Option(None, "--headers", "-h", help="JSON headers string"),
    data: Optional[str] = typer.Option(None, "--data", "-d", help="JSON data string for request body"),
    save: Optional[str] = typer.Option(None, "--save", "-s", help="Save request with this name"),
    timeout: int = typer.Option(30, "--timeout", "-t", help="Request timeout in seconds"),
):
    """Make an API request and display the response."""
    # Process headers
    header_dict = {}
    if headers:
        try:
            header_dict = json.loads(headers)
        except json.JSONDecodeError:
            typer.echo("Error: Headers must be a valid JSON object", err=True)
            return
    
    # Process data
    data_dict = None
    if data:
        try:
            data_dict = json.loads(data)
        except json.JSONDecodeError:
            typer.echo("Error: Data must be a valid JSON object", err=True)
            return
    
    # Make the request
    try:
        method = method.upper()
        typer.echo(f"Making {method} request to {url}...")
        
        response = requests.request(
            method=method,
            url=url,
            headers=header_dict,
            json=data_dict,
            timeout=timeout,
        )
        
        # Format response time
        elapsed = response.elapsed.total_seconds()
        elapsed_str = f"{elapsed:.2f}s"
        
        # Get the response content
        try:
            response_json = response.json()
            response_content = json.dumps(response_json, indent=2)
            content_type = "application/json"
        except json.JSONDecodeError:
            response_content = response.text
            content_type = response.headers.get("Content-Type", "text/plain")
        
        # Display response
        typer.echo(f"\nStatus: {response.status_code} {response.reason}")
        typer.echo(f"Time: {elapsed_str}")
        typer.echo(f"Content-Type: {content_type}")
        typer.echo("\nResponse Headers:")
        for key, value in response.headers.items():
            typer.echo(f"  {key}: {value}")
        
        typer.echo("\nResponse Body:")
        typer.echo(response_content)
        
        # Save request if specified
        if save:
            _save_request(save, method, url, header_dict, data_dict, response)
            
    except requests.RequestException as e:
        typer.echo(f"Error: {str(e)}", err=True)

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
                url=request_data.get("url", ""),
                method=request_data.get("method", "GET"),
                headers=json.dumps(headers) if headers else None,
                data=json.dumps(data) if data else None,
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