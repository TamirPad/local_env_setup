"""
Environment variable utilities for the local environment setup tool.
This module provides functionality to load and access environment variables from .env files.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

def load_env_file(env_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load environment variables from a .env file.
    
    Args:
        env_file (Optional[str]): Path to the .env file. If None, looks for .env in the current directory
                                 and parent directories.
    
    Returns:
        Dict[str, Any]: Dictionary containing the loaded environment variables
    
    Raises:
        FileNotFoundError: If the .env file is not found
    """
    if env_file:
        env_path = Path(env_file)
    else:
        # Start with current directory and look up
        current_dir = Path.cwd()
        env_path = current_dir / '.env'
        
        while not env_path.exists() and current_dir.parent != current_dir:
            current_dir = current_dir.parent
            env_path = current_dir / '.env'
    
    if not env_path.exists():
        raise FileNotFoundError(f"No .env file found in {env_path} or its parent directories")
    
    load_dotenv(env_path)
    
    # Return a dictionary of all environment variables
    return {key: value for key, value in os.environ.items()}

def get_env_var(key: str, default: Any = None) -> Any:
    """
    Get an environment variable value.
    
    Args:
        key (str): The environment variable key
        default (Any): Default value to return if the key is not found
    
    Returns:
        Any: The value of the environment variable or the default value
    """
    return os.environ.get(key, default)

def set_env_var(key: str, value: str) -> None:
    """
    Set an environment variable.
    
    Args:
        key (str): The environment variable key
        value (str): The value to set
    """
    os.environ[key] = value 