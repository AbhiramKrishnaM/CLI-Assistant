"""Ollama DeepSeek-R1 7B model implementation."""
import json
import re
import sys
import time
from typing import Any, Dict, List, Optional

import requests
from rich import print as rich_print
from rich.console import Console
from rich.panel import Panel

from ..utils.config import get_config_value
from ..utils.formatting import loading_spinner, print_error, print_info
from .base_model import BaseAIModel

console = Console()


class OllamaDeepSeekModel(BaseAIModel):
    """Implementation of the DeepSeek-R1 7B model via Ollama."""

    @property
    def model_name(self) -> str:
        """The name of the model."""
        return "deepseek-r1: 7b"

    @classmethod
    def get_ollama_url(cls) -> str:
        """Get the Ollama API URL from configuration."""
        result = get_config_value("ollama.url", "http: //localhost: 11434/api")
        return str(result)

    @classmethod
    def get_ollama_timeout(cls) -> int:
        """Get the Ollama API timeout from configuration."""
        result = get_config_value("ollama.timeout", 60)
        return int(result)

    @classmethod
    def is_available(cls) -> bool:
        """Check if Ollama is available and the model is installed."""
        try:
            response = requests.get(f"{cls.get_ollama_url()}/tags", timeout=2)
            if response.status_code == 200:
                data = response.json()
                available_models = [model["name"] for model in data.get("models", [])]
                return "deepseek-r1: 7b" in available_models
            return False
        except Exception:
            return False

    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_length: Optional[int] = None,
        system_prompt: Optional[str] = None,
        stream: bool = True,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Generate text using Ollama DeepSeek model.

        Args:
            prompt: The prompt to send to the model
            temperature: Controls randomness (0.0-1.0)
            max_length: Maximum number of tokens to generate
            system_prompt: Optional system prompt to set context
            stream: Whether to stream the response in real-time

        Returns:
            Dictionary with generated text and metadata
        """
        headers = {"Content-Type": "application/json"}
        timeout = self.get_ollama_timeout()

        # Prepare request data
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": temperature,
            "stream": stream,
        }

        # Add optional parameters if provided
        if max_length is not None:
            data["max_tokens"] = max_length

        if system_prompt is not None:
            data["system"] = system_prompt

        try:
            if not stream:
                # Non-streaming mode (wait for full response)
                with loading_spinner(
                    f"Generating text with {self.model_name}...", spinner_style="moon"
                ):
                    response = requests.post(
                        f"{self.get_ollama_url()}/generate",
                        headers=headers,
                        json=data,
                        timeout=timeout,
                    )

                if response.status_code == 200:
                    result = response.json()
                    text = result.get("response", "")

                    # Handle think tags in non-streaming mode
                    text = self._process_think_tags(text)

                    return {
                        "text": text,
                        "prompt": prompt,
                        "model_used": self.model_name,
                        "completion_tokens": result.get("eval_count", 0),
                        "total_duration": result.get("total_duration", 0),
                    }
                else:
                    error_message = f"Ollama API error: {response.status_code}"
                    try:
                        error_detail = response.json()
                        error_message += f" - {error_detail.get('error', '')}"
                    except Exception:
                        pass

                    print_error(error_message)
                    return {"error": True, "message": error_message}
            else:
                # Streaming mode (show output in real-time)
                print(f"\nGenerating with {self.model_name}: ")

                # Open a streaming connection
                response = requests.post(
                    f"{self.get_ollama_url()}/generate",
                    headers=headers,
                    json=data,
                    stream=True,
                    timeout=timeout,
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
                                chunk = json.loads(line.decode("utf-8"))

                                # Extract and display the text piece
                                if "response" in chunk:
                                    text_piece = chunk["response"]
                                    full_response += text_piece

                                    # Check for <think> tags
                                    if (
                                        "<think>" in text_piece
                                        and not in_thinking_section
                                    ):
                                        in_thinking_section = True
                                        # Add collapsible thinking indicator
                                        rich_print(
                                            "[bold blue]🧠 [Thinking...] "
                                            "[click to expand][/bold blue]"
                                        )
                                        continue

                                    if in_thinking_section:
                                        # Collect thinking content but don't display it
                                        thinking_content += text_piece

                                        # Check if thinking section is ending
                                        if "</think>" in text_piece:
                                            in_thinking_section = False
                                            # Store full thinking content for later use
                                            full_response = full_response.replace(
                                                f"<think>{thinking_content}", ""
                                            )
                                            rich_print(
                                                "[bold green]✓ [Thinking completed]"
                                                "[/bold green]"
                                            )
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
                    thinking_sections = self._extract_thinking_sections(full_response)
                    clean_response = self._remove_thinking_sections(full_response)

                    if thinking_sections:
                        sys.stdout.write("\n\n")
                        sys.stdout.flush()
                        print_info("Model reasoning (click to expand):")
                        for i, thinking in enumerate(thinking_sections, 1):
                            panel = Panel(
                                thinking.strip(),
                                title=f"[bold]Thinking Process #{i}[/bold]",
                                subtitle="[dim][click to collapse][/dim]",
                                border_style="blue",
                            )
                            rich_print(panel)

                    # Return the collected response and metadata
                    total_duration = time.time() - start_time
                    return {
                        "text": clean_response,
                        "prompt": prompt,
                        "model_used": self.model_name,
                        "completion_tokens": eval_count,
                        "total_duration": total_duration,
                        "thinking": thinking_sections,
                    }
                else:
                    error_message = f"Ollama API error: {response.status_code}"
                    try:
                        error_detail = response.json()
                        error_message += f" - {error_detail.get('error', '')}"
                    except Exception:
                        pass

                    print_error(error_message)
                    return {"error": True, "message": error_message}

        except Exception as e:
            error_message = f"Error communicating with Ollama: {str(e)}"
            print_error(error_message)
            return {"error": True, "message": error_message}

    def generate_code(
        self,
        description: str,
        language: str,
        temperature: float = 0.7,
        max_length: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Generate code based on a description.

        Args:
            description: Description of what the code should do
            language: The programming language to generate
            temperature: Controls randomness (0.0-1.0)
            max_length: Maximum number of tokens to generate

        Returns:
            Dictionary with generated code and metadata
        """
        # Create a code-specific prompt
        prompt = f"# {language} code to {description}\n\n"

        # Use a system prompt to guide the model to generate code
        system_prompt = (
            f"You are an expert {language} programmer. Generate high-quality, "
            f"working code that addresses the user's request. Include comments to "
            f"explain key parts. Only output code, no explanations."
        )

        # Use the text generation with code-specific settings
        result = self.generate_text(
            prompt=prompt,
            temperature=temperature,
            max_length=max_length or 2048,  # Longer default for code
            system_prompt=system_prompt,
            stream=kwargs.get("stream", True),
        )

        # Extract the code and clean it up
        code = result.get("text", "")

        # Process the code to remove markdown formatting if present
        if "```" in code:
            # Extract code from markdown code block
            code_blocks = re.findall(r"```(?: \w+)?\n(.*?)```", code, re.DOTALL)
            if code_blocks:
                code = code_blocks[0].strip()

        # Return with code-specific metadata
        return {
            "code": code,
            "language": language,
            "prompt": description,
            "model_used": self.model_name,
            "completion_tokens": result.get("completion_tokens", 0),
            "total_duration": result.get("total_duration", 0),
        }

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of texts to generate embeddings for

        Returns:
            List of embedding vectors
        """
        # Note: Ollama doesn't currently support embeddings via API for all models
        # For now, return dummy embeddings
        print_error("Embeddings not supported for Ollama models yet")
        return [[0.0] * 10] * len(texts)

    def _extract_thinking_sections(self, text: str) -> List[str]:
        """Extract all thinking sections from the text."""
        pattern = r"<think>(.*?)</think>"
        return re.findall(pattern, text, re.DOTALL)

    def _remove_thinking_sections(self, text: str) -> str:
        """Remove all thinking sections from the text."""
        pattern = r"<think>.*?</think>"
        return re.sub(pattern, "", text, flags=re.DOTALL)

    def _process_think_tags(self, text: str) -> str:
        """Process think tags in non-streaming mode."""
        # Extract thinking sections (not used but needed for clean_text)
        self._extract_thinking_sections(text)

        # Remove thinking sections from the text
        clean_text = self._remove_thinking_sections(text)

        # Return the processed text
        return clean_text
