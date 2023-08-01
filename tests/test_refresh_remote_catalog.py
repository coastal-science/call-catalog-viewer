import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from os.path import exists, join
from src.refresh_remote_catalog import cli as refresh_remote_catalog
from testing_utils import dummy_remote_add, dummy_local_add, yaml
import logging
import json

TESTING_FIELD_DEFAULT = 0

VALID_GIT_NAME = 'catalog-versions-test'

def mock_change_testing_field(tmp_path: Path, remote_name: str, new_value: int):
    '''Update the call-catalog.yaml in the remote_name with the new value. Simulates a change in git'''
    with open(str(tmp_path) + '/' + remote_name + '/call-catalog.yaml', 'r+') as f:
        data = yaml.safe_load(f)
        data['site-details']['testing-field'] = new_value
        f.seek(0)
        yaml.dump(data, f)
    
    
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

def test_valid_git_repo(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Call without mocking remote call. Will use the repo in shared_datadir and make connection, but nothing to pull so no changes'''
    # arrange
    monkeypatch.chdir(tmp_path)
    caplog.set_level(logging.INFO)
    # don't need to remote add because we are already there in the shared_datadir
    
    # act
    EXIT_CODE = refresh_remote_catalog([
        VALID_GIT_NAME,
        '--path', str(shared_datadir) + '/catalogs'
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    assert f'Pulling remote changes from {VALID_GIT_NAME}...' in caplog.messages
    assert f'Successfully pulled all changes and {VALID_GIT_NAME} is up to date' in caplog.messages

def test_invalid_git_repo(tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Call without mocking the remote call will throw error for invalid git connection'''
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

@patch("src.refresh_remote_catalog.Repo")
def test_refresh_only_catalog(mock_repo, tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Add one remote catalog and refresh it. Assert changes were applied'''
    # arrage
    caplog.set_level(logging.INFO)
    
    mock_repo.return_value = MagicMock()
    mock_repo.git.checkout.return_value = None
    mock_repo.git.execute.return_value = None
    
    monkeypatch.chdir(tmp_path)
    remote_url, remote_name = 'fake-repo.git', 'fake-repo'
    dummy_remote_add(remote_url, remote_name, tmp_path, shared_datadir)
    
    # Mocking the change to [site-details][testing-value] in the yaml file as if the change was pulled from github
    # We are assuming that pull would be a success really checking the reconstruction of json files after the change is pulled
    mock_change_testing_field(tmp_path, remote_name, 5)
        
    EXIT_CODE = refresh_remote_catalog([
        remote_name,
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    assert f'Pulling remote changes from {remote_name}...' in caplog.messages
    assert f'Successfully pulled all changes and {remote_name} is up to date' in caplog.messages
    
    assert exists(join(tmp_path, remote_name, 'call-catalog.yaml'))
    assert exists(join(tmp_path, remote_name + '.json'))
        
    with open(join(tmp_path, remote_name + '.json'), 'r') as f:
        data = json.load(f)
        assert data['site-details']['testing-field'] == 5
        
@patch("src.refresh_remote_catalog.Repo")
def test_refresh_with_multiple_added(mock_repo, tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Add 2 remote catalogs. Call refresh on one of them. Assert it is updated and the othe ris not'''
    # arrange
    caplog.set_level(logging.INFO)
    
    mock_repo.return_value = MagicMock()
    mock_repo.git.checkout.return_value = None
    mock_repo.git.execute.return_value = None
    
    # arrange
    monkeypatch.chdir(tmp_path)
    remote_url, remote_name = 'fake-repo.git', 'fake-repo'
    second_remote_url, second_remote_name = 'second-fake-repo.git', 'second-fake-repo'
    dummy_remote_add(remote_url, remote_name, tmp_path, shared_datadir)
    dummy_remote_add(second_remote_url, second_remote_name, tmp_path, shared_datadir)
    
    # Mocking the change to [site-details][testing-value] in the yaml file as if the change was pulled from github
    # We are assuming that pull would be a success really checking the reconstruction of json files after the change is pulled
    mock_change_testing_field(tmp_path, remote_name, 5)
        
    EXIT_CODE = refresh_remote_catalog([
        remote_name,
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    assert f'Pulling remote changes from {remote_name}...' in caplog.messages
    assert f'Successfully pulled all changes and {remote_name} is up to date' in caplog.messages
    
    assert f'Pulling remote changes from {second_remote_name}...' not in caplog.messages
    assert f'Successfully pulled all changes and {second_remote_name} is up to date' not in caplog.messages
    
    assert exists(join(tmp_path, remote_name, 'call-catalog.yaml'))
    assert exists(join(tmp_path, remote_name + '.json'))
    
    assert exists(join(tmp_path, second_remote_name, 'call-catalog.yaml'))
    assert exists(join(tmp_path, second_remote_name + '.json'))
        
    # assert that one is updated and the other is not
    with open(join(tmp_path, second_remote_name + '.json'), 'r') as f:
        data = json.load(f)
        assert data['site-details']['testing-field'] == TESTING_FIELD_DEFAULT
        
    with open(join(tmp_path, remote_name + '.json'), 'r') as f:
        data = json.load(f)
        assert data['site-details']['testing-field'] == 5

@patch("src.refresh_remote_catalog.Repo")
def test_refresh_all(mock_repo, tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Add 2 remote catalogs and call refresh with --all. Assert that both catalogs were called'''
    # arrange
    caplog.set_level(logging.INFO)

    mock_repo.return_value = MagicMock()
    mock_repo.git.checkout.return_value = None
    mock_repo.git.execute.return_value = None
    
    monkeypatch.chdir(tmp_path)
    remote_url, remote_name = 'fake-repo.git', 'fake-repo'
    second_remote_url, second_remote_name = 'second-fake-repo.git', 'second-fake-repo'
    dummy_remote_add(remote_url, remote_name, tmp_path, shared_datadir)
    dummy_remote_add(second_remote_url, second_remote_name, tmp_path, shared_datadir)
    
    # Mocking the change to [site-details][testing-value] in the yaml file as if the change was pulled from github
    # We are assuming that pull would be a success really checking the reconstruction of json files after the change is pulled
    mock_change_testing_field(tmp_path, remote_name, 5)
    mock_change_testing_field(tmp_path, second_remote_name, 5)
        
    EXIT_CODE = refresh_remote_catalog([
        "--all",
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    # assert text in logger to make sure each one is actually called
    assert f'Pulling changes from {remote_name}...' in caplog.messages
    assert f'Successfully pulled changes from {remote_name}...' in caplog.messages
    assert f'Pulling changes from {second_remote_name}...' in caplog.messages
    assert f'Successfully pulled changes from {second_remote_name}...' in caplog.messages
    
    # assert file existence and content
    assert exists(join(tmp_path, remote_name, 'call-catalog.yaml'))
    assert exists(join(tmp_path, remote_name + '.json'))
    
    assert exists(join(tmp_path, second_remote_name, 'call-catalog.yaml'))
    assert exists(join(tmp_path, second_remote_name + '.json'))
        
    # assert that one is updated and the other is not
    with open(join(tmp_path, second_remote_name + '.json'), 'r') as f:
        data = json.load(f)
        assert data['site-details']['testing-field'] == 5
        
    with open(join(tmp_path, remote_name + '.json'), 'r') as f:
        data = json.load(f)
        assert data['site-details']['testing-field'] == 5
        
@patch("src.refresh_remote_catalog.Repo")
def test_refresh_all_with_locals(mock_repo, tmp_path: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    '''Add 2 remote catalogs and one local. When updating with --all ensure that it is called on both remote, but not the local'''
    # arrange
    caplog.set_level(logging.INFO)

    mock_repo.return_value = MagicMock()
    mock_repo.git.checkout.return_value = None
    mock_repo.git.execute.return_value = None
    
    monkeypatch.chdir(tmp_path)
    remote_url, remote_name = 'fake-repo.git', 'fake-repo'
    second_remote_url, second_remote_name = 'second-fake-repo.git', 'second-fake-repo'
    local_name = 'local-repo'
    dummy_remote_add(remote_url, remote_name, tmp_path, shared_datadir)
    dummy_remote_add(second_remote_url, second_remote_name, tmp_path, shared_datadir)
    dummy_local_add(local_name, tmp_path)
    
    # Mocking the change to [site-details][testing-value] in the yaml file as if the change was pulled from github
    # We are assuming that pull would be a success really checking the reconstruction of json files after the change is pulled
    mock_change_testing_field(tmp_path, remote_name, 5)
    mock_change_testing_field(tmp_path, second_remote_name, 5)
        
    EXIT_CODE = refresh_remote_catalog([
        "--all",
        "--path", str(tmp_path)
    ])
    
    # assert
    assert EXIT_CODE == 0
    
    # assert text in logger to make sure each one is actually called
    assert f'Pulling changes from {remote_name}...' in caplog.messages
    assert f'Successfully pulled changes from {remote_name}...' in caplog.messages
    assert f'Pulling changes from {second_remote_name}...' in caplog.messages
    assert f'Successfully pulled changes from {second_remote_name}...' in caplog.messages
    
    assert f'Pulling changes from {local_name}...' not in caplog.messages
    assert f'Successfully pulled changes from {local_name}...' not in caplog.messages


    
    # assert file existence and content
    assert exists(join(tmp_path, remote_name, 'call-catalog.yaml'))
    assert exists(join(tmp_path, remote_name + '.json'))
    
    assert exists(join(tmp_path, second_remote_name, 'call-catalog.yaml'))
    assert exists(join(tmp_path, second_remote_name + '.json'))
        
    # assert that one is updated and the other is not
    with open(join(tmp_path, second_remote_name + '.json'), 'r') as f:
        data = json.load(f)
        assert data['site-details']['testing-field'] == 5
        
    with open(join(tmp_path, remote_name + '.json'), 'r') as f:
        data = json.load(f)
        assert data['site-details']['testing-field'] == 5
