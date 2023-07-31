from src.set_root_catalog import cli as set_root_catalog
from testing_utils import dummy_local_add, dummy_remote_add

from os.path import exists, join
import pytest
import json
import logging
from pathlib import Path

def test_empty_cli(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Call set_root_catalog with on argument'''
    # arrange
    monkeypatch.chdir(tmp_path)

    EXIT_CODE = set_root_catalog([""])

    assert EXIT_CODE != 0
    assert 'Please enter a non-empty catalog name' in caplog.text

def test_catalog_does_not_exist(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    ''''Call with a catalog name that is not added'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    repo_name = 'not-real'
    
    # act
    EXIT_CODE = set_root_catalog([
        repo_name,
        '--path', str(tmp_path)
        ])
    
    assert EXIT_CODE != 0
    assert f'The repo {repo_name} does not exist, cannot set it as root catalog.' in caplog.text

def test_catalog_already_root(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Try to set the current root as the new root'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    root_catalog, root_catalog_url = 'root-catalog', 'root-catalog.git'
    dummy_remote_add(root_catalog_url, root_catalog, tmp_path, shared_datadir)
    
    # act
    EXIT_CODE = set_root_catalog([
        root_catalog,
        '--path', str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE != 0
    assert f'The repo {root_catalog} is already the root catalog. Doing nothing' in caplog.text

def test_set_local_no_remote_added(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Add a local catalog and try to set that as the remote'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    local_catalog_name = 'local-catalogue'
    dummy_local_add(local_catalog_name, tmp_path)
    
    # act
    EXIT_CODE = set_root_catalog([
        local_catalog_name,
        '--path', str(tmp_path)
    ])
    
    assert EXIT_CODE != 0
    assert f'The local catalog {local_catalog_name} is not a remote catalog. Cannot be set as the root catalog' in caplog.text
    
def test_set_local_remote_added(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Try to set the new root catalog as a locally added one with existing remote added'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    
    local_catalog_name = 'local-catalogue'
    dummy_local_add(local_catalog_name, tmp_path)
    
    remote_catalog_name, remote_catalog_url = 'remote-catalog', 'remote-catalog.git'
    dummy_remote_add(remote_catalog_url, remote_catalog_name, tmp_path, shared_datadir)
    
    # act
    EXIT_CODE = set_root_catalog([
        local_catalog_name,
        '--path', str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE != 0
    assert f'The local catalog {local_catalog_name} is not a remote catalog. Cannot be set as the root catalog' in caplog.text

def test_set_root_valid(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Add two remote repos and set the non-root to the root'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    caplog.set_level(logging.INFO)
    
    root_catalog_name, root_catalog_url = 'root-catalog', 'root-catalg.git'
    dummy_remote_add(root_catalog_url, root_catalog_name, tmp_path, shared_datadir)
    
    new_root_catalog_name, new_root_catalog_url = 'new-root-catalog', 'new-root-catalog.git'
    dummy_remote_add(new_root_catalog_url, new_root_catalog_name, tmp_path, shared_datadir)
    
    # act
    EXIT_CODE = set_root_catalog([
        new_root_catalog_name,
        '--path', str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    assert exists(join(tmp_path, new_root_catalog_name, 'library.yaml'))
    assert exists(join(tmp_path, 'library.yaml'))
    assert not exists(join(tmp_path, root_catalog_name, 'library.yaml'))
    
    # check our json files
    assert exists(join(tmp_path, root_catalog_name + '.json'))
    assert exists(join(tmp_path, new_root_catalog_name + '.json'))
    
    with open(join(tmp_path, root_catalog_name + '.json'), 'r') as f:
        data = json.load(f)
        assert data['site-details']['catalogue']['is_root'] == 'false'
        
    with open(join(tmp_path, new_root_catalog_name + '.json'), 'r') as f:
        data = json.load(f)
        assert data['site-details']['catalogue']['is_root'] == 'true'

    assert f'Successfully set {new_root_catalog_name} as new root catalog' in caplog.text