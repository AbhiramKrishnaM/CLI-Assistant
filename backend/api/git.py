"""API endpoints for git operations assistance."""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from backend.services.model_manager import model_manager

logger = logging.getLogger(__name__)
router = APIRouter()


class GitDiff(BaseModel):
    """Model for git diff information."""
    
    added: List[str] = Field(default_factory=list, description="Added lines")
    removed: List[str] = Field(default_factory=list, description="Removed lines")
    files: List[str] = Field(default_factory=list, description="Changed files")


class CommitMessageRequest(BaseModel):
    """Request model for commit message generation."""
    
    diff: GitDiff = Field(..., description="Git diff information")
    message_type: str = Field("conventional", description="Type of commit message (conventional or descriptive)")


class CommitMessageResponse(BaseModel):
    """Response model for commit message generation."""
    
    message: str = Field(..., description="Generated commit message")
    model_used: str = Field(..., description="Name of the model used")


class PRDescriptionRequest(BaseModel):
    """Request model for PR description generation."""
    
    branch_name: str = Field(..., description="Current branch name")
    commits: List[str] = Field(..., description="List of commit messages in the PR")
    diff_summary: Optional[GitDiff] = Field(None, description="Summary of changes")


class PRDescriptionResponse(BaseModel):
    """Response model for PR description generation."""
    
    title: str = Field(..., description="Suggested PR title")
    description: str = Field(..., description="Generated PR description")
    model_used: str = Field(..., description="Name of the model used")


@router.post("/commit-message", response_model=CommitMessageResponse)
async def generate_commit_message(request: CommitMessageRequest):
    """Generate a commit message based on git diff."""
    logger.info(f"Commit message request for {len(request.diff.files)} files")
    
    try:
        # Get the text generation model
        model = model_manager.get_model("text_generation")
        if not model:
            raise HTTPException(status_code=503, detail="Text generation model not available")
        
        # Mock implementation - would be replaced with actual model call
        # In a real implementation, we would create a proper prompt based on the diff
        # and use the model to generate a commit message
        
        # Sample mock commit message based on files
        if request.message_type == "conventional":
            message_type = "feat"
            if any(f.endswith((".md", ".txt")) for f in request.diff.files):
                message_type = "docs"
            elif any("test" in f for f in request.diff.files):
                message_type = "test"
                
            message = f"{message_type}: update files"
            if request.diff.files:
                message += f" ({', '.join(request.diff.files[:2])})"
        else:
            message = f"Update {len(request.diff.files)} files"
            
        return CommitMessageResponse(
            message=message,
            model_used=model.model_id,
        )
        
    except Exception as e:
        logger.error(f"Error generating commit message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating commit message: {str(e)}")


@router.post("/pr-description", response_model=PRDescriptionResponse)
async def generate_pr_description(request: PRDescriptionRequest):
    """Generate a PR description based on commits."""
    logger.info(f"PR description request for branch {request.branch_name}")
    
    try:
        # Get the text generation model
        model = model_manager.get_model("text_generation")
        if not model:
            raise HTTPException(status_code=503, detail="Text generation model not available")
        
        # Mock implementation - would be replaced with actual model call
        # In a real implementation, we would create a proper prompt based on the commits
        # and use the model to generate a PR description
        
        # Generate title from branch name
        title = request.branch_name.replace("-", " ").replace("_", " ").title()
        if title.startswith("Feature "):
            title = title[8:]
            
        # Generate mock description
        description = f"# {title}\n\n## Changes\n\n"
        
        for commit in request.commits:
            description += f"- {commit}\n"
            
        description += "\n## Testing\n\n- [ ] Tests added for new functionality\n- [ ] All tests passing"
        
        return PRDescriptionResponse(
            title=title,
            description=description,
            model_used=model.model_id,
        )
        
    except Exception as e:
        logger.error(f"Error generating PR description: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating PR description: {str(e)}")


@router.get("/message-types")
async def list_commit_message_types():
    """List supported commit message types."""
    return {
        "types": [
            "conventional",
            "descriptive",
        ]
    } 