import pytest
from pathlib import Path
from src.refresh_remote_catalog import cli as refresh_remote_catalog
from testing_utils import dummy_remote_add, dummy_local_add

def test_refresh_cli_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    """Calling cli without arguments should fail and warn about missing arguments"""

    # arrange
    monkeypatch.chdir(tmp_path)

    # act
    EXIT_CODE = refresh_remote_catalog([""])

    assert EXIT_CODE != 0
    assert 'Please specify a catalog name, or use the --all flag to update all catalogs' in caplog.messages
    
def test_refresh_no_remote_catalogs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Calling with no remote catalogs added, will fail not work properly'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    EXIT_CODE = refresh_remote_catalog([
        "dummy-catalog-name",
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE != 0
    assert 'No remote catalogs are added. Please add one before updating.' in caplog.messages

def test_refresh_remote_catalog_not_exist(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Adding a remote catalog so library.yaml exists, but passing invalid catalog name'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    dummy_remote_add("fake-repo.git", "fake-repo", tmp_path, shared_datadir)
    fake_name = "dummy-catalog-name"
    
    # act
    EXIT_CODE = refresh_remote_catalog([
        fake_name,
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE != 0
    assert f'The catalog {fake_name} does not exist. Please add it before updating' in caplog.messages

def test_refresh_local_catalog(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Adding a remote and local catalog in setup, attempting to refresh the local'''
    # arrange
    monkeypatch.chdir(tmp_path)
    remote_url, remote_name = 'fake-repo.git', 'fake-repo'
    local_name = 'local-repo'
    dummy_remote_add(remote_url, remote_name, tmp_path, shared_datadir)
    dummy_local_add(local_name, tmp_path)  
      
    # act
    EXIT_CODE = refresh_remote_catalog([
        local_name,
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE != 0
    assert f'The catalog {local_name} is not a remote catalog' in caplog.messages
    
def test_invalid_git_repo(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange
    monkeypatch.chdir(tmp_path)
    remote_url, remote_name = 'fake-repo.git', 'fake-repo'
    dummy_remote_add(remote_url, remote_name, tmp_path, shared_datadir)
    
    # act
    EXIT_CODE = refresh_remote_catalog([
        remote_name,
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE != 0
    assert f'There was a problem pulling the changes for repo {remote_name}' in caplog.messages
