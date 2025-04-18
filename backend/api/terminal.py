"""API endpoints for terminal command suggestions and explanations."""
import logging
from fastapi import APIRouter, HTTPException
from shared.models.terminal import (
    CommandSuggestionRequest, 
    CommandSuggestionResponse,
    CommandExplanationRequest,
    CommandExplanationResponse,
    CommandSuggestion,
)
from backend.services.model_manager import model_manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/suggest", response_model=CommandSuggestionResponse)
async def suggest_command(request: CommandSuggestionRequest):
    """Suggest terminal commands based on a description."""
    logger.info(f"Command suggestion request: {request.description}")
    
    try:
        # Get the text generation model
        model = model_manager.get_model("text_generation")
        if not model:
            raise HTTPException(status_code=503, detail="Text generation model not available")
        
        # Mock implementation - would be replaced with actual model call
        # In a real implementation, we would create a proper prompt
        # and use the model to generate suggestions
        
        # Return mock suggestions for development
        return CommandSuggestionResponse(
            suggestions=[
                CommandSuggestion(
                    command=f"command1 --option {request.description.split()[0]}",
                    explanation="This is a mock suggestion for demonstration purposes.",
                    platform=request.platform if request.platform != "auto" else "linux",
                    confidence=0.9,
                ),
                CommandSuggestion(
                    command=f"command2 -a -b {request.description.split()[0]}",
                    explanation="This is another mock suggestion for demonstration purposes.",
                    platform=request.platform if request.platform != "auto" else "linux",
                    confidence=0.7,
                ),
            ],
            model_used=model.model_id,
        )
        
    except Exception as e:
        logger.error(f"Error suggesting commands: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error suggesting commands: {str(e)}")


@router.post("/explain", response_model=CommandExplanationResponse)
async def explain_command(request: CommandExplanationRequest):
    """Explain a terminal command."""
    logger.info(f"Command explanation request: {request.command}")
    
    try:
        # Get the text generation model
        model = model_manager.get_model("text_generation")
        if not model:
            raise HTTPException(status_code=503, detail="Text generation model not available")
        
        # Mock implementation - would be replaced with actual model call
        # In a real implementation, we would create a proper prompt
        # and use the model to generate an explanation
        
        # Return mock explanation for development
        parts = [
            {"part": request.command.split()[0], "explanation": "This is the command name"},
        ]
        
        for i, arg in enumerate(request.command.split()[1:], 1):
            if arg.startswith("-"):
                parts.append({"part": arg, "explanation": f"This is option {i}"})
            else:
                parts.append({"part": arg, "explanation": f"This is argument {i}"})
        
        return CommandExplanationResponse(
            command=request.command,
            explanation=f"This is a mock explanation for: {request.command}",
            parts=parts,
            model_used=model.model_id,
        )
        
    except Exception as e:
        logger.error(f"Error explaining command: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error explaining command: {str(e)}")


@router.get("/platforms")
async def list_supported_platforms():
    """List supported platforms for terminal commands."""
    return {
        "platforms": [
            "linux",
            "mac",
            "windows",
            "auto",
        ]
    } 