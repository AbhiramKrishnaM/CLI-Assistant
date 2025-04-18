"""Service for managing AI models."""
import os
import logging
import gc
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
        self.model_configs = {
            "code_generation": {
                "model_id": "gpt2",  # Simple model that doesn't need sentencepiece
                "device": "cuda" if torch.cuda.is_available() else "cpu",
                "quantization": "none",
                "max_length": 1024,
                "temperature": 0.7,
            },
            "text_generation": {
                "model_id": "gpt2",  # Simple model available without special deps
                "device": "cuda" if torch.cuda.is_available() else "cpu",
                "quantization": "none",
                "max_length": 512,
                "temperature": 0.7,
            },
            "embedding": {
                "model_id": "sentence-transformers/all-MiniLM-L6-v2",
                "device": "cuda" if torch.cuda.is_available() else "cpu",
            }
        }
        
        # Directory to store downloaded models
        self.models_dir = os.path.expanduser("~/.aidev/models")
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Cache directory for Hugging Face models
        os.environ["TRANSFORMERS_CACHE"] = self.models_dir
        
        logger.info("Model manager initialized")
        logger.info(f"Using device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    
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
        
        try:
            # Free up memory if possible
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
            config = self.model_configs[model_type]
            model_id = config["model_id"]
            device = config["device"]
            
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
                
                # Load model directly without pipeline
                model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    cache_dir=self.models_dir,
                    device_map="auto" if device == "cuda" else None,
                    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                )
                
                self.models[model_type] = model
                logger.info(f"Model {model_type} loaded successfully")
            
            return self.models[model_type]
            
        except Exception as e:
            logger.error(f"Error loading model {model_type}: {str(e)}", exc_info=True)
            
            # Provide a MockModel as fallback for development
            logger.warning(f"Using MockModel as fallback for {model_type}")
            model = MockModel(self.model_configs[model_type])
            self.models[model_type] = model
            return model
    
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
            
            # Generate text
            logger.info(f"Generating text with {model_type} model")
            
            # Check if we're using a mock model (fallback)
            if isinstance(model, MockModel):
                return model.generate(prompt, **kwargs)
                
            # Handle direct model inference (no pipeline)
            tokenizer = self.tokenizers[model_type]
            inputs = tokenizer(prompt, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
                
            # Generate with the model
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature if temperature > 0 else None,
                    do_sample=temperature > 0,
                    num_return_sequences=1,
                    pad_token_id=tokenizer.eos_token_id,
                )
                
            # Decode the generated text
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the prompt from the generated text
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
                
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


class MockModel:
    """Mock implementation of a model for development."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the mock model."""
        self.config = config
        self.model_id = config["model_id"]
    
    def __call__(self, prompt: str, **kwargs) -> List[Dict[str, str]]:
        """Generate text based on a prompt."""
        # This is a mock implementation
        return [{"generated_text": prompt + f"\n\nMock response from {self.model_id} for this prompt."}]
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text based on a prompt."""
        # This is a mock implementation
        return f"Mock response from {self.model_id} for: {prompt[:50]}..."
    
    def encode(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts."""
        # This is a mock implementation
        return [[0.1, 0.2, 0.3, 0.4, 0.5] for _ in texts]


# Singleton instance
model_manager = ModelManager() 