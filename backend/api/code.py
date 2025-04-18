"""API endpoints for code generation and explanation."""
import logging
from fastapi import APIRouter, HTTPException, Depends
from shared.models.code import (
    CodeGenerationRequest,
    CodeGenerationResponse,
    CodeExplanationRequest,
    CodeExplanationResponse,
)
from backend.services.model_manager import model_manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest):
    """Generate code based on a description."""
    logger.info(f"Code generation request for {request.language}")
    
    try:
        # Create prompt for code generation
        prompt = f"# {request.language} code to {request.description}\n\n"
        
        # Log the request and model details
        logger.info(f"Using model: {model_manager.model_configs['code_generation']['model_id']}")
        
        # Generate the code using the appropriate model
        code = model_manager.generate_text(
            model_type="code_generation",
            prompt=prompt,
            temperature=request.temperature,
            max_length=request.max_length or 2048,
        )
        
        # If there's an error in the response, return error
        if code.startswith("Error"):
            logger.error(f"Error in code generation: {code}")
            raise HTTPException(status_code=500, detail=f"Code generation failed: {code}")
        
        # Get the model ID
        model_info = next((m for m in model_manager.get_available_models() 
                         if m["type"] == "code_generation"), {"model_id": "unknown"})
        
        model_id = model_info["model_id"]
        
        # Return the response with additional information
        return CodeGenerationResponse(
            code=code,
            language=request.language,
            model_used=model_id,
        )
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Code generation failed: {str(e)}")


@router.post("/explain", response_model=CodeExplanationResponse)
async def explain_code(request: CodeExplanationRequest):
    """Explain the provided code."""
    logger.info(f"Code explanation request of length {len(request.code)}")
    
    try:
        # Detect language if not provided
        language = request.language or "Unspecified (auto-detect)"
        
        # Create a more detailed prompt for the model
        prompt = f"""# Task: Explain the following {language} code

```{language}
{request.code}
```

# Explanation:
This code"""
        
        # Log the request and model details
        logger.info(f"Using model: {model_manager.model_configs['text_generation']['model_id']}")
        
        # Generate the explanation using the text generation model
        explanation = model_manager.generate_text(
            model_type="text_generation",
            prompt=prompt,
            temperature=0.3,  # Lower temperature for more focused response
            max_length=1024,
        )
        
        # Handle errors in the response
        if explanation.startswith("Error"):
            logger.error(f"Error in code explanation: {explanation}")
            raise HTTPException(status_code=500, detail=f"Code explanation failed: {explanation}")
        
        # Get the model ID
        model_info = next((m for m in model_manager.get_available_models() 
                         if m["type"] == "text_generation"), {"model_id": "unknown"})
        model_id = model_info["model_id"]
        
        # Return the response with additional information
        return CodeExplanationResponse(
            explanation=explanation,
            language_detected=language,
            model_used=model_id,
        )
    
    except Exception as e:
        logger.error(f"Error explaining code: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Code explanation failed: {str(e)}")


@router.get("/languages")
async def list_supported_languages():
    """List supported programming languages."""
    return {
        "languages": [
            "python",
            "javascript",
            "typescript",
            "java",
            "c",
            "cpp",
            "csharp",
            "go",
            "ruby",
            "rust",
            "php",
            "swift",
            "kotlin",
            "sql",
            "bash",
            "html",
            "css",
        ]
    } 