# Migration Guide: From Backend to Standalone Mode

This document explains the changes made to the AI CLI Assistant codebase to move from a client-server architecture with Hugging Face models to a standalone architecture with Ollama models.

## Overview of Changes

The main architectural change is removing the dependency on the backend FastAPI service for handling Ollama model inference. Instead, we've created a modular model framework that allows direct integration with Ollama and potentially other model providers.

### Key Changes

1. **New Model Framework**:
   - Created `cli/ai_agent_models/` directory with a pluggable architecture
   - Implemented `BaseAIModel` abstract class that all models inherit from
   - Created model implementations starting with `OllamaDeepSeekModel`
   - Added a factory system for loading models

2. **CLI Interface Updates**:
   - Changed all commands to use local models by default
   - Updated command-line options (`--local/--api` instead of `--local` flag)
   - Improved error handling and model availability checks

3. **Backend Changes**:
   - Backend is now optional, used only when `--api` flag is specified
   - Removed the dependency on the backend for Ollama model inference

## Using the New Architecture

### Default Behavior

By default, all commands now use local models:

```bash
# Generate code using local model (default)
aidev code generate "Create a Python function to calculate factorial"

# Select a specific model
aidev code generate --model llama2:7b "Create a Python function to calculate factorial"
```

### Using the Backend API

If you want to use the backend API (for example, if you have custom models deployed there), you can use the `--api` flag:

```bash
# Generate code using the backend API
aidev code generate --api "Create a Python function to calculate factorial"
```

## Adding New Models

The new architecture makes it easy to add new model implementations:

1. Create a new file in `cli/ai_agent_models/` for your model implementation
2. Implement the `BaseAIModel` abstract class
3. Register your model in `__init__.py`

For more details, see [cli/ai_agent_models/README.md](cli/ai_agent_models/README.md).

## Migration Checklist

If you're migrating an existing project or extension that used the old architecture:

1. Update imports to use the new model framework:
   ```python
   # Old
   from cli.utils.api import api_request, OLLAMA_AVAILABLE, get_available_local_models
   
   # New
   from cli.utils.api import api_request, get_available_local_models
   from cli.ai_agent_models.model_factory import get_model
   ```

2. Update command-line options:
   ```python
   # Old
   use_local: bool = typer.Option(False, "--local", "-l", help="Use local Ollama model instead of API backend")
   
   # New
   use_local: bool = typer.Option(True, "--local/--api", help="Use local AI model instead of API backend")
   ```

3. Replace OLLAMA_AVAILABLE checks:
   ```python
   # Old
   if use_local and not OLLAMA_AVAILABLE:
       print_warning("Ollama is not available. Falling back to API backend.")
       use_local = False
   
   # New
   if use_local:
       local_models = get_available_local_models()
       if not local_models:
           print_warning("No local models available. Falling back to API backend.")
           use_local = False
   ```

4. Update model references in API calls:
   ```python
   # Old
   local_model_name=model if use_local else None
   
   # New
   local_model_name=model
   ```

## Testing

The test suite has been updated to use the new model framework. If you're running tests that use models, you'll need to have Ollama installed and at least one model pulled.

To run the tests without model dependencies, use:

```bash
python tests/run_tests.py -k "not slow"
``` 