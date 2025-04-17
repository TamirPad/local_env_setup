# Local Environment Setup Documentation

## Overview
Local Environment Setup is a tool to automate the setup of a local development environment. It handles the installation and configuration of various development tools and infrastructure components.

## Installation

### Prerequisites
- macOS (currently only supported platform)
- Python 3.8 or higher
- Git

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/local_env_setup.git
   cd local_env_setup
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Run the setup:
   ```bash
   poetry run local_env_setup init
   ```

## Usage

### Basic Setup
To set up your entire development environment:
```bash
poetry run local_env_setup init
```

### Individual Components
You can also set up individual components:

- Python environment:
  ```bash
  poetry run local_env_setup python
  ```

- Git configuration:
  ```bash
  poetry run local_env_setup git
  ```

- Shell setup:
  ```bash
  poetry run local_env_setup shell
  ```

- Infrastructure tools:
  ```bash
  poetry run local_env_setup kubernetes
  poetry run local_env_setup terraform
  poetry run local_env_setup docker
  ```

## Configuration

### Environment Variables
The following environment variables can be set to customize the setup:

- `DEV_DIR`: Development directory path (default: `~/dev`)
- `GIT_USERNAME`: Git username
- `GIT_EMAIL`: Git email
- `PYTHON_VERSION`: Python version to install (default: `3.11.0`)
- `POETRY_VERSION`: Poetry version to install (default: `1.4.2`)
- `TERRAFORM_VERSION`: Terraform version to install (default: `1.4.0`)
- `KUBECTL_VERSION`: kubectl version to install (default: `1.26.0`)
- `HELM_VERSION`: Helm version to install (default: `3.11.0`)
- `AWS_REGION`: AWS region (default: `us-east-1`)
- `AWS_PROFILE`: AWS profile (default: `default`)

### Configuration Files
- `pyproject.toml`: Project configuration and dependencies
- `ruff.toml`: Linting configuration
- `.pre-commit-config.yaml`: Pre-commit hooks configuration

## Troubleshooting

### Common Issues
1. **Permission Errors**
   - Solution: Run with sudo or ensure proper permissions

2. **Network Issues**
   - Solution: Check internet connection and proxy settings

3. **Installation Failures**
   - Solution: Check logs and retry the specific component

### Logs
Logs are stored in:
- `~/.local_env_setup/logs/` for setup logs
- `~/.local_env_setup/monitoring/` for monitoring data

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 