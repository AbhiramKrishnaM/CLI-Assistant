"""Service for managing AI models."""
import os
import logging
import gc
import re
from typing import Dict, List, Optional, Any
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig, AutoModel
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class ModelManager:
    """Manager for loading and using AI models."""
    
    def __init__(self):
        """Initialize the model manager."""
        self.models = {}
        self.tokenizers = {}
        
        # Check if GPU is available
        has_gpu = torch.cuda.is_available()
        
        # Configure models based on hardware
        if has_gpu:
            # GPU configurations - can use larger models
            self.model_configs = {
                "code_generation": {
                    "model_id": "Salesforce/codegen-350M-mono",  # Small specialized code model
                    "device": "cuda",
                    "quantization": "4bit",
                    "max_length": 1024,
                    "temperature": 0.7,
                },
                "text_generation": {
                    "model_id": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # Small chat model
                    "device": "cuda",
                    "quantization": "4bit",
                    "max_length": 512,
                    "temperature": 0.7,
                },
                "embedding": {
                    "model_id": "sentence-transformers/all-MiniLM-L6-v2",
                    "device": "cuda",
                    "quantization": "none",
                }
            }
        else:
            # CPU configurations - use smaller models
            self.model_configs = {
                "code_generation": {
                    "model_id": "Salesforce/codegen-350M-mono",  # Keep the same model
                    "device": "cpu",
                    "quantization": "none",
                    "max_length": 1024,
                    "temperature": 0.7,
                },
                "text_generation": {
                    "model_id": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # Keep using TinyLlama
                    "device": "cpu", 
                    "quantization": "none",
                    "max_length": 512,
                    "temperature": 0.7,
                },
                "embedding": {
                    "model_id": "sentence-transformers/all-MiniLM-L6-v2",
                    "device": "cpu",
                    "quantization": "none",
                }
            }
        
        # Directory to store downloaded models
        self.models_dir = os.path.expanduser("~/.aidev/models")
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Cache directory for Hugging Face models
        os.environ["TRANSFORMERS_CACHE"] = self.models_dir
        
        logger.info("Model manager initialized")
        logger.info(f"Using device: {'CUDA' if has_gpu else 'CPU'}")
    
    def get_model(self, model_type: str):
        """
        Get a model for a specific task.
        
        Args:
            model_type: Type of model to get (code_generation, text_generation, embedding)
            
        Returns:
            The loaded model or None if not available
        """
        if model_type in self.models:
            logger.info(f"Using cached {model_type} model")
            return self.models[model_type]
        
        if model_type not in self.model_configs:
            logger.error(f"Unknown model type: {model_type}")
            return None
        
        logger.info(f"Loading {model_type} model: {self.model_configs[model_type]['model_id']}...")
        
        # Setting a timeout for model loading to avoid hanging
        import signal
        
        class TimeoutException(Exception):
            pass
        
        def timeout_handler(signum, frame):
            raise TimeoutException("Model loading timed out")
        
        # Set timeout for 60 seconds
        try:
            # Only on Unix systems
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(60)
        except (AttributeError, ValueError):
            # On Windows, we can't use SIGALRM
            logger.warning("Signal timeout not supported on this platform")
        
        try:
            # Free up memory if possible
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
            config = self.model_configs[model_type]
            model_id = config["model_id"]
            device = config["device"]
            quantization = config.get("quantization", "none")
            
            if model_type == "embedding":
                # Load sentence transformer model
                model = SentenceTransformer(model_id, cache_folder=self.models_dir)
                if device == "cuda":
                    model = model.to(device)
                self.models[model_type] = model
                logger.info(f"Embedding model loaded successfully")
                
            else:  # code_generation or text_generation
                # Load tokenizer
                tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=self.models_dir)
                if not tokenizer.pad_token:
                    tokenizer.pad_token = tokenizer.eos_token
                self.tokenizers[model_type] = tokenizer
                
                # Load model with quantization if available
                if quantization == "4bit" and torch.cuda.is_available():
                    try:
                        import bitsandbytes as bnb
                        logger.info(f"Using 4-bit quantization for {model_type} model")
                        
                        # Create BitsAndBytes config
                        quantization_config = BitsAndBytesConfig(
                            load_in_4bit=True,
                            bnb_4bit_compute_dtype=torch.float16,
                            bnb_4bit_use_double_quant=True,
                            bnb_4bit_quant_type="nf4"
                        )
                        
                        # Load model with quantization
                        model = AutoModelForCausalLM.from_pretrained(
                            model_id,
                            cache_dir=self.models_dir,
                            device_map="auto",
                            quantization_config=quantization_config,
                            torch_dtype=torch.float16
                        )
                    except ImportError:
                        logger.warning("bitsandbytes not available, loading without 4-bit quantization")
                        model = AutoModelForCausalLM.from_pretrained(
                            model_id,
                            cache_dir=self.models_dir,
                            device_map="auto" if device == "cuda" else None,
                            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                        )
                else:
                    # Load without quantization
                    model = AutoModelForCausalLM.from_pretrained(
                        model_id,
                        cache_dir=self.models_dir,
                        device_map="auto" if device == "cuda" else None,
                        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                    )
                
                self.models[model_type] = model
                logger.info(f"Model {model_type} loaded successfully")
            
            # Reset the alarm
            try:
                signal.alarm(0)
            except (AttributeError, ValueError):
                pass
                
            return self.models[model_type]
            
        except TimeoutException:
            logger.error(f"Timeout while loading model {model_type}")
            # Reset the alarm
            try:
                signal.alarm(0)
            except (AttributeError, ValueError):
                pass
            # Just return None for now - no fallback
            return None
        except Exception as e:
            # Reset the alarm
            try:
                signal.alarm(0)
            except (AttributeError, ValueError):
                pass
                
            logger.error(f"Error loading model {model_type}: {str(e)}", exc_info=True)
            return None
    
    def generate_text(self, model_type: str, prompt: str, **kwargs) -> str:
        """Generate text using the specified model."""
        model = self.get_model(model_type)
        if not model:
            return f"Error: Model {model_type} not available"
        
        try:
            config = self.model_configs[model_type]
            
            # If embedding model was requested for text generation, use fallback
            if model_type == "embedding":
                logger.warning("Embedding model cannot generate text, using text_generation model instead")
                return self.generate_text("text_generation", prompt, **kwargs)
            
            # Set default parameters from config if not provided
            max_length = kwargs.get("max_length", config.get("max_length", 512))
            temperature = kwargs.get("temperature", config.get("temperature", 0.7))
            
            # Enhanced prompts for better code generation
            enhanced_prompt = prompt
            if model_type == "code_generation":
                # Enhance the prompt with more context and structure for code generation
                if "python" in prompt.lower():
                    enhanced_prompt = prompt + "\n\n```python\n# Complete implementation\n"
                elif "javascript" in prompt.lower() or "js" in prompt.lower():
                    enhanced_prompt = prompt + "\n\n```javascript\n// Complete implementation\n"
                elif "java" in prompt.lower():
                    enhanced_prompt = prompt + "\n\n```java\n// Complete implementation\n"
                else:
                    enhanced_prompt = prompt + "\n\n```\n# Complete implementation\n"
            elif model_type == "text_generation" and "TinyLlama" in config["model_id"]:
                # Format for TinyLlama chat model
                enhanced_prompt = f"<human>: {prompt}\n<assistant>:"
            
            # Generate text
            logger.info(f"Generating text with {model_type} model")
            
            # Handle direct model inference (no pipeline)
            tokenizer = self.tokenizers[model_type]
            inputs = tokenizer(enhanced_prompt, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
                
            # Generate with the model
            with torch.no_grad():
                # Add specific generation parameters for better results
                outputs = model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature if temperature > 0 else 0.2,  # Avoid 0 temperature
                    do_sample=temperature > 0,
                    num_return_sequences=1,
                    pad_token_id=tokenizer.eos_token_id,
                    repetition_penalty=1.2,  # Add repetition penalty
                    no_repeat_ngram_size=2,  # Prevent repeating 2-grams
                    top_p=0.95,  # Use nucleus sampling
                    top_k=50,    # Limit vocabulary
                )
                
            # Decode the generated text
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the prompt from the generated text
            if generated_text.startswith(enhanced_prompt):
                generated_text = generated_text[len(enhanced_prompt):].strip()
            
            # For TinyLlama, extract assistant's response
            if model_type == "text_generation" and "TinyLlama" in config["model_id"]:
                if "<human>:" in generated_text:
                    # Extract just the assistant's part
                    generated_text = generated_text.split("<assistant>:", 1)[-1].split("<human>:", 1)[0].strip()
            
            # Clean up the generated code text
            if model_type == "code_generation":
                # First, extract code from markdown code block if present
                if "```" in generated_text:
                    parts = generated_text.split("```")
                    if len(parts) >= 3:
                        code_part = parts[1]
                        # Remove language identifier if present
                        first_line_end = code_part.find('\n')
                        if first_line_end > 0:
                            language_part = code_part[:first_line_end].strip()
                            if language_part in ["python", "javascript", "java", "js"]:
                                code_part = code_part[first_line_end:].strip()
                        generated_text = code_part
                
                # Check for unfinished code blocks - if we have opener without closer, add closer
                if generated_text.count("```") % 2 == 1:
                    generated_text += "\n```"
                
                # Remove excessive repetitions (more than 3 identical lines in a row)
                lines = generated_text.split('\n')
                cleaned_lines = []
                repeat_count = 1
                prev_line = None
                
                for line in lines:
                    if line == prev_line:
                        repeat_count += 1
                        if repeat_count <= 3:  # Allow up to 3 repetitions
                            cleaned_lines.append(line)
                    else:
                        repeat_count = 1
                        cleaned_lines.append(line)
                    prev_line = line
                    
                generated_text = '\n'.join(cleaned_lines)
                
                # Ensure we have a reasonable length response
                if len(generated_text.split('\n')) > 50:
                    generated_text = '\n'.join(generated_text.split('\n')[:50])
                    generated_text += "\n# ... truncated due to length"
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}", exc_info=True)
            return f"Error generating text: {str(e)}"
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        model = self.get_model("embedding")
        if not model:
            logger.error("Embedding model not available")
            return [[0.0] * 10] * len(texts)  # Return dummy embeddings
        
        try:
            logger.info(f"Generating embeddings for {len(texts)} texts")
            embeddings = model.encode(texts)
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}", exc_info=True)
            return [[0.0] * 10] * len(texts)  # Return dummy embeddings
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get information about available models."""
        return [
            {
                "type": model_type,
                "model_id": config["model_id"],
                "loaded": model_type in self.models,
                "device": config.get("device", "cpu"),
                "quantization": config.get("quantization", "none"),
            }
            for model_type, config in self.model_configs.items()
        ]
    
    def unload_model(self, model_type: str) -> bool:
        """Unload a model to free memory."""
        if model_type in self.models:
            logger.info(f"Unloading model {model_type}")
            
            # Remove from models dictionary
            del self.models[model_type]
            
            # Remove tokenizer if exists
            if model_type in self.tokenizers:
                del self.tokenizers[model_type]
            
            # Force garbage collection
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
            return True
        return False


# Singleton instance
model_manager = ModelManager() 