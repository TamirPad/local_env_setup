from local_env_setup.core.base import BaseSetup
from local_env_setup.config.env import env

class TerraformSetup(BaseSetup):
    """Setup Terraform."""
    
    def check_prerequisites(self) -> bool:
        """Check if prerequisites are met."""
        if not self.is_command_available("brew"):
            self.logger.error("Homebrew is not installed. Please install it first.")
            return False
        return True
    
    def install_terraform(self) -> bool:
        """Install Terraform."""
        if self.is_command_available("terraform"):
            self.logger.info("Terraform is already installed")
            return True
            
        self.logger.info("Installing Terraform...")
        if not self.run_command(["brew", "install", "terraform"]):
            return False
            
        # Verify installation
        version = self.get_command_output(["terraform", "version"])
        if version:
            self.logger.info(f"Terraform version: {version}")
            return True
        return False
    
    def run(self):
        """Setup Terraform."""
        if not self.check_platform():
            return
            
        if not self.check_prerequisites():
            return
            
        if not self.install_terraform():
            return
            
        self.logger.info("✅ Terraform setup completed!")

def run():
    """Run the Terraform setup."""
    setup = TerraformSetup()
    setup.run() 