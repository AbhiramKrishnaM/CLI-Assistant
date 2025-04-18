"""Configuration management for the CLI tool."""
import os
import json
from typing import Any, Dict, Optional

# Default configuration directory
CONFIG_DIR = os.path.expanduser("~/.aidev")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Default configuration
DEFAULT_CONFIG = {
    "backend": {
        "url": "http://localhost:8000",
        "timeout": 30,
    },
    "models": {
        "code_generation": "huggingface/CodeLlama-7b-Instruct-hf",
        "text_generation": "huggingface/mistralai/Mistral-7B-Instruct-v0.2",
    },
    "appearance": {
        "theme": "default",
        "color_output": True,
    },
    "history": {
        "save_history": True,
        "max_history_items": 100,
    },
    "ollama": {
        "enabled": True,
        "url": "http://localhost:11434/api",
        "default_model": "deepseek-r1:7b",
        "timeout": 60
    }
}

def ensure_config_dir():
    """Ensure the configuration directory exists."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)

def load_config() -> Dict[str, Any]:
    """Load the configuration from the config file."""
    ensure_config_dir()
    
    if not os.path.exists(CONFIG_FILE):
        # Create default config if it doesn't exist
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            
        # Make sure the config has the latest keys
        updated = False
        for section, values in DEFAULT_CONFIG.items():
            if section not in config:
                config[section] = values
                updated = True
            elif isinstance(values, dict):
                for key, value in values.items():
                    if key not in config[section]:
                        config[section][key] = value
                        updated = True
        
        if updated:
            save_config(config)
            
        return config
    except json.JSONDecodeError:
        # If the config file is corrupted, use the default
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]) -> bool:
    """Save the configuration to the config file."""
    ensure_config_dir()
    
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except IOError:
        return False

def get_config_value(key_path: str, default: Any = None) -> Any:
    """
    Get a configuration value by its key path.
    
    Example: get_config_value("backend.url") would return the URL from the backend section.
    """
    config = load_config()
    
    keys = key_path.split(".")
    value = config
    
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default

def set_config_value(key_path: str, value: Any) -> bool:
    """
    Set a configuration value by its key path.
    
    Example: set_config_value("backend.url", "http://localhost:9000")
    """
    config = load_config()
    
    keys = key_path.split(".")
    config_section = config
    
    # Navigate to the nested section
    for key in keys[:-1]:
        if key not in config_section:
            config_section[key] = {}
        config_section = config_section[key]
    
    # Set the final value
    config_section[keys[-1]] = value
    
    return save_config(config)

def reset_config() -> bool:
    """Reset the configuration to default values."""
    return save_config(DEFAULT_CONFIG.copy()) 