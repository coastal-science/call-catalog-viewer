from src.remove_remote_catalog import cli as remove_remote_catalog
from test_add_remote_catalog import dummy_local_add, dummy_remote_add
import pytest
from pathlib import Path

def test_add_cli_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Calling cli without arguments should exit and warn about missing arguments"""

    # arrange
    monkeypatch.chdir(tmp_path)

    # act
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        remove_remote_catalog([""])

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0
    
def test_catalog_name_not_exist(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    """Calling cli with empty catalog set up for a name that doesn't exist"""

    # arrange
    monkeypatch.chdir(tmp_path)
    dummy_remote_add("fake.git", "catalog", tmp_path)
    repo_name = "catalog-not-there"

    # act
    EXIT_CODE = remove_remote_catalog([
                    repo_name,
                    "--path", str(tmp_path)
                ])

    # assert
    assert EXIT_CODE != 0
    assert f'Catalog {repo_name} not in' in caplog.text