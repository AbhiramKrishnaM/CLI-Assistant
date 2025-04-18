"""Main entry point for the FastAPI backend service."""
import logging
import sys
import os
from pathlib import Path

# Add parent directory to sys.path to allow relative imports
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI CLI Assistant API",
    description="Backend API for the AI-powered CLI assistant",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from backend.api.code import router as code_router
from backend.api.terminal import router as terminal_router
from backend.api.git import router as git_router
from backend.api.docs import router as docs_router
from backend.api.api_testing import router as api_testing_router

app.include_router(code_router, prefix="/code", tags=["code"])
app.include_router(terminal_router, prefix="/terminal", tags=["terminal"])
app.include_router(git_router, prefix="/git", tags=["git"])
app.include_router(docs_router, prefix="/docs", tags=["docs"])
app.include_router(api_testing_router, prefix="/api-testing", tags=["api-testing"])

# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": str(exc)},
    )

@app.get("/", tags=["status"])
async def root():
    """Root endpoint to check API status."""
    return {"status": "online", "message": "AI CLI Assistant API is running"}

@app.get("/health", tags=["status"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)