# Ollama Integration

The CLI tool now supports using local Ollama models for all commands, providing a privacy-focused, offline alternative to API-based AI.

## Setup

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model: `ollama pull deepseek-r1:7b` (recommended)
3. Ensure Ollama is running before using the CLI with local models

## Using Ollama with CLI Commands

All major commands now support local Ollama models. Use the `--local` flag to activate:

```bash
# General format
aidev [command] [subcommand] --local [options] "your prompt"
```

### Supported Commands

The following commands all support Ollama integration:

#### Terminal Commands
```bash
# Generate terminal command suggestions
aidev terminal suggest --local "find large files on my system"

# Explain a terminal command
aidev terminal explain --local "find / -type f -size +100M"
```

#### Code Commands
```bash
# Generate code
aidev code generate --local --language python "function to calculate fibonacci sequence"

# Explain code
aidev code explain --local path/to/file.py --line-range 10-20
```

#### Git Commands
```bash
# Generate commit message
aidev git generate-commit --local

# Generate PR description
aidev git pr-description --local
```

#### Documentation Commands
```bash
# Search documentation
aidev docs search --local "async functions in javascript"

# Summarize documentation
aidev docs summarize --local path/to/documentation.md --length medium
```

## Advanced Options

Each command supports these additional options when using Ollama:

### Model Selection

Specify which local model to use:

```bash
aidev terminal suggest --local --model "deepseek-r1:7b" "find files modified in last 24 hours"
```

Available models depend on what you've downloaded with Ollama.

### Real-time Streaming

By default, all commands show results in real-time as they're generated:

```bash
# Disable streaming if preferred
aidev terminal suggest --local --no-stream "find large files"
```

### Model Thinking Process

Commands can show or hide the model's reasoning process:

```bash
# Show model thinking (default)
aidev terminal suggest --local --show-thinking "how to find large files on my system"

# Hide model thinking
aidev terminal suggest --local --no-thinking "how to find large files on my system"
```

When `--show-thinking` is enabled, the model's thought process will be displayed in expandable panels.

## Fallback Behavior

If Ollama is not available or a requested model isn't found, commands will automatically fall back to:
1. Another available local model (if any)
2. The standard API backend

Error messages will inform you when fallbacks occur.

## Performance Considerations

- Local models run on your hardware, so performance depends on your system specifications
- First-time queries may take longer as models load into memory
- Using smaller models improves response speed at the cost of some capability

## Checking Ollama Status

You can check if Ollama is available and see what models you have locally:

```
aidev api ollama-models
```

or

```
aidev terminal models
```

Both commands will show available models and the current default model.

## Configuration

You can configure Ollama settings using:

```
aidev api config
```

This shows the current configuration and status of Ollama integration.

### Changing Configuration

To modify settings:

```
# Change the default model
aidev api config --set-ollama-model "llama3:8b"

# Change the Ollama API URL (if running on a different machine)
aidev api config --set-ollama-url "http://192.168.1.100:11434/api"

# Increase the timeout for larger models
aidev api config --set-ollama-timeout 120

# Disable Ollama integration
aidev api config --ollama-enabled false
```

## Troubleshooting

If you're having issues with Ollama integration:

1. Ensure Ollama is installed and running:
   ```
   ollama list
   ```

2. Check if the model is available:
   ```
   ollama list
   ```

3. Pull the model if it's not available:
   ```
   ollama pull deepseek-r1:7b
   ```

4. Verify the Ollama API is accessible:
   ```
   curl http://localhost:11434/api/tags
   ```

5. Check the CLI configuration:
   ```
   aidev api config
   ```

6. Test a simple generation:
   ```
   ollama run deepseek-r1:7b "Hello, how are you?"
   ``` 