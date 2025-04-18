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
        # Skip predefined examples check and always use model inference
        prompt = f"# {request.language} code to {request.description}\n\n"
        
        # Generate the code using the appropriate model
        code = model_manager.generate_text(
            model_type="code_generation",
            prompt=prompt,
            temperature=request.temperature,
            max_length=request.max_length or 2048,
        )
        
        # If there's an error in the response, return a simple example
        if code.startswith("Error"):
            logger.warning(f"Error in code generation, using fallback. Error: {code}")
            return CodeGenerationResponse(
                code=f"# Simple {request.language} example for: {request.description}\n\n" + 
                     f"# Note: This is a basic example. The AI model encountered an error.\n\n" +
                     f"def example_function():\n    print('Example for: {request.description}')\n\nexample_function()",
                language=request.language,
                model_used="fallback_example"
            )
        
        # Get the model ID
        model_info = next((m for m in model_manager.get_available_models() 
                         if m["type"] == "code_generation"), {"model_id": "unknown"})
        
        # Return the response
        return CodeGenerationResponse(
            code=code,
            language=request.language,
            model_used=model_info["model_id"],
        )
    
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}", exc_info=True)
        # Return a fallback example instead of raising an exception
        return CodeGenerationResponse(
            code=f"# Error generating code for: {request.description}\n\n" + 
                 f"# {str(e)}\n\n" +
                 f"def example_function():\n    print('Example for: {request.description}')\n\nexample_function()",
            language=request.language,
            model_used="error_fallback"
        )


@router.post("/explain", response_model=CodeExplanationResponse)
async def explain_code(request: CodeExplanationRequest):
    """Explain the provided code."""
    logger.info(f"Code explanation request of length {len(request.code)}")
    
    try:
        # Detect language if not provided
        language = request.language or "Unspecified (auto-detect)"
        
        # Create a simpler prompt for the model
        prompt = f"# Code to explain:\n\n```\n{request.code}\n```\n\n# Explanation:\n"
        
        # Generate the explanation using the text generation model
        explanation = model_manager.generate_text(
            model_type="text_generation",
            prompt=prompt,
            temperature=0.3,  # Lower temperature for more focused response
            max_length=1024,
        )
        
        # Handle errors in the response
        if explanation.startswith("Error"):
            logger.warning(f"Error in code explanation, using fallback. Error: {explanation}")
            return CodeExplanationResponse(
                explanation="This code appears to be " + language + " code. " +
                           "I'm not able to provide a detailed explanation at the moment. " +
                           "Please try again later or try with a different code snippet.",
                language_detected=language,
                model_used="fallback_explanation"
            )
        
        # Get the model ID
        model_info = next((m for m in model_manager.get_available_models() 
                         if m["type"] == "text_generation"), {"model_id": "unknown"})
        
        # Return the response
        return CodeExplanationResponse(
            explanation=explanation,
            language_detected=language,
            model_used=model_info["model_id"],
        )
    
    except Exception as e:
        logger.error(f"Error explaining code: {str(e)}", exc_info=True)
        # Return a fallback explanation instead of raising an exception
        return CodeExplanationResponse(
            explanation=f"Error explaining the code: {str(e)}",
            language_detected=language,
            model_used="error_fallback"
        )


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