import subprocess
import platform
import logging
import shutil
import os
from typing import List, Optional, Dict, Any, Union
from pathlib import Path
from abc import ABC, abstractmethod
from local_env_setup.core.logging import setup_logger, get_logger
from local_env_setup.core.monitoring import SetupMonitor
from local_env_setup.utils.shell import run_command
from local_env_setup.utils.file import create_directory, append_to_file

class BaseSetup(ABC):
    """Base class for all setup components.
    
    This class provides common functionality for setup components,
    including platform checks, command execution, and file operations.
    """
    
    def __init__(self):
        """Initialize the base setup component."""
        self.logger = get_logger(self.__class__.__name__)
        self.setup_logging()
        self.system = platform.system()
        self.is_macos = self.system == "Darwin"
        self.monitor = SetupMonitor()
        self.rollback_steps: List[Dict[str, Any]] = []
        
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def check_platform(self) -> bool:
        """Check if the current platform is supported.
        
        Returns:
            bool: True if the platform is supported, False otherwise
        """
        self.monitor.start_step("platform_check")
        try:
            if not self.is_macos:
                self.logger.error(f"Unsupported platform: {self.system}")
                self.monitor.end_step(False, "Unsupported platform")
                return False
            self.monitor.end_step(True)
            return True
        except Exception as e:
            self.monitor.end_step(False, str(e))
            return False
    
    def is_command_available(self, cmd: str) -> bool:
        """Check if a command is available in the system.
        
        Args:
            cmd: Command to check
            
        Returns:
            bool: True if the command exists, False otherwise
        """
        self.monitor.start_step(f"check_command_{cmd}")
        try:
            if shutil.which(cmd) is None:
                self.monitor.end_step(False, f"Command not found: {cmd}")
                return False
            self.monitor.end_step(True)
            return True
        except Exception as e:
            self.monitor.end_step(False, str(e))
            return False
    
    def run_command(self, cmd: List[str], shell: bool = False) -> bool:
        """Run a command and return its success status.
        
        Args:
            cmd: Command to run as a list of strings
            shell: Whether to run the command in a shell
            
        Returns:
            bool: True if the command succeeded, False otherwise
        """
        self.monitor.start_step(f"run_command_{'_'.join(cmd)}")
        try:
            subprocess.run(cmd, check=True, shell=shell)
            self.monitor.end_step(True)
            return True
        except subprocess.CalledProcessError as e:
            error_msg = f"Command failed: {e}"
            self.logger.error(error_msg)
            self.monitor.end_step(False, error_msg)
            return False
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            self.logger.error(error_msg)
            self.monitor.end_step(False, error_msg)
            return False
            
    def add_rollback_step(self, step: Dict[str, Any]) -> None:
        """Add a step to the rollback list."""
        self.rollback_steps.append(step)
        
    def rollback(self) -> None:
        """Execute rollback steps in reverse order."""
        self.monitor.start_step("rollback")
        try:
            for step in reversed(self.rollback_steps):
                if "function" in step and "args" in step:
                    step["function"](*step["args"])
            self.monitor.end_step(True)
        except Exception as e:
            self.monitor.end_step(False, f"Rollback failed: {e}")
            
    def create_directory(self, path: Union[str, Path]) -> bool:
        """Create a directory if it doesn't exist.
        
        Args:
            path: Path to create
            
        Returns:
            bool: True if directory exists or was created, False otherwise
        """
        self.monitor.start_step(f"create_directory_{path}")
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            self.add_rollback_step({
                "function": lambda p: Path(p).rmdir() if Path(p).exists() else None,
                "args": [path]
            })
            self.monitor.end_step(True)
            return True
        except OSError as e:
            self.logger.error(f"Failed to create directory {path}: {e}")
            self.monitor.end_step(False, str(e))
            return False
            
    def append_to_file(self, path: Union[str, Path], content: str) -> bool:
        """Append content to a file.
        
        Args:
            path: Path to the file
            content: Content to append
            
        Returns:
            bool: True if content was appended successfully, False otherwise
        """
        self.monitor.start_step(f"append_to_file_{path}")
        try:
            path = Path(path)
            if not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('a') as f:
                f.write(content)
            self.add_rollback_step({
                "function": lambda p, c: Path(p).write_text(c) if c else Path(p).unlink(),
                "args": [path, content]
            })
            self.monitor.end_step(True)
            return True
        except OSError as e:
            self.logger.error(f"Failed to append to file {path}: {e}")
            self.monitor.end_step(False, str(e))
            return False
            
    def backup_file(self, filepath: str) -> bool:
        """Backup a file by appending .bak to its name.
        
        Args:
            filepath (str): Path to the file to backup
            
        Returns:
            bool: True if backup was successful, False otherwise
        """
        if not os.path.exists(filepath):
            return True
            
        backup_path = f"{filepath}.bak"
        try:
            shutil.copy2(filepath, backup_path)
            self.logger.info(f"Backed up {filepath} to {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to backup {filepath}: {e}")
            return False
            
    def get_command_output(self, cmd: List[str], shell: bool = False) -> Optional[str]:
        """Run a command and return its output.
        
        Args:
            cmd: Command to run as a list of strings
            shell: Whether to run the command in a shell
            
        Returns:
            str: Command output if successful, None otherwise
        """
        self.monitor.start_step(f"get_command_output_{'_'.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, check=True, shell=shell)
            output = result.stdout.decode('utf-8').strip() if result.stdout else None
            self.monitor.end_step(True)
            return output
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e}")
            self.monitor.end_step(False, f"Command failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error running command: {e}")
            self.monitor.end_step(False, f"Error running command: {e}")
            return None
    
    @abstractmethod
    def run(self) -> bool:
        """Run the setup process.
        
        Returns:
            bool: True if setup was successful, False otherwise
        """
        pass 