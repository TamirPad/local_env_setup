import os
from local_env_setup.core.base import BaseSetup
from local_env_setup.config.env import env

class KubernetesSetup(BaseSetup):
    """Setup Kubernetes tools (kubectl, kubectx, Helm)."""
    
    def __init__(self):
        super().__init__()
        self.kube_dir = os.path.expanduser("~/.kube")
        self.zshrc_path = os.path.expanduser("~/.zshrc")
    
    def check_prerequisites(self) -> bool:
        """Check if prerequisites are met."""
        if not self.is_command_available("brew"):
            self.logger.error("Homebrew is not installed. Please install it first.")
            return False
        return True
    
    def install_kubectl(self) -> bool:
        """Install kubectl."""
        if self.is_command_available("kubectl"):
            self.logger.info("kubectl is already installed")
            return True
            
        self.logger.info("Installing kubectl...")
        return self.run_command(["brew", "install", "kubectl"])
    
    def install_kubectx(self) -> bool:
        """Install kubectx."""
        if self.is_command_available("kubectx"):
            self.logger.info("kubectx is already installed")
            return True
            
        self.logger.info("Installing kubectx...")
        return self.run_command(["brew", "install", "kubectx"])
    
    def install_helm(self) -> bool:
        """Install Helm."""
        if self.is_command_available("helm"):
            self.logger.info("Helm is already installed")
            return True
            
        self.logger.info("Installing Helm...")
        return self.run_command(["brew", "install", "helm"])
    
    def setup_kubeconfig(self) -> bool:
        """Setup kubeconfig directory."""
        if not self.create_directory(self.kube_dir):
            return False
            
        # Check if kubectl is properly installed
        version = self.get_command_output(["kubectl", "version", "--client", "--short"])
        if version:
            self.logger.info(f"kubectl version: {version}")
        return True
    
    def setup_shell_completion(self) -> bool:
        """Setup shell completion for kubectl."""
        # Backup .zshrc
        if not self.backup_file(self.zshrc_path):
            self.logger.warning("Failed to backup .zshrc, continuing anyway...")
        
        # Add kubectl completion
        kube_config = """
# Kubernetes configuration
source <(kubectl completion zsh)
alias k=kubectl
complete -F __start_kubectl k
"""
        return self.append_to_file(self.zshrc_path, kube_config)
    
    def run(self):
        """Setup Kubernetes tools."""
        if not self.check_platform():
            return
            
        if not self.check_prerequisites():
            return
            
        # Install tools
        if not all([
            self.install_kubectl(),
            self.install_kubectx(),
            self.install_helm()
        ]):
            return
            
        # Setup configuration
        if not all([
            self.setup_kubeconfig(),
            self.setup_shell_completion()
        ]):
            return
            
        self.logger.info("✅ Kubernetes tools setup completed!")

def run():
    """Run the Kubernetes setup."""
    setup = KubernetesSetup()
    setup.run() 