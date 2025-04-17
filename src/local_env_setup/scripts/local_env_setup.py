#!/usr/bin/env python3
import argparse
import sys
import os
from local_env_setup.setup.dev_tools.git import run as setup_git
from local_env_setup.setup.os.homebrew import run as install_homebrew
from local_env_setup.setup.dev_tools.python import run as setup_python
from local_env_setup.setup.os.shell import run as setup_shell
from local_env_setup.setup.infra.kubernetes import run as setup_kubernetes
from local_env_setup.setup.infra.terraform import run as setup_terraform
from local_env_setup.setup.infra.docker import run as install_docker
from local_env_setup.config import env

def init():
    print("Bootstrapping local development environment...")
    # Create dev directory if it doesn't exist
    dev_dir = os.path.expanduser(env.DEV_DIR)
    if not os.path.exists(dev_dir):
        os.makedirs(dev_dir)
        print(f"✅ Created development directory: {dev_dir}")
    
    setup_git()
    install_homebrew()
    setup_python()
    setup_shell()
    install_docker()
    setup_kubernetes()
    setup_terraform()
    print("✅ Dev environment initialized!")

def git():
    setup_git()

def homebrew():
    install_homebrew()

def python():
    setup_python()

def shell():
    setup_shell()

def docker():
    install_docker()

def kubernetes():
    setup_kubernetes()

def terraform():
    setup_terraform()

def main():
    parser = argparse.ArgumentParser(description="Local Environment Setup CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommands
    subparsers.add_parser("init", help="Initialize dev environment")
    subparsers.add_parser("git", help="Setup Git configuration")
    subparsers.add_parser("homebrew", help="Install Homebrew")
    subparsers.add_parser("python", help="Setup Python environment")
    subparsers.add_parser("shell", help="Setup Oh My Zsh and Powerlevel10k")
    subparsers.add_parser("docker", help="Install Docker Desktop")
    subparsers.add_parser("kubernetes", help="Setup Kubernetes tools")
    subparsers.add_parser("terraform", help="Setup Terraform")

    args = parser.parse_args()

    # Command handling
    if args.command == "init":
        init()
    elif args.command == "git":
        git()
    elif args.command == "homebrew":
        homebrew()
    elif args.command == "python":
        python()
    elif args.command == "shell":
        shell()
    elif args.command == "docker":
        docker()
    elif args.command == "kubernetes":
        kubernetes()
    elif args.command == "terraform":
        terraform()
    else:
        print("Usage: local_env_setup {init|git|homebrew|python|shell|docker|kubernetes|terraform}")
        sys.exit(1)

if __name__ == "__main__":
    main() 