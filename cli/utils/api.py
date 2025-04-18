"""API client for interacting with the backend."""
import requests
import json
from typing import Dict, Any, Optional, List
from rich import print
from .config import get_config_value
from .formatting import loading_spinner
try:
    from .ollama import generate_text_with_ollama, check_ollama_availability
    OLLAMA_AVAILABLE = check_ollama_availability()
except (ImportError, Exception):
    OLLAMA_AVAILABLE = False

def api_request(
    endpoint: str, 
    method: str = "GET", 
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    loading_message: Optional[str] = None,
    use_local_model: bool = False,
    local_model_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Make a request to the API backend or use local Ollama models if specified.
    
    Args:
        endpoint: API endpoint to call
        method: HTTP method
        data: Request data
        params: Query parameters
        loading_message: Custom loading message
        use_local_model: Whether to use a local Ollama model instead of the API
        local_model_name: Name of the local model to use (e.g., "deepseek-r1:7b")
    """
    # Check if we should use local model
    if use_local_model and OLLAMA_AVAILABLE and endpoint == "/text/generate" and method == "POST":
        # Use specified model or default to deepseek-r1:7b
        model_name = local_model_name or "deepseek-r1:7b"
        
        # Extract parameters from data
        prompt = data.get("prompt", "")
        temperature = data.get("temperature", 0.7)
        max_length = data.get("max_length")
        system_prompt = data.get("system_prompt")
        stream = data.get("stream", True)  # Default to streaming
        show_thinking = data.get("show_thinking", True)  # Default to showing thinking
        
        # Generate text using local Ollama model
        return generate_text_with_ollama(
            prompt=prompt,
            model=model_name,
            temperature=temperature,
            max_length=max_length,
            system_prompt=system_prompt,
            stream=stream
        )
    
    # Otherwise, proceed with regular API request
    base_url = get_config_value("backend.url", "http://localhost:8000")
    timeout = get_config_value("backend.timeout", 30)
    
    url = f"{base_url}/{endpoint.lstrip('/')}"
    
    # Use a default loading message based on the endpoint if none provided
    if loading_message is None:
        if "code/generate" in endpoint:
            loading_message = "Generating code..."
        elif "code/explain" in endpoint:
            loading_message = "Analyzing code..."
        elif "text/generate" in endpoint:
            loading_message = "Generating text..."
        elif "docs" in endpoint:
            loading_message = "Searching documentation..."
        else:
            loading_message = "Waiting for response..."
    
    try:
        # Use the loading spinner while waiting for the API response
        with loading_spinner(loading_message):
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=timeout
            )
        
        # Raise exception for error status codes
        response.raise_for_status()
        
        return response.json()
    except requests.RequestException as e:
        print(f"[bold red]Error communicating with the backend:[/bold red] {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json().get('detail', str(e))
                print(f"[red]API Error:[/red] {error_detail}")
            except ValueError:
                print(f"[red]API Error:[/red] {e.response.text}")
        
        # Return empty response with error information
        return {
            "error": True,
            "message": str(e),
            "status_code": e.response.status_code if hasattr(e, 'response') and e.response is not None else None
        }
    except Exception as e:
        print(f"[bold red]Unexpected error:[/bold red] {str(e)}")
        return {"error": True, "message": str(e)}

def get_available_local_models() -> List[str]:
    """
    Get a list of available local models from Ollama.
    
    Returns:
        List of model names or empty list if Ollama is not available
    """
    if OLLAMA_AVAILABLE:
        from .ollama import get_available_models
        return get_available_models()
    return [] 