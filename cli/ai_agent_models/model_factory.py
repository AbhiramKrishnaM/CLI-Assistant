"""Factory for creating AI model instances."""

from typing import Any, Dict, Optional, cast

from ..utils.config import get_config_value
from . import MODEL_CLASSES, get_model_class
from .base_model import BaseAIModel


def get_default_model_name() -> str:
    """Get the default model name from configuration."""
    result = get_config_value("ai.default_model", "deepseek-r1:7b")
    return cast(str, result)  # Cast to str to satisfy mypy


_model_instances: Dict[str, BaseAIModel] = {}


def get_model(model_name: Optional[str] = None) -> Optional[BaseAIModel]:
    """
    Get a model instance based on name.

    Args:
        model_name: Name of the model to use (or None for default)

    Returns:
        A model instance or None if not available
    """
    # Use default model if none specified
    if model_name is None:
        model_name = get_default_model_name()

    # Return cached instance if available
    if model_name in _model_instances:
        return _model_instances[model_name]

    # Get the appropriate model class
    model_class = get_model_class(model_name)
    if model_class is None:
        return None

    # Check if the model is available
    if not model_class.is_available():
        return None

    # Create a new instance
    model = model_class()
    _model_instances[model_name] = model

    return model


def get_available_models() -> Dict[str, Any]:
    """
    Get information about available models.

    Returns:
        Dictionary with model information
    """
    available_models = {}

    for model_name, model_class in MODEL_CLASSES.items():
        available_models[model_name] = {
            "name": model_name,
            "available": model_class.is_available(),
            "type": model_class.__name__,
        }

    return available_models
