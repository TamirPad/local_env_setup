import pytest
from unittest.mock import patch, MagicMock
import subprocess
import platform
from pathlib import Path
from src.local_env_setup.core.base import BaseSetup

class TestBaseSetupImpl(BaseSetup):
    """Concrete implementation of BaseSetup for testing."""
    
    def run(self):
        """Test implementation of abstract run method."""
        pass

class TestBaseSetup:
    """Test suite for BaseSetup class."""
    
    @pytest.fixture
    def base_setup(self):
        """Create a test instance of BaseSetup."""
        return TestBaseSetupImpl()
    
    @patch('platform.system')
    def test_check_platform_macos(self, mock_system, base_setup):
        """Test platform check for macOS."""
        mock_system.return_value = 'Darwin'
        assert base_setup.check_platform() is True
    
    @patch('platform.system')
    def test_check_platform_non_macos(self, mock_system, base_setup):
        """Test platform check for non-macOS."""
        mock_system.return_value = 'Linux'
        assert base_setup.check_platform() is False
    
    @patch('shutil.which')
    def test_is_command_available_true(self, mock_which, base_setup):
        """Test command availability check when command exists."""
        mock_which.return_value = '/usr/bin/command'
        assert base_setup.is_command_available('command') is True
    
    @patch('shutil.which')
    def test_is_command_available_false(self, mock_which, base_setup):
        """Test command availability check when command doesn't exist."""
        mock_which.return_value = None
        assert base_setup.is_command_available('command') is False
    
    @patch('subprocess.run')
    def test_run_command_success(self, mock_run, base_setup):
        """Test successful command execution."""
        mock_run.return_value = subprocess.CompletedProcess(['command'], 0)
        result = base_setup.run_command(['command'])
        assert result is True
    
    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run, base_setup):
        """Test failed command execution."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ['command'])
        result = base_setup.run_command(['command'])
        assert result is False
    
    @patch('subprocess.run')
    def test_get_command_output_success(self, mock_run, base_setup):
        """Test successful command output capture."""
        mock_run.return_value = subprocess.CompletedProcess(['command'], 0, stdout=b'output')
        result = base_setup.get_command_output(['command'])
        assert result == 'output'
    
    @patch('subprocess.run')
    def test_get_command_output_failure(self, mock_run, base_setup):
        """Test failed command output capture."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ['command'])
        result = base_setup.get_command_output(['command'])
        assert result is None
    
    @patch('pathlib.Path.mkdir')
    def test_create_directory_success(self, mock_mkdir, base_setup):
        """Test successful directory creation."""
        mock_mkdir.return_value = None
        result = base_setup.create_directory(Path('/test/dir'))
        assert result is True
    
    @patch('pathlib.Path.mkdir')
    def test_create_directory_failure(self, mock_mkdir, base_setup):
        """Test failed directory creation."""
        mock_mkdir.side_effect = OSError()
        result = base_setup.create_directory(Path('/test/dir'))
        assert result is False
    
    @patch('pathlib.Path.write_text')
    def test_append_to_file_success(self, mock_write, base_setup):
        """Test successful file append."""
        mock_write.return_value = None
        result = base_setup.append_to_file(Path('/test/file'), 'content')
        assert result is True
    
    @patch('pathlib.Path.write_text')
    def test_append_to_file_failure(self, mock_write, base_setup):
        """Test failed file append."""
        mock_write.side_effect = OSError()
        result = base_setup.append_to_file(Path('/test/file'), 'content')
        assert result is False 