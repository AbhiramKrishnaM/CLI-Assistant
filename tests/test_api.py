"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from shared.models.code import CodeGenerationRequest, CodeExplanationRequest

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "message": "AI CLI Assistant API is running"}

def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_code_generate_endpoint(mock_model_manager):
    """Test code generation endpoint."""
    request_data = {
        "description": "A function to calculate the factorial of a number",
        "language": "python",
        "temperature": 0.7,
        "max_length": 512
    }
    
    response = client.post("/code/generate", json=request_data)
    assert response.status_code == 200
    assert "code" in response.json()
    assert "language" in response.json()
    assert "model_used" in response.json()
    
    # Verify the mock was called correctly
    mock_model_manager.generate_text.assert_called_once()
    call_args = mock_model_manager.generate_text.call_args[1]
    assert call_args["model_type"] == "code_generation"
    assert "factorial" in call_args["prompt"]
    assert call_args["temperature"] == 0.7
    assert call_args["max_length"] == 512

def test_code_explain_endpoint(mock_model_manager):
    """Test code explanation endpoint."""
    request_data = {
        "code": """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
        """,
        "language": "python",
        "detail_level": "medium"
    }
    
    response = client.post("/code/explain", json=request_data)
    assert response.status_code == 200
    assert "explanation" in response.json()
    assert "language_detected" in response.json()
    assert "model_used" in response.json()
    
    # Verify the mock was called correctly
    mock_model_manager.generate_text.assert_called_once()
    call_args = mock_model_manager.generate_text.call_args[1]
    assert call_args["model_type"] == "text_generation"
    assert "factorial" in call_args["prompt"]

def test_languages_endpoint():
    """Test the supported languages endpoint."""
    response = client.get("/code/languages")
    assert response.status_code == 200
    assert "languages" in response.json()
    
    # Check that common languages are in the list
    languages = response.json()["languages"]
    assert "python" in languages
    assert "javascript" in languages

def test_terminal_command_endpoint(mock_model_manager):
    """Test the terminal command suggestion endpoint."""
    request_data = {
        "description": "List all files in a directory",
        "platform": "mac"
    }
    
    response = client.post("/terminal/suggest", json=request_data)
    assert response.status_code == 200
    assert "command" in response.json()
    assert "explanation" in response.json()
    assert "model_used" in response.json()
    
    # Verify the mock was called with the right parameters
    mock_model_manager.generate_text.assert_called_once()
    call_args = mock_model_manager.generate_text.call_args[1]
    assert call_args["model_type"] == "text_generation"
    assert "List all files" in call_args["prompt"]
    assert "mac" in call_args["prompt"]

def test_terminal_explain_endpoint(mock_model_manager):
    """Test the terminal command explanation endpoint."""
    request_data = {
        "command": "ls -la"
    }
    
    response = client.post("/terminal/explain", json=request_data)
    assert response.status_code == 200
    assert "explanation" in response.json()
    assert "model_used" in response.json()
    
    # Verify the mock was called with the right parameters
    mock_model_manager.generate_text.assert_called_once()
    call_args = mock_model_manager.generate_text.call_args[1]
    assert call_args["model_type"] == "text_generation"
    assert "ls -la" in call_args["prompt"]

def test_git_commit_endpoint(mock_model_manager):
    """Test the git commit message generation endpoint."""
    request_data = {
        "changes": [
            {"status": "M", "file_path": "main.py"},
            {"status": "A", "file_path": "utils.py"}
        ],
        "message_type": "conventional"
    }
    
    response = client.post("/git/commit-message", json=request_data)
    assert response.status_code == 200
    assert "message" in response.json()
    assert "model_used" in response.json() 