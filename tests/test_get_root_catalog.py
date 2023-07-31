from src.get_root_catalog import cli as get_root_catalog
from src.set_root_catalog import cli as set_root_catalog

from testing_utils import dummy_local_add, dummy_remote_add
import pytest
import logging
from pathlib import Path

def test_no_catalogs_added(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''No catalogs are added when calling get root'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    EXIT_CODE = get_root_catalog([
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE != 0
    assert 'No remote catalogs have been added to the viewer. One must be added to have a root catalog.' in caplog.text

def test_only_local_catalog(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''No remote catalogs are present, just a local one'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    local_catalog = "local-catalog"
    dummy_local_add(local_catalog, tmp_path)
    
    # act
    EXIT_CODE = get_root_catalog([
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE != 0
    assert 'No remote catalogs have been added to the viewer. One must be added to have a root catalog.' in caplog.text

def test_single_remote_catalog(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Calling with a single root remote catalog'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    root_catalog_name, root_catalog_url = "root-catalog", "root-catalog.git"
    dummy_remote_add(root_catalog_url, root_catalog_name, tmp_path, shared_datadir)
    caplog.set_level(logging.INFO)

    
    # act
    EXIT_CODE = get_root_catalog([
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE == 0
    assert f'{root_catalog_name} is the root catalog' in caplog.text
    
def test_multiple_remote_catalogs(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Calling when multiple remote catalogs are added'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    
    root_catalog_name, root_catalog_url = "root-catalog", "root-catalog.git"
    dummy_remote_add(root_catalog_url, root_catalog_name, tmp_path, shared_datadir)
    
    non_root_name, non_root_url = "non-root", "non-root.git"
    dummy_remote_add(non_root_url, non_root_name, tmp_path, shared_datadir)
    
    caplog.set_level(logging.INFO)
    
    # act
    EXIT_CODE = get_root_catalog([
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE == 0
    assert f'{root_catalog_name} is the root catalog' in caplog.text
    
def test_remote_and_local_catalogs(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Calling when multiple remote catalogs are added'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    
    root_catalog_name, root_catalog_url = "root-catalog", "root-catalog.git"
    dummy_remote_add(root_catalog_url, root_catalog_name, tmp_path, shared_datadir)
    
    local_name = "local-catalogue"
    dummy_local_add(local_name, tmp_path)
    
    caplog.set_level(logging.INFO)
    
    # act
    EXIT_CODE = get_root_catalog([
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE == 0
    assert f'{root_catalog_name} is the root catalog' in caplog.text
    
def test_set_new_root_catalog(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Calling when multiple remote catalogs are added'''
    
    # arrange
    monkeypatch.chdir(tmp_path)
    
    first_root_name, first_root_url = "root-catalog", "root-catalog.git"
    dummy_remote_add(first_root_url, first_root_name, tmp_path, shared_datadir)
    
    second_root_name, second_root_url = "second-root", "second-root.git"
    dummy_remote_add(second_root_url, second_root_name, tmp_path, shared_datadir)
    
    caplog.set_level(logging.INFO)
    
    # act
    EXIT_CODE = get_root_catalog([
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE == 0
    assert f'{first_root_name} is the root catalog' in caplog.text
    
    # arrange changed root catalog
    set_root_catalog([
        second_root_name, 
        "--path", str(tmp_path)
    ])
    
    # act
    EXIT_CODE = get_root_catalog([
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE == 0
    assert f'{second_root_name} is the root catalog' in caplog.text