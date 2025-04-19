"""Base class for AI model implementations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseAIModel(ABC):
    """Base class for all AI models used in the CLI."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """The name of the model."""
        pass

    @classmethod
    @abstractmethod
    def is_available(cls) -> bool:
        """Check if the model is available to use."""
        pass

    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_length: Optional[int] = None,
        system_prompt: Optional[str] = None,
        stream: bool = True,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Generate text based on a prompt.

        Args:
            prompt: The prompt to generate text from
            temperature: Controls randomness (0.0-1.0)
            max_length: Maximum number of tokens to generate
            system_prompt: Optional system prompt to set context
            stream: Whether to stream the response in real-time
            **kwargs: Additional model-specific parameters

        Returns:
            Dictionary with generated text and metadata
        """
        pass

    @abstractmethod
    def generate_code(
        self,
        description: str,
        language: str,
        temperature: float = 0.7,
        max_length: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Generate code based on a description.

        Args:
            description: Description of what the code should do
            language: The programming language to generate
            temperature: Controls randomness (0.0-1.0)
            max_length: Maximum number of tokens to generate
            **kwargs: Additional model-specific parameters

        Returns:
            Dictionary with generated code and metadata
        """
        pass

    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of texts to generate embeddings for

        Returns:
            List of embedding vectors
        """
        pass
