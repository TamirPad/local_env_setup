import os
import shutil
from local_env_setup.core.base import BaseSetup
from local_env_setup.config.env import env

class ShellSetup(BaseSetup):
    """Setup Oh My Zsh with Powerlevel10k theme and essential tools."""
    
    def __init__(self):
        super().__init__()
        self.zshrc_path = os.path.expanduser("~/.zshrc")
        self.oh_my_zsh_path = os.path.expanduser("~/.oh-my-zsh")
    
    def check_prerequisites(self) -> bool:
        """Check if prerequisites are met."""
        if not self.is_command_available("brew"):
            self.logger.error("Homebrew is not installed. Please install it first.")
            return False
        return True
    
    def install_oh_my_zsh(self) -> bool:
        """Install Oh My Zsh."""
        if os.path.exists(self.oh_my_zsh_path):
            self.logger.info("Oh My Zsh is already installed")
            return True
            
        self.logger.info("Installing Oh My Zsh...")
        install_script = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended'
        return self.run_command(install_script.split())
    
    def install_powerlevel10k(self) -> bool:
        """Install Powerlevel10k theme."""
        theme_path = os.path.join(self.oh_my_zsh_path, "custom", "themes", "powerlevel10k")
        if os.path.exists(theme_path):
            self.logger.info("Powerlevel10k is already installed")
            return True
            
        self.logger.info("Installing Powerlevel10k...")
        return self.run_command([
            "git", "clone", "--depth=1",
            "https://github.com/romkatv/powerlevel10k.git",
            theme_path
        ])
    
    def install_plugins(self) -> bool:
        """Install Zsh plugins."""
        plugins_path = os.path.join(self.oh_my_zsh_path, "custom", "plugins")
        if not self.create_directory(plugins_path):
            return False
            
        # Install zsh-autosuggestions
        autosuggestions_path = os.path.join(plugins_path, "zsh-autosuggestions")
        if not os.path.exists(autosuggestions_path):
            self.logger.info("Installing zsh-autosuggestions...")
            if not self.run_command([
                "git", "clone", "https://github.com/zsh-users/zsh-autosuggestions",
                autosuggestions_path
            ]):
                return False
                
        # Install zsh-syntax-highlighting
        highlighting_path = os.path.join(plugins_path, "zsh-syntax-highlighting")
        if not os.path.exists(highlighting_path):
            self.logger.info("Installing zsh-syntax-highlighting...")
            if not self.run_command([
                "git", "clone", "https://github.com/zsh-users/zsh-syntax-highlighting.git",
                highlighting_path
            ]):
                return False
                
        return True
    
    def setup_zshrc(self) -> bool:
        """Setup .zshrc configuration."""
        # Backup .zshrc
        if not self.backup_file(self.zshrc_path):
            self.logger.warning("Failed to backup .zshrc, continuing anyway...")
            
        # Configure .zshrc
        zsh_config = """
# Oh My Zsh configuration
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="powerlevel10k/powerlevel10k"
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
source $ZSH/oh-my-zsh.sh

# Powerlevel10k configuration
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
"""
        return self.append_to_file(self.zshrc_path, zsh_config)
    
    def run(self):
        """Setup shell environment."""
        if not self.check_platform():
            return
            
        if not self.check_prerequisites():
            return
            
        if not all([
            self.install_oh_my_zsh(),
            self.install_powerlevel10k(),
            self.install_plugins(),
            self.setup_zshrc()
        ]):
            return
            
        self.logger.info("✅ Shell setup completed!")

def run():
    """Run the shell setup."""
    setup = ShellSetup()
    setup.run() 