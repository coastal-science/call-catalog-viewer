from pathlib import Path
import pytest
from src.add_remote_catalog import cli as add_remote_catalog

def test_add_cli_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Calling cli without arguments should exit and warn about missing arguments"""

    # arrange
    monkeypatch.chdir(tmp_path)

    # act
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_remote_catalog([""])

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0
    
def test_invalid_git_url(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    """Calling cli with an invalid git url"""
    
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_remote_catalog([
            "fake-git-url",
            "call-catalog.yaml"
        ])
        
    # assert
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0
    
def test_invalid_git_url(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Calling cli with an invalid yaml file. Will fail with argparser validation"""
    
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_remote_catalog([
            "real-git-url",
            "call-catalog.yaml"
        ])
        
    # assert
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0
    
def test_invalid_yaml_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Calling cli with an invalid yaml file. Will fail with argparser validation"""
    
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_remote_catalog([
            "real-git-url",
            "call-catalog.yaml"
        ])
        
    # assert
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0
