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
        # Get the code generation model
        model = model_manager.get_model("code_generation")
        if not model:
            raise HTTPException(status_code=503, detail="Code generation model not available")
        
        # Create a prompt for the model
        prompt = f"""
        You are an expert {request.language} developer.
        Generate {request.language} code based on this description:
        
        {request.description}
        
        Provide only the code without any additional explanation.
        """
        
        # Generate the code
        code = model.generate(
            prompt=prompt,
            temperature=request.temperature,
            max_length=request.max_length or 1024,
        )
        
        # Return the response
        return CodeGenerationResponse(
            code=code,
            language=request.language,
            model_used=model.model_id,
        )
    
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating code: {str(e)}")


@router.post("/explain", response_model=CodeExplanationResponse)
async def explain_code(request: CodeExplanationRequest):
    """Explain the provided code."""
    logger.info(f"Code explanation request of length {len(request.code)}")
    
    try:
        # Get the text generation model
        model = model_manager.get_model("text_generation")
        if not model:
            raise HTTPException(status_code=503, detail="Text generation model not available")
        
        # Detect language if not provided
        language = request.language or "Unspecified (auto-detect)"
        
        # Create a prompt for the model
        detail_level_prompt = {
            "brief": "Provide a brief overview of what this code does.",
            "medium": "Explain what this code does with moderate detail.",
            "detailed": "Provide a detailed explanation of this code, including how it works and potential issues."
        }.get(request.detail_level, "Explain what this code does.")
        
        prompt = f"""
        You are an expert code reviewer.
        Explain the following {language} code:
        
        ```
        {request.code}
        ```
        
        {detail_level_prompt}
        """
        
        # Generate the explanation
        explanation = model.generate(
            prompt=prompt,
            temperature=0.3,  # Lower temperature for more focused response
            max_length=1024,
        )
        
        # Return the response
        return CodeExplanationResponse(
            explanation=explanation,
            language_detected=language,
            model_used=model.model_id,
        )
    
    except Exception as e:
        logger.error(f"Error explaining code: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error explaining code: {str(e)}")


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