"""Tests for model integration."""
import pytest
import logging
from cli.ai_agent_models.model_factory import get_model, get_available_models

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Tests that use the real model (slower but more thorough)
@pytest.mark.slow
def test_model_factory_initialization():
    """Test that the model factory initializes properly."""
    models = get_available_models()
    assert len(models) >= 1  # Should have at least one model
    
    # The default model should be available
    default_model = get_model()
    # Skip the test if no models are available (e.g., Ollama is not installed)
    if default_model is None:
        pytest.skip("No AI models available to test")
    
    assert default_model is not None
    assert default_model.model_name in models

@pytest.mark.slow
def test_code_generation():
    """Test code generation."""
    model = get_model()
    # Skip the test if no models are available
    if model is None:
        pytest.skip("No AI models available to test")
    
    description = "Create a function that calculates the Fibonacci sequence up to n terms"
    language = "python"
    
    result = model.generate_code(
        description=description,
        language=language,
        temperature=0.7,
        max_length=1024,
        stream=False
    )
    
    assert result is not None
    assert "code" in result
    code = result["code"]
    assert len(code) > 0
    # Basic check that it looks like Python code
    assert "def" in code

@pytest.mark.slow
def test_text_generation():
    """Test text generation."""
    model = get_model()
    # Skip the test if no models are available
    if model is None:
        pytest.skip("No AI models available to test")
    
    prompt = "Explain the concept of recursion in programming in simple terms."
    
    result = model.generate_text(
        prompt=prompt,
        temperature=0.7,
        max_length=1024,
        stream=False
    )
    
    assert result is not None
    assert "text" in result
    explanation = result["text"]
    assert len(explanation) > 0
    # Check that the explanation mentions recursion
    assert "recurs" in explanation.lower()

@pytest.mark.slow
def test_embeddings():
    """Test embedding model."""
    model = get_model()
    # Skip the test if no models are available
    if model is None:
        pytest.skip("No AI models available to test")
    
    texts = [
        "Python is a programming language",
        "JavaScript runs in the browser",
        "Machine learning is a subset of AI"
    ]
    
    embeddings = model.generate_embeddings(texts)
    
    assert embeddings is not None
    assert len(embeddings) == len(texts)
    assert len(embeddings[0]) > 0  # Should have at least some dimensions

# Mock model for testing
class MockAIModel:
    @property
    def model_name(self):
        return "mock-model"
    
    def generate_text(self, prompt, **kwargs):
        return {
            "text": "This is mock generated text",
            "model_used": "mock-model",
            "completion_tokens": 10
        }
    
    def generate_code(self, description, language, **kwargs):
        return {
            "code": "def mock_function():\n    return 'This is mock code'",
            "language": language,
            "model_used": "mock-model",
            "completion_tokens": 15
        }
    
    def generate_embeddings(self, texts):
        return [[0.1, 0.2, 0.3, 0.4, 0.5]] * len(texts)
    
    @classmethod
    def is_available(cls):
        return True

@pytest.fixture
def mock_ai_model():
    """Fixture for a mock AI model."""
    return MockAIModel()

# Tests that use the mock model (faster for CI/CD)
def test_mock_model(mock_ai_model):
    """Test that the mock model works as expected."""
    assert mock_ai_model is not None
    
    # Test generate_text
    result = mock_ai_model.generate_text(
        prompt="Generate a factorial function"
    )
    assert result["text"] == "This is mock generated text"
    
    # Test generate_code
    result = mock_ai_model.generate_code(
        description="Generate a factorial function",
        language="python"
    )
    assert "def mock_function" in result["code"]
    
    # Test generate_embeddings
    texts = ["Example text 1", "Example text 2", "Example text 3"]
    embeddings = mock_ai_model.generate_embeddings(texts)
    assert len(embeddings) == 3
    assert len(embeddings[0]) == 5  # Mock returns 5-dimensional vectors 