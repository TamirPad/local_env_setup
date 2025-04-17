import subprocess
from local_env_setup.config import env

def run():
    """Configure Git with user details and VS Code as default editor."""
    try:
        
        # Print current configuration
        print("\nCurrent Git Configuration:")
        print("-" * 30)
        name_result = subprocess.run(["git", "config", "--global", "user.name"], capture_output=True, text=True)
        email_result = subprocess.run(["git", "config", "--global", "user.email"], capture_output=True, text=True)
        print(f"Name:  {name_result.stdout.strip() if name_result.returncode == 0 else 'Not set'}")
        print(f"Email: {email_result.stdout.strip() if email_result.returncode == 0 else 'Not set'}")
        print("-" * 30)
        
        # Set Git user name and email
        subprocess.run(["git", "config", "--global", "user.name", env.GIT_USERNAME], check=True)
        subprocess.run(["git", "config", "--global", "user.email", env.GIT_EMAIL], check=True)
        subprocess.run(["git", "config", "--global", "core.editor", "code --wait"], check=True)
        
        # Print updated configuration
        print("\nUpdated Git Configuration:")
        print("-" * 30)
        name_result = subprocess.run(["git", "config", "--global", "user.name"], capture_output=True, text=True)
        email_result = subprocess.run(["git", "config", "--global", "user.email"], capture_output=True, text=True)
        print(f"Name:  {name_result.stdout.strip() if name_result.returncode == 0 else 'Not set'}")
        print(f"Email: {email_result.stdout.strip() if email_result.returncode == 0 else 'Not set'}")
        print("-" * 30)
        
        print("✅ Git configured with name/email and VS Code as default editor.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error configuring Git: {e}")
        raise 