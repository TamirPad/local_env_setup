from local_env_setup.core.base import BaseSetup
from local_env_setup.config.env import env
import subprocess

class HomebrewSetup(BaseSetup):
    """Setup Homebrew package manager."""
    
    def check_prerequisites(self) -> bool:
        """Check if prerequisites are met."""
        if self.is_command_available("brew"):
            self.logger.info("Homebrew is already installed")
            return True
        return True
    
    def install_homebrew(self) -> bool:
        """Install Homebrew."""
        self.logger.info("Installing Homebrew...")
        try:
            # First download the install script
            result = subprocess.run(
                ['curl', '-fsSL', 'https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh'],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                self.logger.error("Failed to download Homebrew installation script")
                return False
                
            # Then execute the downloaded script
            install_command = [
                '/bin/bash',
                '-c',
                result.stdout
            ]
            return self.run_command(install_command)
        except Exception as e:
            self.logger.error(f"Error during Homebrew installation: {e}")
            return False
    
    def run(self):
        """Setup Homebrew."""
        if not self.check_platform():
            return
            
        if not self.check_prerequisites():
            return
            
        if not self.install_homebrew():
            return
            
        self.logger.info("✅ Homebrew setup completed!")

def run():
    """Run the Homebrew setup."""
    setup = HomebrewSetup()
    setup.run() 