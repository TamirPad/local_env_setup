#!/usr/bin/env python3
"""
Script to check environment variables directly.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Get the project root directory (go up two levels from the script)
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'

print(f"Checking .env file at: {env_path}")
print(f"File exists: {env_path.exists()}")

if env_path.exists():
    # Load environment variables
    load_dotenv(env_path)
    
    # Print all environment variables
    print("\nEnvironment Variables:")
    print("-" * 30)
    for key, value in os.environ.items():
        if key.startswith('GIT_'):
            print(f"{key}: {value}")
    print("-" * 30)
else:
    print(f"Error: .env file not found at {env_path}") 