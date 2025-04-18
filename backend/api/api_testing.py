"""API endpoints for API testing and formatting."""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import httpx

logger = logging.getLogger(__name__)
router = APIRouter()


class APIRequestModel(BaseModel):
    """Model for an API request."""
    
    url: str = Field(..., description="API endpoint URL")
    method: str = Field("GET", description="HTTP method (GET, POST, PUT, DELETE, etc.)")
    headers: Optional[Dict[str, str]] = Field(None, description="Request headers")
    data: Optional[Dict[str, Any]] = Field(None, description="Request data/body")
    params: Optional[Dict[str, str]] = Field(None, description="Query parameters")
    timeout: int = Field(30, description="Request timeout in seconds")


class APIResponseModel(BaseModel):
    """Model for an API response."""
    
    status_code: int = Field(..., description="HTTP status code")
    headers: Dict[str, str] = Field(..., description="Response headers")
    content: Any = Field(..., description="Response content")
    time_taken: float = Field(..., description="Request time in seconds")


class APIExplainRequest(BaseModel):
    """Request to explain an API response."""
    
    request: APIRequestModel = Field(..., description="Original API request")
    response: APIResponseModel = Field(..., description="API response to explain")


class APIExplainResponse(BaseModel):
    """Response with API explanation."""
    
    explanation: str = Field(..., description="Explanation of the API response")
    status_explanation: str = Field(..., description="Explanation of the status code")
    headers_explanation: Dict[str, str] = Field(..., description="Explanation of important headers")
    model_used: str = Field(..., description="Name of the model used")


@router.post("/request", response_model=APIResponseModel)
async def make_api_request(request: APIRequestModel):
    """Make an API request and return the response."""
    logger.info(f"API request: {request.method} {request.url}")
    
    try:
        async with httpx.AsyncClient() as client:
            # Prepare the request
            method = request.method.upper()
            
            # Make the request and measure time
            import time
            start_time = time.time()
            response = await client.request(
                method=method,
                url=request.url,
                headers=request.headers,
                json=request.data,
                params=request.params,
                timeout=request.timeout,
            )
            elapsed = time.time() - start_time
            
            # Process the response
            try:
                content = response.json()
            except Exception:
                content = response.text
                
            # Convert headers to dict (they might be a multi-dict)
            headers_dict = dict(response.headers.items())
            
            return APIResponseModel(
                status_code=response.status_code,
                headers=headers_dict,
                content=content,
                time_taken=elapsed,
            )
            
    except httpx.RequestError as e:
        logger.error(f"Error making API request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error making API request: {str(e)}")


@router.post("/explain", response_model=APIExplainResponse)
async def explain_api_response(request: APIExplainRequest):
    """Explain an API response."""
    logger.info(f"API explanation request for {request.request.method} {request.request.url}")
    
    try:
        from backend.services.model_manager import model_manager
        model = model_manager.get_model("text_generation")
        if not model:
            raise HTTPException(status_code=503, detail="Text generation model not available")
        
        # Mock implementation - would be replaced with actual model call
        # In a real implementation, we would create a proper prompt
        # and use the model to generate explanations
        
        # Generate mock explanations
        status_explanation = f"Status code {request.response.status_code}"
        if 200 <= request.response.status_code < 300:
            status_explanation += " indicates the request was successful."
        elif 400 <= request.response.status_code < 500:
            status_explanation += " indicates a client error."
        elif 500 <= request.response.status_code < 600:
            status_explanation += " indicates a server error."
            
        # Explain important headers
        headers_explanation = {}
        for key, value in request.response.headers.items():
            if key.lower() in ["content-type", "content-length", "authorization"]:
                headers_explanation[key] = f"This header indicates {key.lower().replace('-', ' ')}."
                
        # General explanation
        explanation = f"This is a mock explanation for a {request.request.method} request to {request.request.url}."
        if isinstance(request.response.content, dict) and len(request.response.content) > 0:
            explanation += f" The response contains {len(request.response.content)} fields."
            
        return APIExplainResponse(
            explanation=explanation,
            status_explanation=status_explanation,
            headers_explanation=headers_explanation,
            model_used=model.model_id,
        )
        
    except Exception as e:
        logger.error(f"Error explaining API response: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error explaining API response: {str(e)}")


@router.get("/methods")
async def list_http_methods():
    """List supported HTTP methods."""
    return {
        "methods": [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "HEAD",
            "OPTIONS",
        ]
    } 