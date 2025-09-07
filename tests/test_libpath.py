import sys
import logging
from typing import Any
import subprocess
import os
from unittest.mock import patch

 # Mock the decky module before importing anything that uses it
class MockDecky:
    """Mock decky module for testing"""
    
    # Mock constants
    HOME = "/home/deck"
    USER = "deck"
    DECKY_VERSION = "v2.5.0"
    DECKY_USER = "deck"
    DECKY_USER_HOME = "/home/deck"
    DECKY_HOME = "/home/deck/homebrew"
    DECKY_PLUGIN_SETTINGS_DIR = "/home/deck/homebrew/settings/test-plugin"
    DECKY_PLUGIN_RUNTIME_DIR = "/home/deck/homebrew/data/test-plugin"
    DECKY_PLUGIN_LOG_DIR = "/home/deck/homebrew/logs/test-plugin"
    DECKY_PLUGIN_DIR = "/home/deck/homebrew/plugins/test-plugin"
    DECKY_PLUGIN_NAME = "Test Plugin"
    DECKY_PLUGIN_VERSION = "0.0.1"
    DECKY_PLUGIN_AUTHOR = "Test Author"
    DECKY_PLUGIN_LOG = "/home/deck/homebrew/logs/test-plugin/plugin.log"
    
    # Mock logger
    logger = logging.getLogger("decky")
    
    # Mock functions
    @staticmethod
    def migrate_any(target_dir: str, *files_or_directories: str) -> dict[str, str]:
        return {}
    
    @staticmethod
    def migrate_settings(*files_or_directories: str) -> dict[str, str]:
        return {}
    
    @staticmethod
    def migrate_runtime(*files_or_directories: str) -> dict[str, str]:
        return {}
    
    @staticmethod
    def migrate_logs(*files_or_directories: str) -> dict[str, str]:
        return {}
    
    @staticmethod
    async def emit(event: str, *args: Any) -> None:
        pass

sys.modules['decky'] = MockDecky

from main import Plugin
import pytest


@pytest.mark.asyncio
async def test_wifi_shell_script_execution_LD_LIBRARY_PATH_blank_exit_zero():
    """Test that demonstrates the readline symbol error with version mismatch"""
    # GIVEN
    plugin = Plugin()
    plugin.lock_script_path = "./lock_wifi.sh"
    plugin.unlock_script_path = "./unlock_wifi.sh"
    plugin.state_file_path = "/tmp/wifi_lock_state.json"
    
    # CREATE A MALICIOUS LIBRARY THAT WILL CAUSE THE SYMBOL ERROR
    malicious_lib_dir = "/tmp/malicious_lib"
    os.makedirs(malicious_lib_dir, exist_ok=True)

    subprocess.run([
        'cp', '/usr/lib/libformw.so.6', f'{malicious_lib_dir}/libreadline.so.8'
    ], check=True)
    
    # SIMULATE DECKY LOADER ENVIRONMENT
    bad_env = {
        "LD_LIBRARY_PATH": malicious_lib_dir,
        "PATH": os.environ.get('PATH', ''),
        **os.environ
    }
    original_run = subprocess.run
    def mock_subprocess_run(*args, **kwargs):
        kwargs['env'] = bad_env
        print(f"Running command: {args[0] if args else 'No args'}")
        print(f"With environment: {kwargs.get('env', {}).get('LD_LIBRARY_PATH', 'Not set')}")
        result = original_run(*args, **kwargs)
        print(f"Return code: {result.returncode}")
        print(f"STDERR: {result.stderr}")
        return result
    
    # WHEN
    with patch('subprocess.run', mock_subprocess_run):
        result = await plugin.lock_wifi()
        print(f"Final result: {result}")

    # THEN - Check for ANY readline symbol error (not just the specific one)
    error_occurred = (
        "undefined symbol: rl_trim_arg_from_keyseq" in result.get('message', '') or
        "undefined symbol: rl_copy_text" in result.get('message', '') or
        "undefined symbol: rl_" in result.get('message', '') or  # Catch any readline symbol
        "undefined symbol" in result.get('message', '') and "rl_" in result.get('message', '')
    )

    
    
    assert error_occurred, f"Expected a readline symbol error but got: {result}"