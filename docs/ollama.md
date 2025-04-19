# Ollama Integration Guide

This guide explains how to set up and use Ollama models with AIDEV.

## What is Ollama?

[Ollama](https://ollama.ai) is an open-source tool that allows you to run large language models (LLMs) locally on your machine. It provides a simple API for running models like DeepSeek, Llama, and Mistral without requiring a cloud service.

## Setup

### 1. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai).

**Mac**:
```bash
brew install ollama
```

**Linux**:
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows**:
Download the installer from the [Ollama website](https://ollama.ai).

### 2. Start Ollama

Once installed, start the Ollama service:

```bash
ollama serve
```

This runs Ollama in the background and exposes its API on port 11434.

### 3. Pull a Model

Pull at least one model to use with AIDEV:

```bash
# Recommended model
ollama pull deepseek-r1:7b

# Alternative models
ollama pull llama2:7b
ollama pull mistral:7b
```

The first pull operation will download the model files, which may take some time depending on your internet connection and the model size.

## Using Ollama with AIDEV

### Basic Usage

All AIDEV commands automatically use Ollama models:

```bash
# Generate code
aidev code generate "Create a function to calculate prime numbers in Python"

# Get terminal command suggestions
aidev terminal suggest "find all PDF files modified in the last week"

# Generate a git commit message
aidev git generate-commit
```

### Model Selection

Specify a particular model with the `--model` flag:

```bash
# Use a specific model
aidev code generate --model "mistral:7b" "Write a recursive function to calculate factorial"

# Use the default model
aidev terminal suggest "find large files on my system"
```

### Streaming Options

Control the streaming behavior:

```bash
# Enable streaming (default) - shows results as they're generated
aidev docs search "javascript promises"

# Disable streaming - shows complete response when finished
aidev docs search --no-stream "javascript promises"
```

### Thinking Process

View or hide the model's reasoning:

```bash
# Show thinking (default) - displays reasoning in collapsible panels
aidev git generate-commit --show-thinking

# Hide thinking - only shows the final output
aidev git generate-commit --no-thinking
```

## Command Reference

### Code Commands

```bash
# Generate code with a specific language
aidev code generate "Sort an array of integers" --language javascript

# Explain existing code
aidev code explain path/to/code.py --lines 10-20
```

### Terminal Commands

```bash
# Get command suggestions
aidev terminal suggest "compress a directory into a tar.gz file"

# Explain a command
aidev terminal explain "find . -type f -name '*.log' -mtime +30 -delete"
```

### Git Commands

```bash
# Generate a commit message based on changes
aidev git generate-commit

# Create a PR description from commits
aidev git pr-description
```

### Documentation Commands

```bash
# Search for documentation
aidev docs search "async functions" --language javascript --max 10

# Summarize a document
aidev docs summarize README.md --length medium
```

### API Commands

```bash
# Check available models
aidev api ollama-models

# Configure Ollama settings
aidev api config --set-ollama-model "deepseek-r1:7b"
aidev api config --set-ollama-url "http://localhost:11434/api"
aidev api config --set-ollama-timeout 120
```

## Configuration

AIDEV uses these default Ollama settings:

```
[ai]
default_model = "deepseek-r1:7b"

[ollama]
url = "http://localhost:11434/api"
timeout = 60  # seconds
enabled = true
```

You can modify these settings using the `api config` command:

```bash
# Show current configuration
aidev api config

# Set a different default model
aidev api config --set-ollama-model "mistral:7b"

# Change Ollama API URL (if running on a different machine)
aidev api config --set-ollama-url "http://192.168.1.100:11434/api"
```

## Troubleshooting

### Common Issues

#### "Model not found" error

```
Model 'deepseek-r1:7b' not found
```

**Solution**: Pull the model with Ollama:
```bash
ollama pull deepseek-r1:7b
```

#### "Connection refused" error

```
Failed to connect to Ollama: Connection refused
```

**Solutions**:
1. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

2. Check if the Ollama API is accessible:
   ```bash
   curl http://localhost:11434/api/tags
   ```

3. Verify your firewall isn't blocking connections to port 11434

#### Slow response times

**Solutions**:
1. Use a smaller model (e.g., deepseek-r1:7b instead of llama2:70b)
2. Increase the timeout:
   ```bash
   aidev api config --set-ollama-timeout 180
   ```

### Diagnostic Commands

```bash
# Check if Ollama is running and available
aidev api config

# List available models
aidev api ollama-models

# Check Ollama directly
ollama list
```

### Resetting Ollama

If you're having persistent issues with Ollama:

```bash
# Stop the Ollama service
killall ollama

# Start Ollama again
ollama serve
```

## Additional Resources

- [Ollama GitHub Repository](https://github.com/ollama/ollama)
- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/README.md)
- [DeepSeek Model Information](https://ollama.ai/library/deepseek-r1)
- [AIDEV Development Guide](development.md)
