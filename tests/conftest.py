"""Pytest configuration file with fixtures."""
import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Add parent directory to sys.path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_model_manager():
    """Fixture to mock the model manager for faster tests."""
    with patch('backend.services.model_manager.model_manager') as mock_manager:
        # Mock the generate_text method
        mock_manager.generate_text.return_value = "This is mock generated text"
        
        # Mock the generate_embeddings method
        mock_manager.generate_embeddings.return_value = [[0.1, 0.2, 0.3, 0.4, 0.5] for _ in range(3)]
        
        # Mock the get_available_models method
        mock_manager.get_available_models.return_value = [
            {
                "type": "code_generation",
                "model_id": "gpt2",
                "loaded": True,
                "device": "cpu",
                "quantization": "none",
            },
            {
                "type": "text_generation",
                "model_id": "gpt2",
                "loaded": True,
                "device": "cpu",
                "quantization": "none",
            },
            {
                "type": "embedding",
                "model_id": "sentence-transformers/all-MiniLM-L6-v2",
                "loaded": True,
                "device": "cpu",
            }
        ]
        
        # Mock the get_model method
        mock_manager.get_model.return_value = MagicMock()
        
        # Mock the unload_model method
        mock_manager.unload_model.return_value = True
        
        yield mock_manager

@pytest.fixture
def temp_code_file(tmp_path):
    """Create a temporary Python file for testing code-related functionality."""
    file_content = """
def add(a, b):
    \"\"\"Add two numbers and return the result.\"\"\"
    return a + b

def subtract(a, b):
    \"\"\"Subtract b from a and return the result.\"\"\"
    return a - b
"""
    file_path = tmp_path / "example.py"
    file_path.write_text(file_content)
    return file_path 