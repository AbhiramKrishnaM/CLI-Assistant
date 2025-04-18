"""API endpoints for text generation."""
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException
from shared.models.text import (
    TextGenerationRequest,
    TextGenerationResponse
)
from backend.services.model_manager import model_manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate", response_model=TextGenerationResponse)
async def generate_text(request: TextGenerationRequest):
    """Generate text based on a prompt."""
    logger.info(f"Text generation request with temperature {request.temperature}")
    
    try:
        # Log the request 
        logger.info(f"Using model: {model_manager.model_configs['text_generation']['model_id']}")
        
        # Generate the response
        response = model_manager.generate_text(
            model_type="text_generation",
            prompt=request.prompt,
            temperature=request.temperature,
            max_length=request.max_length or 1024,
        )
        
        # Check for errors in the response
        if response.startswith("Error"):
            logger.error(f"Error in text generation: {response}")
            raise HTTPException(status_code=500, detail=f"Text generation failed: {response}")
        
        # Get the model ID
        model_info = next((m for m in model_manager.get_available_models() 
                         if m["type"] == "text_generation"), {"model_id": "unknown"})
        model_id = model_info["model_id"]
        
        # Return the generated text
        return TextGenerationResponse(
            text=response,
            prompt=request.prompt,
            model_used=model_id,
            completion_tokens=len(response.split())
        )
    
    except Exception as e:
        logger.error(f"Error generating text: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Text generation failed: {str(e)}")


@router.get("/models")
async def list_models():
    """List all available text generation models."""
    try:
        models = model_manager.get_available_models()
        
        # Filter to just get text generation models
        text_models = [m for m in models if m["type"] == "text_generation"]
        
        return {"models": text_models}
    
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}") 