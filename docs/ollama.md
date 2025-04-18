# Using Local Models with Ollama

This CLI tool supports using local LLM models via [Ollama](https://ollama.ai/), providing a way to run AI commands without requiring internet access or sending data to external APIs.

## Prerequisites

1. Install Ollama by following the instructions at https://github.com/ollama/ollama
2. Pull the deepseek-r1:7b model (or any other model you want to use):
   ```
   ollama pull deepseek-r1:7b
   ```
3. Make sure Ollama is running (it should be running as a service in the background)

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

## Using Ollama with CLI Commands

Most text generation commands support using local models via the `--local` flag:

```
aidev terminal suggest --local "how to find large files on my system"
```

You can also specify which model to use:

```
aidev terminal explain --local --model deepseek-r1:7b "grep -r 'pattern' ."
```

### Real-time Streaming

By default, the CLI shows text generation results in real-time as they come from Ollama, just like ChatGPT's streaming interface. If you prefer to wait for the full response before seeing it (like in the original implementation), you can use the `--no-stream` flag:

```
aidev terminal suggest --local --no-stream "how to find large files on my system"
```

This is useful when you want to pipe the output to another command or when you're running scripts.

### Model Thinking Process

If your model output includes sections enclosed in `<think>...</think>` tags, the CLI will treat these as the model's internal reasoning process and display them as collapsible sections. This gives you insight into how the model arrived at its answers.

You can control this behavior with the `--show-thinking/--no-thinking` flags:

```
# Hide model reasoning process
aidev terminal suggest --local --no-thinking "how to find large files on my system"

# Show model reasoning (default)
aidev terminal suggest --local --show-thinking "how to find large files on my system"
```

When `--show-thinking` is enabled:
1. The model's thoughts are displayed in expandable/collapsible panels
2. During streaming, a thinking indicator shows when the model is reasoning
3. The raw thinking process is not included in the actual command suggestions or explanations

### Supported Commands

The following commands support using local Ollama models:

- `terminal suggest`: Generate terminal command suggestions
- `terminal explain`: Explain terminal commands
- `api request`: Make API requests with local model option

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

## Performance Considerations

- Local models may be slower than cloud-based APIs depending on your hardware
- For better performance, use smaller models if available
- First generation after starting Ollama may take longer as the model is loaded into memory 