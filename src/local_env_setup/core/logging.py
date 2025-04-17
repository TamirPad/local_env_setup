import logging
import sys
from typing import Optional

def setup_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Setup a logger with consistent formatting."""
    logger = logging.getLogger(name)
    
    if level is None:
        level = logging.INFO
    
    # Don't add handlers if they already exist
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger 