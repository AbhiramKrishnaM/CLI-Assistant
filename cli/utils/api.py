"""API client for interacting with the backend."""
import requests
import json
from typing import Dict, Any, Optional
from rich import print
from .config import get_config_value

def api_request(
    endpoint: str, 
    method: str = "GET", 
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make a request to the API backend."""
    base_url = get_config_value("backend.url", "http://localhost:8000")
    timeout = get_config_value("backend.timeout", 30)
    
    url = f"{base_url}/{endpoint.lstrip('/')}"
    
    try:
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