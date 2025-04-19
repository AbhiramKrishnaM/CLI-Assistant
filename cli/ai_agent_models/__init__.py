"""AI agent models for the CLI application."""
from typing import Dict, Optional, Type

from .base_model import BaseAIModel
from .ollama_deepseek_r1_7b import OllamaDeepSeekModel

# Register all available model classes
MODEL_CLASSES: Dict[str, Type[BaseAIModel]] = {
    "deepseek-r1: 7b": OllamaDeepSeekModel,
}


def get_model_class(model_name: str) -> Optional[Type[BaseAIModel]]:
    """
    Get the appropriate model class based on the model name.

    Args:
        model_name: Name of the model to use

    Returns:
        A model class or None if not found
    """
    return MODEL_CLASSES.get(model_name)
