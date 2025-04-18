"""Utilities for interacting with Ollama models."""
import requests
import json
import sys
import time
import re
from typing import Dict, Any, Optional, List, Callable
from .formatting import print_error, print_info, print_warning, print_success, loading_spinner
from .config import get_config_value
from rich.console import Console
from rich.panel import Panel
from rich import print as rich_print

console = Console()

# Get Ollama API URL from config
def get_ollama_url() -> str:
    """Get the Ollama API URL from configuration."""
    return get_config_value("ollama.url", "http://localhost:11434/api")

def get_ollama_timeout() -> int:
    """Get the Ollama API timeout from configuration."""
    return get_config_value("ollama.timeout", 60)

def get_default_model() -> str:
    """Get the default Ollama model from configuration."""
    return get_config_value("ollama.default_model", "deepseek-r1:7b")

def get_available_models() -> List[str]:
    """
    Get a list of available models from Ollama.
    
    Returns:
        List of model names available in Ollama
    """
    try:
        response = requests.get(f"{get_ollama_url()}/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [model["name"] for model in data["models"]]
        else:
            print_error(f"Failed to fetch models from Ollama: {response.status_code}")
            return []
    except Exception as e:
        print_error(f"Error connecting to Ollama: {str(e)}")
        return []

def generate_text_with_ollama(
    prompt: str, 
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_length: Optional[int] = None,
    system_prompt: Optional[str] = None,
    stream: bool = True
) -> Dict[str, Any]:
    """
    Generate text using a local Ollama model.
    
    Args:
        prompt: The prompt to send to the model
        model: The Ollama model to use (e.g., "deepseek-r1:7b")
        temperature: Controls randomness (0.0-1.0)
        max_length: Maximum number of tokens to generate
        system_prompt: Optional system prompt to set context
        stream: Whether to stream the response in real-time
        
    Returns:
        Dictionary with generated text and metadata
    """
    # Use default model if none specified
    if model is None:
        model = get_default_model()
        
    headers = {"Content-Type": "application/json"}
    timeout = get_ollama_timeout()
    
    # Prepare request data
    data = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "stream": stream
    }
    
    # Add optional parameters if provided
    if max_length is not None:
        data["max_tokens"] = max_length
    
    if system_prompt is not None:
        data["system"] = system_prompt
    
    try:
        if not stream:
            # Non-streaming mode (wait for full response)
            with loading_spinner(f"Generating text with {model}...", spinner_style="moon"):
                response = requests.post(
                    f"{get_ollama_url()}/generate", 
                    headers=headers,
                    json=data,
                    timeout=timeout
                )
            
            if response.status_code == 200:
                result = response.json()
                text = result.get("response", "")
                
                # Handle think tags in non-streaming mode
                text = process_think_tags(text)
                
                return {
                    "text": text,
                    "prompt": prompt,
                    "model_used": model,
                    "completion_tokens": result.get("eval_count", 0),
                    "total_duration": result.get("total_duration", 0)
                }
            else:
                error_message = f"Ollama API error: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_message += f" - {error_detail.get('error', '')}"
                except:
                    pass
                
                print_error(error_message)
                return {"error": True, "message": error_message}
        else:
            # Streaming mode (show output in real-time)
            print(f"\nGenerating with {model}:")
            
            # Open a streaming connection
            response = requests.post(
                f"{get_ollama_url()}/generate", 
                headers=headers,
                json=data,
                stream=True,
                timeout=timeout
            )
            
            # Variables to collect the full response and stats
            full_response = ""
            thinking_content = ""
            in_thinking_section = False
            eval_count = 0
            start_time = time.time()
            
            # Process the stream
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        # Parse the JSON chunk
                        try:
                            chunk = json.loads(line.decode('utf-8'))
                            
                            # Extract and display the text piece
                            if "response" in chunk:
                                text_piece = chunk["response"]
                                full_response += text_piece
                                
                                # Check for <think> tags
                                if "<think>" in text_piece and not in_thinking_section:
                                    in_thinking_section = True
                                    # Add collapsible thinking indicator
                                    rich_print("[bold blue]🧠 [Thinking...] [click to expand][/bold blue]")
                                    continue
                                
                                if in_thinking_section:
                                    # Collect thinking content but don't display it
                                    thinking_content += text_piece
                                    
                                    # Check if thinking section is ending
                                    if "</think>" in text_piece:
                                        in_thinking_section = False
                                        # Store full thinking content for later use
                                        full_response = full_response.replace(f"<think>{thinking_content}", "")
                                        rich_print("[bold green]✓ [Thinking completed][/bold green]")
                                else:
                                    # Normal text output
                                    sys.stdout.write(text_piece)
                                    sys.stdout.flush()
                            
                            # Keep track of token count
                            if "eval_count" in chunk:
                                eval_count = chunk["eval_count"]
                            
                            # Check if done
                            if chunk.get("done", False):
                                break
                                
                        except json.JSONDecodeError:
                            continue
                
                # Collect and display thinking sections at the end
                thinking_sections = extract_thinking_sections(full_response)
                clean_response = remove_thinking_sections(full_response)
                
                if thinking_sections:
                    sys.stdout.write("\n\n")
                    sys.stdout.flush()
                    print_info("Model reasoning (click to expand):")
                    for i, thinking in enumerate(thinking_sections, 1):
                        panel = Panel(
                            thinking.strip(),
                            title=f"[bold]Thinking Process #{i}[/bold]",
                            subtitle="[dim][click to collapse][/dim]",
                            border_style="blue"
                        )
                        rich_print(panel)
                
                # Return the collected response and metadata
                total_duration = time.time() - start_time
                return {
                    "text": clean_response,
                    "prompt": prompt,
                    "model_used": model,
                    "completion_tokens": eval_count,
                    "total_duration": total_duration,
                    "thinking": thinking_sections
                }
            else:
                error_message = f"Ollama API error: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_message += f" - {error_detail.get('error', '')}"
                except:
                    pass
                
                print_error(error_message)
                return {"error": True, "message": error_message}
    
    except Exception as e:
        error_message = f"Error communicating with Ollama: {str(e)}"
        print_error(error_message)
        return {"error": True, "message": error_message}

def extract_thinking_sections(text: str) -> List[str]:
    """Extract all thinking sections from the text."""
    pattern = r"<think>(.*?)</think>"
    return re.findall(pattern, text, re.DOTALL)

def remove_thinking_sections(text: str) -> str:
    """Remove all thinking sections from the text."""
    pattern = r"<think>.*?</think>"
    return re.sub(pattern, "", text, flags=re.DOTALL)

def process_think_tags(text: str) -> str:
    """Process think tags in non-streaming mode."""
    # Extract thinking sections
    thinking_sections = extract_thinking_sections(text)
    
    # Remove thinking sections from the text
    clean_text = remove_thinking_sections(text)
    
    # Return the processed text
    return clean_text

def check_ollama_availability() -> bool:
    """Check if Ollama is available."""
    try:
        response = requests.get(f"{get_ollama_url()}/tags", timeout=2)
        return response.status_code == 200
    except:
        return False 