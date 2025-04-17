import subprocess
import os
import shutil
import time
import re
from pathlib import Path
from typing import Optional
from local_env_setup.config import env
from local_env_setup.core.base import BaseSetup

class PythonSetup(BaseSetup):
    """Setup component for Python environment configuration.
    
    This class handles the installation and configuration of Python using pyenv.
    It ensures the correct Python version is installed and set as the global version.
    """
    
    def __init__(self):
        """Initialize the Python setup component."""
        super().__init__()
        self.pyenv_root = Path.home() / ".pyenv"
        self.shell_rc = self._get_shell_rc()
        
    def _get_shell_rc(self) -> Path:
        """Get the path to the shell rc file based on the current shell.
        
        Returns:
            Path: Path to the shell rc file
        """
        shell = os.environ.get("SHELL", "")
        if "bash" in shell:
            return Path.home() / ".bashrc"
        elif "zsh" in shell:
            return Path.home() / ".zshrc"
        else:
            raise RuntimeError(f"Unsupported shell: {shell}")
    
    def check_platform(self) -> bool:
        """Check if the current platform is supported.
        
        Returns:
            bool: True if the platform is supported, False otherwise
        """
        return super().check_platform()
    
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met.
        
        Returns:
            bool: True if all prerequisites are met, False otherwise
        """
        if not shutil.which("brew"):
            self.logger.error("Homebrew is not installed")
            return False
            
        if not shutil.which("curl"):
            self.logger.error("curl is not installed")
            return False
            
        return True
    
    def install(self) -> bool:
        """Install pyenv and required Python version.
        
        Returns:
            bool: True if installation was successful, False otherwise
        """
        try:
            # Install pyenv if not already installed
            if not self.check_command_exists("pyenv"):
                self.logger.info("Installing pyenv...")
                subprocess.run(["brew", "install", "pyenv"], check=True)
                
                # Add pyenv configuration to shell rc file
                pyenv_config = f"""
# Pyenv configuration
export PYENV_ROOT="{self.pyenv_root}"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
"""
                with open(self.shell_rc, "a") as f:
                    f.write(pyenv_config)
                self.logger.info(f"Added pyenv configuration to {self.shell_rc}")
                
                # Source the shell rc file
                subprocess.run(f"source {self.shell_rc}", shell=True, check=True)
            
            # Install Python version if not already installed
            if not self.verify_python_version(env.PYTHON_VERSION):
                self.logger.info(f"Installing Python {env.PYTHON_VERSION}...")
                subprocess.run(["pyenv", "install", env.PYTHON_VERSION], check=True)
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error during installation: {e}")
            return False
    
    def configure(self) -> bool:
        """Configure Python environment.
        
        Returns:
            bool: True if configuration was successful, False otherwise
        """
        try:
            # Set global Python version
            subprocess.run(["pyenv", "global", env.PYTHON_VERSION], check=True)
            self.logger.info(f"Set Python {env.PYTHON_VERSION} as global version")
            
            # Give the system a moment to recognize the new Python version
            time.sleep(2)
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error during configuration: {e}")
            return False
    
    def verify(self) -> bool:
        """Verify Python installation and configuration.
        
        Returns:
            bool: True if verification succeeds, False otherwise.
        """
        try:
            # First try to get version from pyenv
            result = subprocess.run(['pyenv', 'version'], capture_output=True, text=False)
            if result.returncode == 0:
                version = result.stdout.decode('utf-8').strip()
                version_match = re.search(r'(\d+\.\d+\.\d+)', version)
                if version_match:
                    current_version = version_match.group(1)
                    if current_version == env.PYTHON_VERSION:
                        self.logger.info(f"Python version {current_version} verified successfully")
                        return True
                    else:
                        self.logger.error(f"Python version mismatch. Expected {env.PYTHON_VERSION}, got {current_version}")
                        return False
            
            # Fallback to direct Python version check
            result = subprocess.run(['python', '--version'], capture_output=True, text=False)
            if result.returncode == 0:
                version = result.stdout.decode('utf-8').strip()
                version_match = re.search(r'(\d+\.\d+\.\d+)', version)
                if version_match:
                    current_version = version_match.group(1)
                    if current_version == env.PYTHON_VERSION:
                        self.logger.info(f"Python version {current_version} verified successfully")
                        return True
                    else:
                        self.logger.error(f"Python version mismatch. Expected {env.PYTHON_VERSION}, got {current_version}")
                        return False
            
            self.logger.error("Could not determine Python version")
            return False
            
        except Exception as e:
            self.logger.error(f"Python verification failed: {str(e)}")
            return False
    
    def check_command_exists(self, cmd: str) -> bool:
        """Check if a command exists in the system.
        
        Args:
            cmd: Command to check
            
        Returns:
            bool: True if the command exists, False otherwise
        """
        return subprocess.run(["which", cmd], capture_output=True).returncode == 0
    
    def verify_python_version(self, version: str) -> bool:
        """Verify if a Python version is valid and installed.
        
        Args:
            version: Python version to verify
            
        Returns:
            bool: True if the version is valid and installed, False otherwise
        """
        try:
            result = subprocess.run(["pyenv", "versions"], capture_output=True, text=False)
            if result.stdout is None:
                return False
            return version in result.stdout.decode('utf-8')
        except subprocess.CalledProcessError:
            return False
            
    def run(self) -> bool:
        """Run the complete Python setup process.
        
        Returns:
            bool: True if setup completes successfully, False otherwise.
        """
        try:
            if not self.check_platform():
                return False
                
            if not self.check_prerequisites():
                return False
                
            if not self.install():
                return False
                
            if not self.configure():
                return False
                
            if not self.verify():
                return False
                
            self.logger.info("Python setup completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Python setup failed: {str(e)}")
            return False

def get_current_python_version():
    """Get the current Python version."""
    try:
        result = subprocess.run(["python", "--version"], capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def backup_file(file_path):
    """Create a backup of a file if it exists."""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.bak"
        shutil.copy2(file_path, backup_path)
        return backup_path
    return None

def run():
    """Setup Python environment using pyenv."""
    try:
        # Check if Homebrew is installed
        if not check_command_exists("brew"):
            print("❌ Homebrew is not installed. Please install it first.")
            return

        # Install pyenv
        if not install_pyenv():
            return

        # Check if curl is installed
        if not check_command_exists("curl"):
            print("❌ curl is not installed. Please install it first.")
            return

        # Check if Python version is already installed
        if verify_python_version(env.PYTHON_VERSION):
            print(f"✅ Python {env.PYTHON_VERSION} is already installed.")
        else:
            # Install Python version
            print(f"Installing Python {env.PYTHON_VERSION}...")
            subprocess.run(["pyenv", "install", env.PYTHON_VERSION], check=True)
            print(f"✅ Python {env.PYTHON_VERSION} installed successfully.")

        # Set global Python version
        subprocess.run(["pyenv", "global", env.PYTHON_VERSION], check=True)
        print(f"✅ Set Python {env.PYTHON_VERSION} as global version.")
        
        # Give the system a moment to recognize the new Python version
        time.sleep(2)
        
        # Verify Python version using pyenv
        result = subprocess.run(["pyenv", "version"], capture_output=True, text=True)
        if env.PYTHON_VERSION not in result.stdout:
            print(f"⚠️  Warning: Python version verification failed. Please restart your shell.")
            print(f"   Expected: {env.PYTHON_VERSION}")
            print(f"   Current: {result.stdout.strip()}")
        else:
            print(f"✅ Verified Python version: {result.stdout.strip()}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error during Python setup: {e}")
        return
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return 