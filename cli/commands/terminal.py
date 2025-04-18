"""Terminal command suggestions and explanations."""
import typer
import sys
from typing import List, Optional
from rich import print
from rich.console import Console
from rich.panel import Panel
from cli.utils.api import api_request, OLLAMA_AVAILABLE, get_available_local_models
from cli.utils.formatting import print_error, print_success, print_info, print_warning

app = typer.Typer(help="Get help with terminal commands")
console = Console()

@app.command()
def suggest(
    description: str = typer.Argument(..., help="What you want to accomplish"),
    platform: str = typer.Option("auto", help="Platform (linux, mac, windows, or auto)"),
    use_local: bool = typer.Option(False, "--local", "-l", help="Use local Ollama model instead of API backend"),
    model: str = typer.Option("deepseek-r1:7b", "--model", "-m", help="Specify which local model to use (requires --local)"),
    no_stream: bool = typer.Option(False, "--no-stream", help="Disable streaming for local models"),
    show_thinking: bool = typer.Option(True, "--show-thinking/--no-thinking", help="Show or hide model's thinking process")
):
    """Suggest terminal commands based on a description."""
    if platform == "auto":
        import platform as plt
        system = plt.system().lower()
        if "darwin" in system:
            platform = "mac"
        elif "linux" in system:
            platform = "linux"
        elif "windows" in system:
            platform = "windows"
        else:
            platform = "linux"  # Default to Linux
    
    print(f"Suggesting commands for '{description}' on {platform}:")
    
    if use_local and not OLLAMA_AVAILABLE:
        print_warning("Ollama is not available. Falling back to API backend.")
        use_local = False
        
    if use_local:
        local_models = get_available_local_models()
        if not local_models:
            print_warning("No local models found in Ollama. Falling back to API backend.")
            use_local = False
        elif model not in local_models:
            print_warning(f"Model '{model}' not found in Ollama. Available models: {', '.join(local_models)}")
            if "deepseek-r1:7b" in local_models:
                model = "deepseek-r1:7b"
                print_info(f"Using deepseek-r1:7b instead.")
            else:
                model = local_models[0]
                print_info(f"Using {model} instead.")
    
    # Request command suggestions from the API
    response = api_request(
        endpoint="/text/generate",
        method="POST",
        data={
            "prompt": f"Suggest terminal commands for: {description}\nPlatform: {platform}",
            "temperature": 0.3,
            "max_length": 512,
            "stream": not no_stream,
            "show_thinking": show_thinking
        },
        loading_message=f"Finding terminal commands for {platform}...",
        use_local_model=use_local,
        local_model_name=model if use_local else None
    )
    
    if "error" in response:
        print_error("Failed to get command suggestions.")
        # Fallback to mock suggestions
        if "list" in description.lower() and "files" in description.lower():
            print("\nCommand: ls -la" if platform != "windows" else "\nCommand: dir /a")
            print("This command lists all files including hidden ones in detailed format.")
        elif "search" in description.lower():
            print("\nCommand: grep -r 'search_term' ." if platform != "windows" else 
                 "\nCommand: findstr /s /i 'search_term' *.*")
            print("This command recursively searches for a term in the current directory.")
        else:
            print("\nI need more specific information to suggest a command. Try describing what you want to do with files, directories, or system resources.")
    else:
        # For streaming mode, the text is already printed in real-time
        # We only need to print a closing line
        if use_local and not no_stream:
            # Already displayed in real-time
            print("\n")  # Add extra newline for separation
            print_success(f"Generation completed with {response.get('model_used', model)}.")
            
            # If non-streaming mode and there are thinking sections
            if no_stream and "thinking" in response and response["thinking"] and show_thinking:
                print_info("Model reasoning (click to expand):")
                for i, thinking in enumerate(response["thinking"], 1):
                    panel = Panel(
                        thinking.strip(),
                        title=f"[bold]Thinking Process #{i}[/bold]",
                        subtitle="[dim][click to collapse][/dim]",
                        border_style="blue"
                    )
                    print(panel)
        else:
            # Display the AI-generated suggestions for non-streaming mode
            suggestions = response.get("text", "No suggestions generated")
            model_info = f" (using {response.get('model_used', 'unknown model')})" if use_local else ""
            print(f"\n[bold green]Suggested Commands{model_info}:[/bold green]")
            print(suggestions)
            
            # Display thinking sections for non-streaming mode if available
            if "thinking" in response and response["thinking"] and show_thinking:
                print_info("Model reasoning (click to expand):")
                for i, thinking in enumerate(response["thinking"], 1):
                    panel = Panel(
                        thinking.strip(),
                        title=f"[bold]Thinking Process #{i}[/bold]",
                        subtitle="[dim][click to collapse][/dim]",
                        border_style="blue"
                    )
                    print(panel)

@app.command()
def explain(
    command: List[str] = typer.Argument(..., help="Command to explain"),
    use_local: bool = typer.Option(False, "--local", "-l", help="Use local Ollama model instead of API backend"),
    model: str = typer.Option("deepseek-r1:7b", "--model", "-m", help="Specify which local model to use (requires --local)"),
    no_stream: bool = typer.Option(False, "--no-stream", help="Disable streaming for local models"),
    show_thinking: bool = typer.Option(True, "--show-thinking/--no-thinking", help="Show or hide model's thinking process")
):
    """Explain what a terminal command does."""
    full_command = " ".join(command)
    print(f"Explaining command: [bold]{full_command}[/bold]")
    
    if use_local and not OLLAMA_AVAILABLE:
        print_warning("Ollama is not available. Falling back to API backend.")
        use_local = False
        
    if use_local:
        local_models = get_available_local_models()
        if not local_models:
            print_warning("No local models found in Ollama. Falling back to API backend.")
            use_local = False
        elif model not in local_models:
            print_warning(f"Model '{model}' not found in Ollama. Available models: {', '.join(local_models)}")
            if "deepseek-r1:7b" in local_models:
                model = "deepseek-r1:7b"
                print_info(f"Using deepseek-r1:7b instead.")
            else:
                model = local_models[0]
                print_info(f"Using {model} instead.")
    
    # Request command explanation from the API
    response = api_request(
        endpoint="/text/generate",
        method="POST",
        data={
            "prompt": f"Explain the following terminal command in detail: {full_command}",
            "temperature": 0.3,
            "max_length": 512,
            "stream": not no_stream,
            "show_thinking": show_thinking
        },
        loading_message=f"Analyzing command...",
        use_local_model=use_local,
        local_model_name=model if use_local else None
    )
    
    if "error" in response:
        print_error("Failed to get command explanation.")
        # Fallback to mock explanations
        if full_command.startswith("ls"):
            print("\nThe 'ls' command lists files and directories.")
            if "-la" in full_command:
                print("The '-l' flag shows detailed information in long format.")
                print("The '-a' flag shows hidden files (those starting with '.').")
        elif full_command.startswith("grep"):
            print("\nThe 'grep' command searches for patterns in files.")
            if "-r" in full_command:
                print("The '-r' flag makes the search recursive through directories.")
        elif full_command.startswith("git"):
            print("\nThis is a git command for version control.")
            if "commit" in full_command:
                print("The 'commit' subcommand records changes to the repository.")
        else:
            print("\nThis command would be explained by the AI model. Currently using mock explanations for demonstration.")
    else:
        # For streaming mode, the text is already printed in real-time
        if use_local and not no_stream:
            # Already displayed in real-time
            print("\n")  # Add extra newline for separation
            print_success(f"Generation completed with {response.get('model_used', model)}.")
            
            # If non-streaming mode and there are thinking sections
            if no_stream and "thinking" in response and response["thinking"] and show_thinking:
                print_info("Model reasoning (click to expand):")
                for i, thinking in enumerate(response["thinking"], 1):
                    panel = Panel(
                        thinking.strip(),
                        title=f"[bold]Thinking Process #{i}[/bold]",
                        subtitle="[dim][click to collapse][/dim]",
                        border_style="blue"
                    )
                    print(panel)
        else:
            # Display the AI-generated explanation for non-streaming mode
            explanation = response.get("text", "No explanation generated")
            model_info = f" (using {response.get('model_used', 'unknown model')})" if use_local else ""
            print(f"\n[bold green]Explanation{model_info}:[/bold green]")
            print(explanation)
            
            # Display thinking sections for non-streaming mode if available
            if "thinking" in response and response["thinking"] and show_thinking:
                print_info("Model reasoning (click to expand):")
                for i, thinking in enumerate(response["thinking"], 1):
                    panel = Panel(
                        thinking.strip(),
                        title=f"[bold]Thinking Process #{i}[/bold]",
                        subtitle="[dim][click to collapse][/dim]",
                        border_style="blue"
                    )
                    print(panel)

@app.command()
def models():
    """List available local models from Ollama."""
    if not OLLAMA_AVAILABLE:
        print_error("Ollama is not available. Make sure it's installed and running.")
        return
    
    models = get_available_local_models()
    if not models:
        print_warning("No local models found. You may need to pull models first.")
        print("\nTo pull the Deepseek model, run: [bold]ollama pull deepseek-r1:7b[/bold]")
        return
    
    print("[bold green]Available local models:[/bold green]")
    for model in models:
        print(f"- {model}")
    
    print("\n[bold blue]To use a local model:[/bold blue]")
    print("terminal suggest --local \"list all files\" ")
    print("terminal explain --local --model deepseek-r1:7b \"ls -la\"")
    print("\n[bold blue]To disable streaming:[/bold blue]")
    print("terminal suggest --local --no-stream \"list all files\"")
    print("terminal explain --local --no-stream \"ls -la\"")
    print("\n[bold blue]To hide thinking sections:[/bold blue]")
    print("terminal suggest --local --no-thinking \"list all files\"")
    print("terminal explain --local --no-thinking \"ls -la\"") 