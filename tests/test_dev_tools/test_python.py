import pytest
from pathlib import Path
from local_env_setup.setup.dev_tools.python import run as setup_python
from local_env_setup.core.monitoring import SetupMonitor

def test_python_setup_success(
    mock_environment,
    mock_subprocess,
    mock_pyenv_root,
    mock_poetry_home,
    tmp_path
):
    """Test successful Python setup."""
    # Run the setup
    setup_python()
    
    # Verify pyenv configuration
    zshrc = Path.home() / ".zshrc"
    assert zshrc.exists()
    with open(zshrc) as f:
        content = f.read()
        assert "PYENV_ROOT" in content
        assert "pyenv init" in content
    
    # Verify Poetry configuration
    assert "poetry" in content
    assert str(mock_poetry_home) in content

def test_python_setup_with_existing_pyenv(
    mock_environment,
    mock_subprocess,
    mock_pyenv_root,
    mock_poetry_home
):
    """Test Python setup when pyenv is already installed."""
    # Mock pyenv as already installed
    mock_subprocess.return_value.stdout = b"3.11.0"
    
    # Run the setup
    setup_python()
    
    # Verify pyenv was not reinstalled
    assert not any("brew install pyenv" in cmd for cmd in mock_subprocess.call_args_list)

def test_python_setup_with_existing_poetry(
    mock_environment,
    mock_subprocess,
    mock_pyenv_root,
    mock_poetry_home
):
    """Test Python setup when Poetry is already installed."""
    # Mock Poetry as already installed
    mock_subprocess.return_value.stdout = b"Poetry version 1.4.2"
    
    # Run the setup
    setup_python()
    
    # Verify Poetry was not reinstalled
    assert not any("install.python-poetry.org" in cmd for cmd in mock_subprocess.call_args_list)

def test_python_setup_with_unsupported_shell(
    mock_environment,
    mock_subprocess,
    mock_pyenv_root,
    mock_poetry_home,
    monkeypatch
):
    """Test Python setup with an unsupported shell."""
    # Mock unsupported shell
    monkeypatch.setenv("SHELL", "/bin/fish")
    
    # Run the setup
    setup_python()
    
    # Verify appropriate error message
    assert "Unsupported shell" in mock_subprocess.call_args_list[-1][0][0]

def test_python_setup_with_missing_curl(
    mock_environment,
    mock_subprocess,
    mock_pyenv_root,
    mock_poetry_home,
    monkeypatch
):
    """Test Python setup when curl is not installed."""
    # Mock curl as not installed
    def mock_which(cmd):
        return "" if cmd == "curl" else f"/usr/local/bin/{cmd}"
    monkeypatch.setattr("shutil.which", mock_which)
    
    # Run the setup
    setup_python()
    
    # Verify appropriate error message
    assert "curl is not installed" in mock_subprocess.call_args_list[-1][0][0]

def test_python_setup_with_failed_pyenv_install(
    mock_environment,
    mock_subprocess,
    mock_pyenv_root,
    mock_poetry_home
):
    """Test Python setup when pyenv installation fails."""
    # Mock pyenv installation failure
    def mock_run(*args, **kwargs):
        if "brew install pyenv" in " ".join(args[0]):
            raise subprocess.CalledProcessError(1, args[0])
        return subprocess.CompletedProcess(args[0], 0)
    mock_subprocess.side_effect = mock_run
    
    # Run the setup
    with pytest.raises(subprocess.CalledProcessError):
        setup_python()

def test_python_setup_monitoring(
    mock_environment,
    mock_subprocess,
    mock_pyenv_root,
    mock_poetry_home
):
    """Test monitoring functionality during Python setup."""
    # Run the setup
    setup_python()
    
    # Get monitoring summary
    monitor = SetupMonitor()
    summary = monitor.get_summary()
    
    # Verify monitoring data
    assert summary["total_steps"] > 0
    assert summary["successful_steps"] > 0
    assert summary["failed_steps"] == 0
    
    # Verify step details
    steps = summary["steps"]
    assert any("platform_check" in step["name"] for step in steps)
    assert any("pyenv" in step["name"] for step in steps)
    assert any("poetry" in step["name"] for step in steps) 