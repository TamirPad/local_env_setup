"""Shell utility functions for running commands."""

import subprocess
import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

def run_command(command: List[str], cwd: Optional[str] = None) -> Tuple[bool, str]:
    """Run a shell command and return its success status and output.
    
    Args:
        command (List[str]): The command to run as a list of strings
        cwd (Optional[str]): Working directory to run the command in
        
    Returns:
        Tuple[bool, str]: (success status, command output)
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e.stderr}")
        return False, e.stderr
    except Exception as e:
        logger.error(f"Error running command: {str(e)}")
        return False, str(e) 