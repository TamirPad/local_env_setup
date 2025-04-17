import pytest
from unittest.mock import patch, MagicMock
import subprocess
from pathlib import Path
from src.local_env_setup.setup.dev_tools.python import PythonSetup

class TestPythonSetup:
    """Test suite for PythonSetup class."""
    
    @pytest.fixture
    def python_setup(self):
        """Create a test instance of PythonSetup."""
        return PythonSetup()
    
    @patch('platform.system')
    def test_check_platform_macos(self, mock_system, python_setup):
        """Test platform check for macOS."""
        mock_system.return_value = 'Darwin'
        python_setup.system = 'Darwin'
        python_setup.is_macos = True
        assert python_setup.check_platform() is True
    
    @patch('platform.system')
    def test_check_platform_non_macos(self, mock_system, python_setup):
        """Test platform check for non-macOS."""
        mock_system.return_value = 'Linux'
        python_setup.system = 'Linux'
        python_setup.is_macos = False
        assert python_setup.check_platform() is False
    
    @patch('shutil.which')
    def test_check_prerequisites_brew_installed(self, mock_which, python_setup):
        """Test prerequisites check when Homebrew is installed."""
        mock_which.return_value = '/usr/local/bin/brew'
        assert python_setup.check_prerequisites() is True
    
    @patch('shutil.which')
    def test_check_prerequisites_brew_not_installed(self, mock_which, python_setup):
        """Test prerequisites check when Homebrew is not installed."""
        mock_which.return_value = None
        assert python_setup.check_prerequisites() is False
    
    @patch('subprocess.run')
    def test_install_success(self, mock_run, python_setup):
        """Test successful Python installation."""
        mock_run.return_value = subprocess.CompletedProcess(['brew', 'install', 'python'], 0)
        assert python_setup.install() is True
    
    @patch('subprocess.run')
    def test_install_failure(self, mock_run, python_setup):
        """Test failed Python installation."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ['brew', 'install', 'python'])
        assert python_setup.install() is False
    
    @patch('subprocess.run')
    def test_configure_success(self, mock_run, python_setup):
        """Test successful Python configuration."""
        mock_run.return_value = subprocess.CompletedProcess(['pip', 'install', '--upgrade', 'pip'], 0)
        assert python_setup.configure() is True
    
    @patch('subprocess.run')
    def test_configure_failure(self, mock_run, python_setup):
        """Test failed Python configuration."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ['pip', 'install', '--upgrade', 'pip'])
        assert python_setup.configure() is False
    
    @patch('subprocess.run')
    def test_verify_success(self, mock_run, python_setup):
        """Test successful Python verification."""
        mock_run.return_value = subprocess.CompletedProcess(['python', '--version'], 0, stdout=b'Python 3.11.0')
        assert python_setup.verify() is True
    
    @patch('subprocess.run')
    def test_verify_failure(self, mock_run, python_setup):
        """Test failed Python verification."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ['python', '--version'])
        assert python_setup.verify() is False
    
    @patch('subprocess.run')
    def test_run_success(self, mock_run, python_setup):
        """Test successful Python setup run."""
        # Set up the platform check
        python_setup.system = 'Darwin'
        python_setup.is_macos = True
        
        # Set up the mock return values
        mock_run.side_effect = [
            # check_prerequisites - brew
            subprocess.CompletedProcess(['which', 'brew'], 0, stdout=b'', stderr=b''),
            # check_prerequisites - curl
            subprocess.CompletedProcess(['which', 'curl'], 0, stdout=b'', stderr=b''),
            # install - check pyenv
            subprocess.CompletedProcess(['which', 'pyenv'], 1, stdout=b'', stderr=b''),
            # install - install pyenv
            subprocess.CompletedProcess(['brew', 'install', 'pyenv'], 0, stdout=b'', stderr=b''),
            # install - source shell rc
            subprocess.CompletedProcess(['source', '/Users/tamirpadlad/.zshrc'], 0, stdout=b'', stderr=b''),
            # install - check python version
            subprocess.CompletedProcess(['pyenv', 'versions'], 0, stdout=b'3.11.0', stderr=b''),
            # configure - set global python version
            subprocess.CompletedProcess(['pyenv', 'global', '3.11.0'], 0, stdout=b'', stderr=b''),
            # verify - check python version
            subprocess.CompletedProcess(['pyenv', 'version'], 0, stdout=b'3.11.0 (set by /Users/tamirpadlad/.pyenv/version)', stderr=b'')
        ]
        assert python_setup.run() is True
    
    @patch('subprocess.run')
    def test_run_install_failure(self, mock_run, python_setup):
        """Test Python setup run with installation failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, ['brew', 'install', 'python'])
        assert python_setup.run() is False
    
    @patch('subprocess.run')
    def test_run_configure_failure(self, mock_run, python_setup):
        """Test Python setup run with configuration failure."""
        mock_run.side_effect = [
            subprocess.CompletedProcess(['brew', 'install', 'python'], 0),
            subprocess.CalledProcessError(1, ['pip', 'install', '--upgrade', 'pip'])
        ]
        assert python_setup.run() is False
    
    @patch('subprocess.run')
    def test_run_verify_failure(self, mock_run, python_setup):
        """Test Python setup run with verification failure."""
        mock_run.side_effect = [
            subprocess.CompletedProcess(['brew', 'install', 'python'], 0),
            subprocess.CompletedProcess(['pip', 'install', '--upgrade', 'pip'], 0),
            subprocess.CalledProcessError(1, ['python', '--version'])
        ]
        assert python_setup.run() is False 