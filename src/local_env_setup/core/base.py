import subprocess
import platform
import logging
import shutil
import os
from typing import List, Optional, Dict, Any
from pathlib import Path
from abc import ABC, abstractmethod
from local_env_setup.core.logging import setup_logger
from local_env_setup.core.monitoring import SetupMonitor
from local_env_setup.utils.shell import run_command
from local_env_setup.utils.file import create_directory, append_to_file

class BaseSetup(ABC):
    """Base class for all setup modules."""
    
    def __init__(self):
        """Initialize the setup class."""
        self.logger = logging.getLogger(self.__class__.__name__)
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
        """Check if the current platform is supported."""
        self.monitor.start_step("platform_check")
        try:
            if not self.is_macos:
                self.logger.error("This setup is only supported on macOS")
                self.monitor.end_step(False, "Unsupported platform")
                return False
            self.monitor.end_step(True)
            return True
        except Exception as e:
            self.monitor.end_step(False, str(e))
            return False
    
    def is_command_available(self, command: str) -> bool:
        """Check if a command is available in the system."""
        self.monitor.start_step(f"check_command_{command}")
        try:
            subprocess.run(["which", command], check=True, capture_output=True)
            self.monitor.end_step(True)
            return True
        except subprocess.CalledProcessError:
            self.monitor.end_step(False, f"Command not found: {command}")
            return False
        except Exception as e:
            self.monitor.end_step(False, str(e))
            return False
    
    def run_command(self, command: List[str], cwd: Optional[str] = None) -> bool:
        """Run a shell command and return success status."""
        self.monitor.start_step(f"run_command_{'_'.join(command)}")
        try:
            subprocess.run(command, check=True, cwd=cwd)
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
            
    def create_directory(self, path: str) -> bool:
        """Create a directory and add rollback step."""
        self.monitor.start_step(f"create_directory_{path}")
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            self.add_rollback_step({
                "function": lambda p: Path(p).rmdir() if Path(p).exists() else None,
                "args": [path]
            })
            self.monitor.end_step(True)
            return True
        except Exception as e:
            self.monitor.end_step(False, str(e))
            return False
            
    def append_to_file(self, filepath: str, content: str) -> bool:
        """Append content to a file and add rollback step."""
        self.monitor.start_step(f"append_to_file_{filepath}")
        try:
            original_content = None
            if Path(filepath).exists():
                with open(filepath, "r") as f:
                    original_content = f.read()
                    
            with open(filepath, "a") as f:
                f.write(content)
                
            self.add_rollback_step({
                "function": lambda p, c: Path(p).write_text(c) if c else Path(p).unlink(),
                "args": [filepath, original_content]
            })
            
            self.monitor.end_step(True)
            return True
        except Exception as e:
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
            
    def get_command_output(self, command: list) -> str:
        """Get the output of a command.
        
        Args:
            command (list): Command to run and its arguments
            
        Returns:
            str: Command output or empty string if command fails
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e}")
            return ""
        except Exception as e:
            self.logger.error(f"Error running command: {e}")
            return ""
    
    @abstractmethod
    def run(self):
        """Run the setup process."""
        pass 