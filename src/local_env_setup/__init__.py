"""
Local Environment Setup CLI
A tool to automate the setup of a local development environment.
"""

__version__ = "0.1.0"

from local_env_setup.setup.infra.kubernetes import run as setup_kubernetes
from local_env_setup.setup.infra.terraform import run as setup_terraform

__all__ = ['setup_kubernetes', 'setup_terraform'] 