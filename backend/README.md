# AI CLI Assistant - Backend Service

This directory contains the FastAPI backend service for the AI-powered CLI assistant.

## Overview

The backend provides API endpoints that:
1. Handle AI model management and inference
2. Process requests from the CLI
3. Provide responses for all the assistant features

## Running the Backend

```bash
# From the project root
python -m backend.main

# Or from within the backend directory
python main.py
```

The server will run on http://localhost:8000 by default.

## API Documentation

After starting the server, you can access the auto-generated API documentation:
- OpenAPI UI: http://localhost:8000/docs
- ReDoc UI: http://localhost:8000/redoc

## API Endpoints

The backend is organized into several API groups:

### Status Endpoints
- `GET /` - Check API status
- `GET /health` - Health check endpoint

### Code Generation
- `POST /code/generate` - Generate code from description
  - Request: Description, language, temperature
  - Response: Generated code, language, model used
- `POST /code/explain` - Explain provided code
  - Request: Code snippet, language, detail level
  - Response: Explanation, detected language, model used
- `GET /code/languages` - List supported programming languages

### Terminal Commands
- `POST /terminal/suggest` - Suggest terminal commands
  - Request: Description of what to accomplish, platform
  - Response: List of command suggestions with explanations
- `POST /terminal/explain` - Explain terminal commands
  - Request: Command string, platform, detail level
  - Response: Explanation, command parts breakdown
- `GET /terminal/platforms` - List supported platforms

### Git Assistance
- `POST /git/commit-message` - Generate commit messages
  - Request: Git diff information, message type
  - Response: Generated commit message
- `POST /git/pr-description` - Generate PR descriptions
  - Request: Branch name, commit messages, diff summary
  - Response: PR title and description
- `GET /git/message-types` - List commit message types

### Documentation
- `POST /docs/search` - Search documentation
  - Request: Search query, language filter, max results
  - Response: Relevant documentation results with content snippets
- `POST /docs/summarize` - Summarize documentation
  - Request: Documentation content, summary length
  - Response: Generated summary
- `GET /docs/languages` - List supported documentation sources

### API Testing
- `POST /api-testing/request` - Make API requests
  - Request: URL, method, headers, data, params
  - Response: Status code, headers, response content, time
- `POST /api-testing/explain` - Explain API responses
  - Request: Original request and response
  - Response: Explanation of status code, headers, and content
- `GET /api-testing/methods` - List supported HTTP methods

## Directory Structure

```
backend/
├── api/            # API routes
│   ├── code.py     # Code generation endpoints
│   ├── terminal.py # Terminal command endpoints
│   ├── git.py      # Git assistance endpoints
│   ├── docs.py     # Documentation endpoints
│   └── api_testing.py # API testing endpoints
├── models/         # Data models
├── services/       # Business logic services
│   └── model_manager.py # AI model management
└── main.py         # Application entry point
```

## Model Management

The backend uses a `ModelManager` service to handle AI model loading and inference:

1. **Model Loading**: Models are loaded on-demand and cached for reuse
2. **Inference**: Standardized interface for generating text and embeddings
3. **Resource Management**: Handles model unloading to free memory when needed

Currently implemented models:
- **Code Generation**: Uses Hugging Face's CodeLlama-7b-Instruct
- **Text Generation**: Uses Mistral-7B-Instruct for various text generation tasks
- **Embeddings**: Uses all-MiniLM-L6-v2 for semantic search and similarity

## Implementation Details

### Error Handling

The backend implements comprehensive error handling:
- Global exception handler for unexpected errors
- Specific error handling for model loading failures
- Proper HTTP status codes for different error types

### Authentication

Authentication is currently not implemented but can be added using FastAPI's security utilities.

### Performance Optimization

- Models are loaded only when needed
- Quantization is used to reduce memory usage
- Prompt templates are optimized for specific tasks

## Development Guide

### Adding a New Endpoint

1. Define request/response models (in `shared/models/` or directly in the API file)
2. Create the endpoint in the appropriate API module
3. Implement the business logic and model integration
4. Document the endpoint with docstrings

### Modifying the Model Manager

1. Add new model configurations in `model_configs` dictionary
2. Implement specific handling for new model types if needed
3. Update the model interface methods as required

### Testing

1. Use the Swagger UI for quick endpoint testing
2. Check logs for errors and debugging information
3. Monitor model loading and memory usage 