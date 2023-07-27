from src.catalog_versions import cli as catalog_versions
import pytest
import logging
from distutils.dir_util import copy_tree
from pathlib import Path


REAL_CATALOG_NAME = "catalog-versions-test"

def test_empty_cli(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    EXIT_CODE = catalog_versions([])
    
    assert EXIT_CODE != 0
    assert 'The name of the catalog must be specified' in caplog.messages
    
def test_catalog_does_not_exist(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange
    monkeypatch.chdir(tmp_path)
    not_real_catalog = "not-real-catalog"
    # act
    EXIT_CODE = catalog_versions([
        not_real_catalog,
        "--path", str(shared_datadir) + "/catalogs/"
    ])
    
    assert EXIT_CODE != 0
    assert f'The catalog {not_real_catalog} does not exist. Please enter a valid catalog name' in caplog.messages
    
def test_no_action_specified(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        "--path", str(shared_datadir) + '/catalogs/'
    ])
    
    # assert
    assert EXIT_CODE != 0
    assert 'Please specify the version or use --list or --latest' in caplog.messages

def test_specify_list_and_latest(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        "--list",
        "--latest",
        "--path", str(shared_datadir) + '/catalogs/'
    ])
    
    # assert
    assert EXIT_CODE != 0
    assert 'Please specify only one of catalog version, --list, or --latest' in caplog.messages

def tests_specify_version_and_list(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        "v1.0",
        "--list",
        "--path", str(shared_datadir) + "/catalogs/"
    ])
    
    # assert 
    assert EXIT_CODE != 0
    assert 'Please specify only one of catalog version, --list, or --latest'

def tests_specify_version_and_latest(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        "v1.0",
        "--latest",
        "--path", str(shared_datadir) + "/catalogs/"
    ])
    
    # assert 
    assert EXIT_CODE != 0
    assert 'Please specify only one of catalog version, --list, or --latest'
    
def test_list_tags(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange
    monkeypatch.chdir(tmp_path)
    caplog.set_level(logging.INFO)
    
    # act
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        "--list",
        "--path", str(shared_datadir) + "/catalogs/"
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    assert 'v1.0' in caplog.messages
    assert 'v2.0' in caplog.messages
    assert 'v3.0' in caplog.messages
    
def test_checkout_v1(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch):
    # arrange 
    monkeypatch.chdir(tmp_path)
    copy_tree(str(shared_datadir) + '/catalogs/', str(tmp_path) + '/catalogs/') # create our copy of the local repository so we don't mess it up with things
    
    
    # act
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        "v1.0",
        "--path", str(tmp_path) + "/catalogs/"
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    with open(str(tmp_path) + '/catalogs/catalog-versions-test/versions.txt', 'r') as f:
        assert f.readline() == '1'
        
def test_checkout_v2(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch):
    # arrange 
    monkeypatch.chdir(tmp_path)
    copy_tree(str(shared_datadir) + '/catalogs/', str(tmp_path) + '/catalogs/') # create our copy of the local repository so we don't mess it up with things
    
    
    # act
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        "v2.0",
        "--path", str(tmp_path) + "/catalogs/"
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    with open(str(tmp_path) + '/catalogs/catalog-versions-test/versions.txt', 'r') as f:
        assert f.readline() == '2'

def test_checkout_v3(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch):
    # arrange 
    monkeypatch.chdir(tmp_path)
    copy_tree(str(shared_datadir) + '/catalogs/', str(tmp_path) + '/catalogs/') # create our copy of the local repository so we don't mess it up with things
    
    
    # act
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        "v3.0",
        "--path", str(tmp_path) + "/catalogs/"
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    with open(str(tmp_path) + '/catalogs/catalog-versions-test/versions.txt', 'r') as f:
        assert f.readline() == '3'
        
def test_checkout_latest(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch):
    # arrange 
    monkeypatch.chdir(tmp_path)
    copy_tree(str(shared_datadir) + '/catalogs/', str(tmp_path) + '/catalogs/') # create our copy of the local repository so we don't mess it up with things
    
    
    # act
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        "--latest",
        "--path", str(tmp_path) + "/catalogs/"
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    with open(str(tmp_path) + '/catalogs/catalog-versions-test/versions.txt', 'r') as f:
        assert f.readline() == '3'
  
def test_checkout_multiple_versions_in_sequence(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch):
    # arrange 
    monkeypatch.chdir(tmp_path)
    copy_tree(str(shared_datadir) + '/catalogs/', str(tmp_path) + '/catalogs/') # create our copy of the local repository so we don't mess it up with things
    first_version = 'v3.0'
    second_version = 'v2.0'
    
    # act
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        first_version,
        "--path", str(tmp_path) + "/catalogs/"
    ])
    
    # assert
    assert EXIT_CODE == 0
    with open(str(tmp_path) + '/catalogs/catalog-versions-test/versions.txt', 'r') as f:
        assert f.readline() == '3'
    
    # Same everything, jus strying it again
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        second_version,
        "--path", str(tmp_path) + "/catalogs/"
    ])
    
    assert EXIT_CODE == 0
    with open(str(tmp_path) + '/catalogs/catalog-versions-test/versions.txt', 'r') as f:
        assert f.readline() == '2'

def test_checkout_version_then_latest(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch):
    # arrange 
    monkeypatch.chdir(tmp_path)
    copy_tree(str(shared_datadir) + '/catalogs/', str(tmp_path) + '/catalogs/') # create our copy of the local repository so we don't mess it up with things
    first_version = 'v1.0'
    
    # act
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        first_version,
        "--path", str(tmp_path) + "/catalogs/"
    ])
    
    # assert
    assert EXIT_CODE == 0
    with open(str(tmp_path) + '/catalogs/catalog-versions-test/versions.txt', 'r') as f:
        assert f.readline() == '1'
    
    # going back to latest
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        "--latest",
        "--path", str(tmp_path) + "/catalogs/"
    ])
    
    assert EXIT_CODE == 0
    with open(str(tmp_path) + '/catalogs/catalog-versions-test/versions.txt', 'r') as f:
        assert f.readline() == '3'

def test_checkout_invalid_tag(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange 
    monkeypatch.chdir(tmp_path)
    copy_tree(str(shared_datadir) + '/catalogs/', str(tmp_path) + '/catalogs/') # create our copy of the local repository so we don't mess it up with things
    invalid_version = '5.0'
    
    # act
    EXIT_CODE = catalog_versions([
        REAL_CATALOG_NAME,
        invalid_version,
        "--path", str(tmp_path) + "/catalogs/"
    ])
    
    # assert
    assert EXIT_CODE != 0
    assert f'The version {invalid_version} does not exist. To view available options use --list' in caplog.messages