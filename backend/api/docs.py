"""API endpoints for documentation search and summarization."""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from backend.services.model_manager import model_manager

logger = logging.getLogger(__name__)
router = APIRouter()


class DocSearchRequest(BaseModel):
    """Request model for documentation search."""
    
    query: str = Field(..., description="Search query")
    language: Optional[str] = Field(None, description="Limit search to specific language/tool")
    max_results: int = Field(5, description="Maximum number of results to return")


class DocSearchResult(BaseModel):
    """Model for a single documentation search result."""
    
    title: str = Field(..., description="Title of the documentation")
    content: str = Field(..., description="Content snippet")
    source: str = Field(..., description="Source of the documentation")
    language: str = Field(..., description="Language or tool")
    relevance: float = Field(..., description="Relevance score (0.0-1.0)")


class DocSearchResponse(BaseModel):
    """Response model for documentation search."""
    
    results: List[DocSearchResult] = Field(..., description="Search results")
    total_results: int = Field(..., description="Total number of results found")
    model_used: str = Field(..., description="Name of the model used")


class DocSummarizationRequest(BaseModel):
    """Request model for documentation summarization."""
    
    content: str = Field(..., description="Content to summarize")
    length: str = Field("medium", description="Summary length (short, medium, long)")


class DocSummarizationResponse(BaseModel):
    """Response model for documentation summarization."""
    
    summary: str = Field(..., description="Generated summary")
    model_used: str = Field(..., description="Name of the model used")


@router.post("/search", response_model=DocSearchResponse)
async def search_docs(request: DocSearchRequest):
    """Search documentation based on a query."""
    logger.info(f"Documentation search request: {request.query}")
    
    try:
        # Get the embedding model for search
        model = model_manager.get_model("embedding")
        if not model:
            raise HTTPException(status_code=503, detail="Embedding model not available")
        
        # Mock implementation - would be replaced with actual embedding search
        # In a real implementation, we would:
        # 1. Convert query to embeddings
        # 2. Search in vector database
        # 3. Return most relevant results
        
        # Return mock results for development
        mock_results = []
        for i in range(min(request.max_results, 5)):
            mock_results.append(
                DocSearchResult(
                    title=f"Documentation {i+1} for {request.query}",
                    content=f"This is a mock result for the query: {request.query}. It contains information about the topic.",
                    source=f"docs/{request.language or 'general'}/page{i+1}.md",
                    language=request.language or "general",
                    relevance=1.0 - (i * 0.1),
                )
            )
            
        return DocSearchResponse(
            results=mock_results,
            total_results=len(mock_results),
            model_used=model.model_id,
        )
        
    except Exception as e:
        logger.error(f"Error searching documentation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error searching documentation: {str(e)}")


@router.post("/summarize", response_model=DocSummarizationResponse)
async def summarize_docs(request: DocSummarizationRequest):
    """Summarize documentation content."""
    logger.info(f"Documentation summarization request of length {len(request.content)}")
    
    try:
        # Get the text generation model
        model = model_manager.get_model("text_generation")
        if not model:
            raise HTTPException(status_code=503, detail="Text generation model not available")
        
        # Mock implementation - would be replaced with actual model call
        # In a real implementation, we would create a proper prompt
        # and use the model to generate a summary
        
        # Calculate summary length based on request
        content_length = len(request.content)
        if request.length == "short":
            summary_length = min(content_length // 10, 200)
        elif request.length == "long":
            summary_length = min(content_length // 3, 1000)
        else:  # medium
            summary_length = min(content_length // 5, 500)
            
        # Generate a mock summary
        summary = f"This is a mock summary of length {summary_length} for the provided documentation."
        if content_length > 100:
            summary += f" The content starts with: {request.content[:50]}..."
            
        return DocSummarizationResponse(
            summary=summary,
            model_used=model.model_id,
        )
        
    except Exception as e:
        logger.error(f"Error summarizing documentation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error summarizing documentation: {str(e)}")


@router.get("/languages")
async def list_doc_languages():
    """List available documentation languages/tools."""
    return {
        "languages": [
            "python",
            "javascript",
            "java",
            "git",
            "docker",
            "linux",
            "bash",
            "sql",
        ]
    } 