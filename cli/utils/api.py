"""API client for interacting with the AI models."""

from typing import Any, Dict, List, Optional

# Import the model factory
from ..ai_agent_models.model_factory import get_available_models, get_model


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
    Make a request to the local AI model.

    Args:
        endpoint: API endpoint path (used to determine the type of request)
        method: HTTP method (for compatibility)
        data: Request data
        params: Query parameters (unused)
        loading_message: Custom loading message
        use_local_model: Whether to use a local model (should always be True)
        local_model_name: Name of the local model to use (e.g., "deepseek-r1:7b")
    """
    # Get model
    model = get_model(local_model_name)

    if not model:
        return {
            "error": True,
            "message": f"No local model available. Model '{local_model_name}' not found.",
        }

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

    else:
        # Unsupported endpoint
        return {"error": True, "message": f"Unsupported endpoint: {endpoint}"}


def get_available_local_models() -> List[str]:
    """
    Get a list of available local models.

    Returns:
        List of model names or empty list if no models are available
    """
    models = get_available_models()
    return [name for name, info in models.items() if info.get("available", False)]
