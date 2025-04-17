import os
from typing import Dict, List
from dataclasses import dataclass, field
from dotenv import load_dotenv
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent.parent.parent

# Load environment variables from .env file
env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded .env file from: {env_path}")
else:
    print(f"❌ .env file not found at: {env_path}")

@dataclass
class EnvConfig:
    """Environment configuration settings."""
    # Development directory
    DEV_DIR: str = os.path.expanduser("~/dev")
    
    # Git configuration
    GIT_USERNAME: str = os.getenv("GIT_USERNAME", "")
    GIT_EMAIL: str = os.getenv("GIT_EMAIL", "")
    
    # Python configuration
    PYTHON_VERSION: str = "3.11.0"
    POETRY_VERSION: str = "1.4.2"
    
    # Shell configuration
    ZSH_PLUGINS: List[str] = field(default_factory=lambda: [
        "zsh-autosuggestions",
        "zsh-syntax-highlighting",
        "git",
        "docker",
        "kubectl"
    ])
    
    # Infrastructure tools
    TERRAFORM_VERSION: str = "1.4.0"
    KUBECTL_VERSION: str = "1.26.0"
    HELM_VERSION: str = "3.11.0"
    
    # AWS configuration
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_PROFILE: str = os.getenv("AWS_PROFILE", "default")
    
    # Docker configuration
    DOCKER_COMPOSE_VERSION: str = "2.17.0"
    
    # Development tools
    VSCODE_EXTENSIONS: List[str] = field(default_factory=lambda: [
        "ms-python.python",
        "ms-azuretools.vscode-docker",
        "hashicorp.terraform",
        "redhat.vscode-yaml"
    ])

# Create environment instance
env = EnvConfig()

# Debug: Print loaded environment variables
print("\nLoaded Environment Variables..")
