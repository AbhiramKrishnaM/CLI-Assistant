# Ollama Integration

The CLI tool uses Ollama models for all commands, providing a privacy-focused, offline AI experience.

## Setup

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model: `ollama pull deepseek-r1:7b` (recommended)
3. Ensure Ollama is running before using the CLI

## Using Ollama with CLI Commands

All commands use Ollama models by default:

```bash
# General format
aidev [command] [subcommand] [options] "your prompt"
```

### Supported Commands

All commands use Ollama models:

#### Terminal Commands
```bash
# Generate terminal command suggestions
aidev terminal suggest "find large files on my system"

# Explain a terminal command
aidev terminal explain "find / -type f -size +100M"
```

#### Code Commands
```bash
# Generate code
aidev code generate --language python "function to calculate fibonacci sequence"

# Explain code
aidev code explain path/to/file.py --line-range 10-20
```

#### Git Commands
```bash
# Generate commit message
aidev git generate-commit

# Generate PR description
aidev git pr-description
```

#### Documentation Commands
```bash
# Search documentation
aidev docs search "async functions in javascript"

# Summarize documentation
aidev docs summarize path/to/documentation.md --length medium
```

## Advanced Options

Each command supports these additional options:

### Model Selection

Specify which model to use:

```bash
aidev terminal suggest --model "llama2:7b" "find files modified in last 24 hours"
```

Available models depend on what you've downloaded with Ollama.

### Real-time Streaming

By default, all commands show results in real-time as they're generated:

```bash
# Disable streaming if preferred
aidev terminal suggest --no-stream "find large files"
```

### Model Thinking Process

Commands can show or hide the model's reasoning process:

```bash
# Show model thinking (default)
aidev terminal suggest --show-thinking "how to find large files on my system"

# Hide model thinking
aidev terminal suggest --no-thinking "how to find large files on my system"
```

When showing thinking is enabled, the model's thought process will be displayed in expandable panels.

## Checking Available Models

You can check what models you have locally:

```
aidev terminal models
```

This command will show available models and the current default model.

## Configuration

You can configure Ollama settings in the configuration file. Default values:

```
[ai]
default_model = "deepseek-r1:7b"

[ollama]
url = "http://localhost:11434/api"
timeout = 60
```

## Troubleshooting

If you're having issues with Ollama:

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

5. Test a simple generation:
   ```
   ollama run deepseek-r1:7b "Hello, how are you?"
   ```
