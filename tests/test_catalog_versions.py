from src.catalog_versions import cli as catalog_versions
import pytest
import logging

from pathlib import Path

def test_empty_cli(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
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
    
def test_list_tags(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    # arrange
    monkeypatch.chdir(tmp_path)
    caplog.set_level(logging.INFO)
    
    # act
    EXIT_CODE = catalog_versions([
        "catalog-versions-test",
        "--list",
        "--path", str(shared_datadir) + "/catalogs/"
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    assert 'v1.0' in caplog.messages
    assert 'v2.0' in caplog.messages
    assert 'v3.0' in caplog.messages
    