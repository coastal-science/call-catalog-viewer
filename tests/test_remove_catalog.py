from pathlib import Path
import pytest
from src.remove_catalog import cli as remove_catalog
from src.utils import yaml
from tests.test_add_catalog import make_library, make_index, make_existing


def test_remove_cli_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Calling cli without arguments should exit and want about missing arguments"""
    
    # arrange
    monkeypatch.chdir(tmp_path)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        exit_code = remove_catalog()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0


def test_remove_from_uninitialized_library(tmp_path: Path, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch):
    """Attempt to remove a catalog from uninitialized index.yaml"""
    
    # arrange
    monkeypatch.chdir(tmp_path)

    # act
    print(f"{tmp_path=}")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        exit_code = remove_catalog(["nonexistent_catalog_name"])
    
    # assert
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0
    
    # cleanup
    # operations occur in the `tmp_path` folder,
    # which is unique to each invocation of the test function handled by `monkeypatch`


def test_remove_from_empty_library(tmp_path: Path, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch):
    """Attempt to remove a catalog from empty index.yaml"""
    
    # arrange
    print(f"{tmp_path=}")
    monkeypatch.chdir(tmp_path)
    # cleanup
    # operations occur in the `tmp_path` folder,
    # which is unique to each invocation of the test function.
