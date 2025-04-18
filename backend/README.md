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
- `POST /code/explain` - Explain provided code
- `GET /code/languages` - List supported programming languages

### Terminal Commands
- `POST /terminal/suggest` - Suggest terminal commands
- `POST /terminal/explain` - Explain terminal commands
- `GET /terminal/platforms` - List supported platforms

### Git Assistance
- `POST /git/commit-message` - Generate commit messages
- `POST /git/pr-description` - Generate PR descriptions
- `GET /git/message-types` - List commit message types

### Documentation
- `POST /docs/search` - Search documentation
- `POST /docs/summarize` - Summarize documentation
- `GET /docs/languages` - List supported documentation sources

### API Testing
- `POST /api-testing/request` - Make API requests
- `POST /api-testing/explain` - Explain API responses
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

## Development

### Adding New Endpoints

1. Create models in `models/` directory
2. Implement service logic in `services/` directory
3. Create the endpoint in the appropriate module in `api/` directory
4. Register the endpoint in `main.py` if needed

### Model Management

The application uses a `ModelManager` service to:
1. Load and cache models as needed
2. Manage model resources
3. Provide a consistent interface for model inference 