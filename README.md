# Local Environment Setup CLI

A command-line tool to automate the setup of a local development environment on macOS.

## Project Structure

```
local_env_setup/
├── src/
│   ├── local_env_setup/
│   │   ├── __init__.py
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── env.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── base.py
│   │   ├── setup/
│   │   │   ├── __init__.py
│   │   │   ├── infra/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── docker.py
│   │   │   │   ├── kubernetes.py
│   │   │   │   └── terraform.py
│   │   │   ├── dev_tools/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── git.py
│   │   │   │   └── python.py
│   │   │   └── os/
│   │   │       ├── __init__.py
│   │   │       ├── homebrew.py
│   │   │       └── shell.py
│   └── scripts/
│       └── local_env_setup.py
├── tests/
│   ├── __init__.py
│   ├── test_base.py
│   ├── test_infra/
│   ├── test_dev_tools/
│   └── test_os/
├── docs/
├── pyproject.toml
├── .pre-commit-config.yaml
└── README.md
```

## Features

- Create and manage development directory (~/dev)
- Configure Git with user details
- Install and configure Homebrew
- Setup Python environment with pyenv and poetry
- Setup Oh My Zsh with Powerlevel10k theme and essential tools
- Install Docker Desktop for Mac
- Setup Kubernetes tools (kubectl, kubectx, Helm)
- Setup Terraform

## Installation

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone this repository:
```bash
git clone https://github.com/yourusername/local_env_setup.git
cd local_env_setup
```

3. Install dependencies:
```bash
poetry install
```

4. Make the script executable:
```bash
chmod +x src/scripts/local_env_setup.py
```

## Usage

The CLI provides several commands to set up your development environment:

```bash
# Using Poetry
poetry run local_env_setup init

# Individual commands
poetry run local_env_setup git         # Setup Git
poetry run local_env_setup homebrew    # Install Homebrew
poetry run local_env_setup python      # Setup Python with pyenv and poetry
poetry run local_env_setup shell       # Setup Oh My Zsh with Powerlevel10k
poetry run local_env_setup docker      # Install Docker Desktop
poetry run local_env_setup kubernetes  # Setup Kubernetes tools
poetry run local_env_setup terraform   # Setup Terraform
```

## Development

### Setup Development Environment

1. Install dependencies:
```bash
poetry install
```

2. Install pre-commit hooks:
```bash
poetry run pre-commit install
```

### Running Tests

```bash
poetry run pytest
```

### Code Style

The project uses:
- Ruff for linting and formatting
- MyPy for type checking

Run all checks:
```bash
# Lint and format code
poetry run ruff check .
poetry run ruff format .

# Type checking
poetry run mypy .
```

### Documentation

- All classes and methods should have docstrings
- Use type hints for all function parameters and return values
- Keep the README.md up to date with any changes

## Configuration

Edit `src/local_env_setup/config/env.py` to customize:
- Git user name and email
- Shell tools to install
- Python version
- Development directory path (defaults to ~/dev)
- Kubernetes tool versions
- Terraform version

## Requirements

- macOS (tested on macOS 12+)
- Python 3.8+
- Administrative privileges (for installations)

## License

MIT