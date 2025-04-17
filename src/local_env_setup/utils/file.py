"""File utility functions for file operations."""

import os
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

def create_directory(path: str) -> bool:
    """Create a directory if it doesn't exist.
    
    Args:
        path (str): Path to the directory to create
        
    Returns:
        bool: True if directory was created or already exists, False otherwise
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {str(e)}")
        return False

def append_to_file(filepath: str, content: str) -> bool:
    """Append content to a file.
    
    Args:
        filepath (str): Path to the file
        content (str): Content to append
        
    Returns:
        bool: True if content was appended successfully, False otherwise
    """
    try:
        with open(filepath, 'a') as f:
            f.write(content + '\n')
        return True
    except Exception as e:
        logger.error(f"Failed to append to file {filepath}: {str(e)}")
        return False 