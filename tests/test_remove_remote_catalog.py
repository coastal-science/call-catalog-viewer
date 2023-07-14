from src.remove_remote_catalog import cli as remove_remote_catalog
from test_add_remote_catalog import dummy_local_add, dummy_remote_add
import pytest
from pathlib import Path
from os.path import exists, join

def test_add_cli_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    """Calling cli without arguments should exit and warn about missing arguments"""

    # arrange
    monkeypatch.chdir(tmp_path)

    # act
    EXIT_CODE = remove_remote_catalog([""])
    
    assert EXIT_CODE != 0
    assert "Please input a valid repo name to remove" in caplog.text
    
def test_remove_catalog_not_exist(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
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
    assert f'Could not find repo {repo_name} in library.yaml' in caplog.text

def test_remove_local_catalog(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    """Attempting to remove a local catalog with remove_remote_catalog"""
    
    # arrange 
    monkeypatch.chdir(tmp_path)
    
    local_repo_name = "local-catalogue"
    dummy_local_add(local_repo_name, tmp_path)
    
    # act
    EXIT_CODE = remove_remote_catalog([
        local_repo_name,
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE != 0
    assert 'Library.yaml does not exist. Please add a remote catalog before removing' in caplog.text
    
def test_remove_root_no_force(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    """Attempting to remove a root catalog with no --force"""
    
    # arrange
    monkeypatch.chdir(tmp_path)
    remote_url, remote_name = "test-whales.git", "test-whales" # Notes: the name must be in the url
    dummy_remote_add(remote_url, remote_name, tmp_path)
    
    # act
    EXIT_CODE = remove_remote_catalog([
        remote_name,
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE != 0
    
    assert exists(join(tmp_path, 'index.yaml'))
    assert exists(join(tmp_path, 'library.yaml'))
    assert exists(join(tmp_path, remote_name + '.json'))
    assert exists(join(tmp_path, remote_name, '/'))
    
    assert 'Attempting to remove root catalog' in caplog.text

def test_remove_root_force(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange 
    monkeypatch.chdir(tmp_path)
    
    remote_url, remote_name = "test-whales.git", "test-whales"
    dummy_remote_add(remote_url, remote_name, tmp_path)
    
    # act
    EXIT_CODE = remove_remote_catalog([
        remote_name,
        "--path", str(tmp_path),
        "--force"
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    assert not exists(join(tmp_path, 'index.yaml'))
    assert not exists(join(tmp_path, 'library.yaml'))
    assert not exists(join(tmp_path, remote_name + '.json'))
    assert not exists(join(tmp_path, remote_name))
    
def test_remove_root_not_last_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange
    monkeypatch.chdir(tmp_path)
    # remote_1 will be the root as it is added first
    remote_url_1, remote_name_1 = "test-whales.git", "test-whales" # Note: the name must be in the url
    remote_url_2, remote_name_2 = "fake-whales.git", "fake-whales" # Note: the name must be in the url
    dummy_remote_add(remote_url_1, remote_name_1, tmp_path)
    dummy_remote_add(remote_url_2, remote_name_2, tmp_path)
    
    # act
    EXIT_CODE = remove_remote_catalog([
        remote_name_1,
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE != 0
    
    assert exists(join(tmp_path, 'index.yaml'))
    assert exists(join(tmp_path, 'library.yaml'))
    assert exists(join(tmp_path, remote_name_1 + '.json'))
    assert exists(join(tmp_path, remote_name_1))
    
    assert 'Attempting to remove root catalog' in caplog.text

def test_remove_root_not_last_file_force(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange
    monkeypatch.chdir(tmp_path)
    # remote_1 will be the root as it is added first
    remote_url_1, remote_name_1 = "test-whales.git", "test-whales" # Note: the name must be in the url
    remote_url_2, remote_name_2 = "fake-whales.git", "fake-whales" # Note: the name must be in the url
    dummy_remote_add(remote_url_1, remote_name_1, tmp_path)
    dummy_remote_add(remote_url_2, remote_name_2, tmp_path)
    
    # act
    EXIT_CODE = remove_remote_catalog([
        remote_name_1,
        "--path", str(tmp_path), 
        "--force"
    ])
    
    # assert
    assert EXIT_CODE != 0
    
    assert exists(join(tmp_path, 'index.yaml'))
    assert exists(join(tmp_path, 'library.yaml'))
    assert exists(join(tmp_path, remote_name_1 + '.json'))
    assert exists(join(tmp_path, remote_name_1, '/'))
    
    assert f'Cannot remove the root catalog {remote_name_1} while other catalogs are in the viewer.' in caplog.text
    
"""
Test Cases
- Try to remove a local catalog
- Remove a non root remote catalog
- Try to remove a root catalog
- Try to rmeove a root catalog with --force
- Successfully remote a root catalog with --force

"""