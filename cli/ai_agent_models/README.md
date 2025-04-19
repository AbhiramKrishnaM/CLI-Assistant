# AI Agent Models

This directory contains the implementations of various AI models used in the CLI application.

## Overview

The structure is designed to allow easy addition of new models and model providers. Each model is implemented as a separate Python class that inherits from the `BaseAIModel` abstract base class, ensuring a consistent interface.

## Structure

- `base_model.py`: Abstract base class defining the interface for all models
- `model_factory.py`: Factory functions for creating and managing model instances
- `ollama_deepseek_r1_7b.py`: Implementation of DeepSeek-R1 7B model via Ollama
- `__init__.py`: Package initialization and model registry

## Adding a New Model

To add a new model, follow these steps:

1. Create a new file `<provider>_<model_name>.py` (e.g., `ollama_llama2_7b.py`)
2. Implement a class that inherits from `BaseAIModel`
3. Register the new model in `__init__.py` by adding it to the `MODEL_CLASSES` dictionary

Example of a minimal model implementation:

```python
from .base_model import BaseAIModel

class MyNewModel(BaseAIModel):
    @property
    def model_name(self) -> str:
        return "my-model-name"

    @classmethod
    def is_available(cls) -> bool:
        # Check if this model is available
        return True

    def generate_text(self, prompt, **kwargs):
        # Implement text generation
        pass

    def generate_code(self, description, language, **kwargs):
        # Implement code generation
        pass

    def generate_embeddings(self, texts):
        # Implement embedding generation
        pass
```

## Using Models

To use a model in your code:

```python
from cli.ai_agent_models.model_factory import get_model

# Get the default model
model = get_model()

# Generate text
result = model.generate_text("Hello, how are you?")

# Generate code
code_result = model.generate_code("a function to sort a list", "python")
```

## Supported Models

Currently supported models:

| Model Name | Provider | Description |
|------------|----------|-------------|
| deepseek-r1:7b | Ollama | DeepSeek 7B model via Ollama API |

## Configuration

Models can be configured in the application configuration file:

```
[ai]
default_model = "deepseek-r1:7b"

[ollama]
url = "http://localhost:11434/api"
timeout = 60
```
