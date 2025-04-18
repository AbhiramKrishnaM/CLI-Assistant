"""Tests for model integration."""
import pytest
import logging
from backend.services.model_manager import model_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Tests that use the real model manager (slower but more thorough)
@pytest.mark.slow
def test_model_manager_initialization():
    """Test that the model manager initializes properly."""
    assert model_manager is not None
    
    models = model_manager.get_available_models()
    assert len(models) >= 3  # Should have at least code_generation, text_generation, and embedding models
    
    model_types = [model["type"] for model in models]
    assert "code_generation" in model_types
    assert "text_generation" in model_types
    assert "embedding" in model_types

@pytest.mark.slow
def test_code_generation():
    """Test code generation model."""
    prompt = """
    You are an expert Python developer.
    Generate Python code based on this description:
    
    Create a function that calculates the Fibonacci sequence up to n terms.
    
    Provide only the code without any additional explanation.
    """
    
    code = model_manager.generate_text(
        model_type="code_generation",
        prompt=prompt,
        temperature=0.7,
        max_length=1024,
    )
    
    assert code is not None
    assert len(code) > 0
    # Basic check that it looks like Python code
    assert "def" in code or "function" in code

@pytest.mark.slow
def test_text_generation():
    """Test text generation model."""
    prompt = """
    Explain the concept of recursion in programming in simple terms.
    """
    
    explanation = model_manager.generate_text(
        model_type="text_generation",
        prompt=prompt,
        temperature=0.7,
        max_length=1024,
    )
    
    assert explanation is not None
    assert len(explanation) > 0
    # Check that the explanation mentions recursion
    assert "recurs" in explanation.lower()

@pytest.mark.slow
def test_embeddings():
    """Test embedding model."""
    texts = [
        "Python is a programming language",
        "JavaScript runs in the browser",
        "Machine learning is a subset of AI"
    ]
    
    embeddings = model_manager.generate_embeddings(texts)
    
    assert embeddings is not None
    assert len(embeddings) == len(texts)
    assert len(embeddings[0]) > 0  # Should have at least some dimensions

@pytest.mark.slow
def test_model_unloading():
    """Test that models can be unloaded."""
    # First ensure the model is loaded
    model_manager.get_model("code_generation")
    
    # Then unload it
    result = model_manager.unload_model("code_generation")
    assert result is True
    
    # Check available models
    models = model_manager.get_available_models()
    code_model = next((m for m in models if m["type"] == "code_generation"), None)
    assert code_model is not None
    assert code_model["loaded"] is False

# Tests that use the mock model manager (faster for CI/CD)
def test_mock_model_manager(mock_model_manager):
    """Test that the mock model manager works as expected."""
    assert mock_model_manager is not None
    
    # Test get_available_models
    models = mock_model_manager.get_available_models()
    assert len(models) == 3
    
    # Test get_model
    model = mock_model_manager.get_model("code_generation")
    assert model is not None
    
    # Test generate_text
    text = mock_model_manager.generate_text(
        model_type="code_generation",
        prompt="Generate a factorial function",
    )
    assert text == "This is mock generated text"
    
    # Test generate_embeddings
    texts = ["Example text 1", "Example text 2", "Example text 3"]
    embeddings = mock_model_manager.generate_embeddings(texts)
    assert len(embeddings) == 3
    assert len(embeddings[0]) == 5  # Mock returns 5-dimensional vectors
    
    # Test unload_model
    result = mock_model_manager.unload_model("code_generation")
    assert result is True 