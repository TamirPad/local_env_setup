import pytest
from pathlib import Path
import platform
from local_env_setup.core.base import BaseSetup

class TestBaseSetup(BaseSetup):
    """Test implementation of BaseSetup for testing purposes."""
    def run(self) -> bool:
        return True

@pytest.fixture
def base_setup():
    return TestBaseSetup()

def test_initialization(base_setup):
    """Test that the base setup initializes correctly."""
    assert base_setup.system == platform.system()
    assert base_setup.is_macos == (platform.system() == "Darwin")
    assert base_setup.rollback_steps == []
    assert base_setup.logger is not None
    assert base_setup.monitor is not None

def test_check_platform(base_setup):
    """Test platform checking functionality."""
    result = base_setup.check_platform()
    if platform.system() == "Darwin":
        assert result is True
    else:
        assert result is False

def test_is_command_available(base_setup):
    """Test command availability checking."""
    # Test with a command that should exist
    assert base_setup.is_command_available("ls") is True
    # Test with a command that should not exist
    assert base_setup.is_command_available("nonexistentcommand123") is False

def test_create_directory(base_setup, tmp_path):
    """Test directory creation functionality."""
    test_dir = tmp_path / "test_dir"
    assert base_setup.create_directory(test_dir) is True
    assert test_dir.exists() and test_dir.is_dir()
    
    # Test creating a directory that already exists
    assert base_setup.create_directory(test_dir) is True

def test_append_to_file(base_setup, tmp_path):
    """Test file appending functionality."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("initial content\n")
    
    # Test appending content
    assert base_setup.append_to_file(test_file, "new content\n") is True
    assert test_file.read_text() == "initial content\nnew content\n"
    
    # Test appending to non-existent file (should create it)
    non_existent_file = tmp_path / "nonexistent.txt"
    assert base_setup.append_to_file(non_existent_file, "content") is True
    assert non_existent_file.exists()
    assert non_existent_file.read_text() == "content"

def test_rollback(base_setup, tmp_path):
    """Test rollback functionality."""
    test_file = tmp_path / "test.txt"
    original_content = "original content\n"
    test_file.write_text(original_content)
    
    # Add a rollback step for file content
    base_setup.add_rollback_step({
        "function": lambda p, c: Path(p).write_text(c) if c else Path(p).unlink(),
        "args": [str(test_file), original_content]
    })
    
    # Modify the file
    test_file.write_text("modified content\n")
    
    # Perform rollback
    base_setup.rollback()
    
    # Verify rollback restored original content
    assert test_file.read_text() == original_content 