import pytest
import tempfile
import shutil
import os
from pathlib import Path
from typing import Generator

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_home_dir(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a mock home directory for tests."""
    home_dir = temp_dir / "home"
    home_dir.mkdir()
    
    # Create mock shell rc files
    (home_dir / ".zshrc").touch()
    (home_dir / ".bashrc").touch()
    
    # Create mock SSH directory
    ssh_dir = home_dir / ".ssh"
    ssh_dir.mkdir(mode=0o700)
    
    yield home_dir

@pytest.fixture
def mock_dev_dir(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a mock development directory for tests."""
    dev_dir = temp_dir / "dev"
    dev_dir.mkdir()
    yield dev_dir

@pytest.fixture
def mock_pyenv_root(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a mock pyenv root directory for tests."""
    pyenv_root = temp_dir / ".pyenv"
    pyenv_root.mkdir()
    
    # Create mock Python versions
    versions_dir = pyenv_root / "versions"
    versions_dir.mkdir()
    (versions_dir / "3.11.0").mkdir()
    
    yield pyenv_root

@pytest.fixture
def mock_poetry_home(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a mock Poetry home directory for tests."""
    poetry_home = temp_dir / ".local" / "bin"
    poetry_home.mkdir(parents=True)
    (poetry_home / "poetry").touch(mode=0o755)
    yield poetry_home

@pytest.fixture
def mock_environment(monkeypatch, mock_home_dir: Path, mock_dev_dir: Path) -> None:
    """Set up mock environment variables."""
    monkeypatch.setenv("HOME", str(mock_home_dir))
    monkeypatch.setenv("DEV_DIR", str(mock_dev_dir))
    monkeypatch.setenv("SHELL", "/bin/zsh")
    
    # Mock which command
    def mock_which(cmd: str) -> str:
        if cmd in ["pyenv", "curl", "git", "brew"]:
            return f"/usr/local/bin/{cmd}"
        return ""
    
    monkeypatch.setattr("shutil.which", mock_which)

@pytest.fixture
def mock_subprocess(monkeypatch) -> None:
    """Mock subprocess.run for testing."""
    class MockResult:
        def __init__(self, returncode=0, stdout="", stderr=""):
            self.returncode = returncode
            self.stdout = stdout.encode() if isinstance(stdout, str) else stdout
            self.stderr = stderr.encode() if isinstance(stderr, str) else stderr
            
    def mock_run(*args, **kwargs):
        cmd = args[0]
        if isinstance(cmd, list):
            cmd = " ".join(cmd)
            
        # Mock successful commands
        if "which" in cmd:
            return MockResult(0)
        elif "pyenv versions" in cmd:
            return MockResult(0, "3.11.0")
        elif "python --version" in cmd:
            return MockResult(0, "Python 3.11.0")
        elif "pip --version" in cmd:
            return MockResult(0, "pip 22.3.1")
            
        return MockResult(0)
        
    monkeypatch.setattr("subprocess.run", mock_run) 