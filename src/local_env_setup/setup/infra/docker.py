"""Docker setup module for installing and configuring Docker Desktop and Docker Compose."""

import subprocess
import os
import platform
from pathlib import Path
from typing import Optional

from local_env_setup.core.base import BaseSetup
from local_env_setup.config.env import env
from local_env_setup.utils.shell import run_command, get_command_output

class DockerSetup(BaseSetup):
    """Setup class for Docker Desktop and Docker Compose."""
    
    def __init__(self):
        """Initialize DockerSetup."""
        super().__init__()
        self.docker_compose_version = env.DOCKER_COMPOSE_VERSION
        self.docker_app_path = Path("/Applications/Docker.app")
        self.docker_compose_path = Path("/usr/local/bin/docker-compose")
    
    def check_platform(self) -> bool:
        """Check if the current platform is supported.
        
        Docker setup supports both macOS and Linux.
        
        Returns:
            bool: True if the platform is supported, False otherwise
        """
        self.monitor.start_step("platform_check")
        try:
            if self.system not in ["Darwin", "Linux"]:
                self.logger.error(f"Unsupported platform: {self.system}")
                self.monitor.end_step(False, "Unsupported platform")
                return False
            self.monitor.end_step(True)
            return True
        except Exception as e:
            self.monitor.end_step(False, str(e))
            return False
    
    def check_prerequisites(self) -> bool:
        """Check if Homebrew is installed."""
        return self.is_command_available("brew")
    
    def install(self) -> bool:
        """Install Docker Desktop and Docker Compose."""
        try:
            # Install Docker Desktop
            if not self.docker_app_path.exists():
                self.logger.info("Installing Docker Desktop...")
                if not self.run_command(["brew", "install", "--cask", "docker"]):
                    self.logger.error("Failed to install Docker Desktop")
                    return False
                self.logger.info("✅ Docker Desktop installed successfully")
            
            # Install Docker Compose
            if not self.docker_compose_path.exists():
                self.logger.info(f"Installing Docker Compose {self.docker_compose_version}...")
                if not self.run_command([
                    "curl", "-L", 
                    f"https://github.com/docker/compose/releases/download/{self.docker_compose_version}/docker-compose-{platform.system().lower()}-{platform.machine()}",
                    "-o", str(self.docker_compose_path)
                ]):
                    self.logger.error("Failed to download Docker Compose")
                    return False
                
                # Make docker-compose executable
                self.docker_compose_path.chmod(0o755)
                self.logger.info("✅ Docker Compose installed successfully")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during Docker installation: {str(e)}")
            return False
    
    def configure(self) -> bool:
        """Configure Docker settings."""
        try:
            # Add current user to docker group
            if platform.system() == "Linux":
                self.logger.info("Adding current user to docker group...")
                if not self.run_command(["sudo", "usermod", "-aG", "docker", os.getenv("USER")]):
                    self.logger.error("Failed to add user to docker group")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during Docker configuration: {str(e)}")
            return False
    
    def verify(self) -> bool:
        """Verify Docker installation."""
        try:
            # Check Docker version
            docker_version = get_command_output(["docker", "--version"])
            if not docker_version:
                self.logger.error("Docker is not properly installed")
                return False
            self.logger.info(f"Docker version: {docker_version.strip()}")
            
            # Check Docker Compose version
            compose_version = get_command_output(["docker-compose", "--version"])
            if not compose_version:
                self.logger.error("Docker Compose is not properly installed")
                return False
            self.logger.info(f"Docker Compose version: {compose_version.strip()}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying Docker installation: {str(e)}")
            return False
    
    def run(self) -> bool:
        """Run the complete Docker setup process."""
        if not self.check_platform():
            return False
            
        if not self.check_prerequisites():
            self.logger.error("Prerequisites not met")
            return False
            
        if not self.install():
            return False
            
        if not self.configure():
            return False
            
        if not self.verify():
            return False
            
        self.logger.info("Docker setup completed successfully")
        return True

def run() -> bool:
    """Run the Docker setup process."""
    return DockerSetup().run() 