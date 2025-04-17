import subprocess
import os
import platform

def run():
    """Install Docker Desktop for Mac."""
    try:
        system = platform.system()
        
        if system == "Darwin":  # macOS
            # Check if Docker is already installed
            if os.path.exists("/Applications/Docker.app"):
                print("ℹ️ Docker Desktop is already installed.")
                return

            print("Installing Docker Desktop...")
            # Install Docker Desktop using Homebrew
            subprocess.run(["brew", "install", "--cask", "docker"], check=True)
            print("✅ Docker Desktop installed successfully.")

            print("\nℹ️ Please start Docker Desktop from your Applications folder.")
            print("ℹ️ After starting, wait for the Docker engine to be running.")
            print("ℹ️ You can check the status by running: docker info")

        else:
            print(f"❌ Docker Desktop installation is not supported on {system}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing Docker: {e}")
        raise 