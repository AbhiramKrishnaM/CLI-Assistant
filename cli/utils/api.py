"""API client for interacting with the AI models."""

from typing import Any, Dict, List, Optional

import requests
from rich import print

# Import the model factory
from ..ai_agent_models.model_factory import get_available_models, get_model
from .config import get_config_value
from .formatting import loading_spinner


def api_request(
    endpoint: str,
    method: str = "GET",
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    loading_message: Optional[str] = None,
    use_local_model: bool = True,  # Default to using local models
    local_model_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Make a request to the AI model or API backend.

    Args:
        endpoint: API endpoint to call
        method: HTTP method
        data: Request data
        params: Query parameters
        loading_message: Custom loading message
        use_local_model: Whether to use a local model instead of the API
        local_model_name: Name of the local model to use (e.g., "deepseek-r1: 7b")
    """
    # Check if we should use local model
    if use_local_model and endpoint in [
        "/text/generate",
        "/code/generate",
        "/code/explain",
    ]:
        # Get model
        model = get_model(local_model_name)

        if model:
            if endpoint == "/text/generate" and method == "POST":
                # Extract parameters from data
                prompt = data.get("prompt", "") if data else ""
                temperature = data.get("temperature", 0.7) if data else 0.7
                max_length = data.get("max_length") if data else None
                system_prompt = data.get("system_prompt") if data else None
                stream = data.get("stream", True) if data else True

                # Generate text using local model
                return model.generate_text(
                    prompt=prompt,
                    temperature=temperature,
                    max_length=max_length,
                    system_prompt=system_prompt,
                    stream=stream,
                )

            elif endpoint == "/code/generate" and method == "POST":
                # Extract parameters from data
                description = data.get("description", "") if data else ""
                language = data.get("language", "python") if data else "python"
                temperature = data.get("temperature", 0.7) if data else 0.7
                max_length = data.get("max_length") if data else None

                # Generate code using local model
                return model.generate_code(
                    description=description,
                    language=language,
                    temperature=temperature,
                    max_length=max_length,
                )

            elif endpoint == "/code/explain" and method == "POST":
                # Extract parameters from data
                code = data.get("code", "") if data else ""
                language = data.get("language") if data else None

                # Create a prompt for code explanation
                prompt = f"""# Task: Explain the following {language or 'code'}

```
{code}
```

# Explanation:
"""

                # Generate explanation using text generation
                return model.generate_text(
                    prompt=prompt,
                    temperature=0.3,  # Lower temperature for more focused explanation
                    stream=data.get("stream", True) if data else True,
                )

    # Otherwise, proceed with regular API request
    base_url = get_config_value("backend.url", "http: //localhost: 8000")
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
                method=method, url=url, json=data, params=params, timeout=timeout
            )

        # Raise exception for error status codes
        response.raise_for_status()

        # Type the response as Dict[str, Any]
        response_data: Dict[str, Any] = response.json()
        return response_data
    except requests.RequestException as e:
        print(f"[bold red]Error communicating with the backend: [/bold red] {str(e)}")
        if hasattr(e, "response") and e.response is not None:
            try:
                error_detail = e.response.json().get("detail", str(e))
                print(f"[red]API Error: [/red] {error_detail}")
            except ValueError:
                print(f"[red]API Error: [/red] {e.response.text}")

        # Return empty response with error information
        return {
            "error": True,
            "message": str(e),
            "status_code": (
                e.response.status_code
                if hasattr(e, "response") and e.response is not None
                else None
            ),
        }
    except Exception as e:
        print(f"[bold red]Unexpected error: [/bold red] {str(e)}")
        return {"error": True, "message": str(e)}


def get_available_local_models() -> List[str]:
    """
    Get a list of available local models.

    Returns:
        List of model names or empty list if no models are available
    """
    models = get_available_models()
    return [name for name, info in models.items() if info.get("available", False)]
