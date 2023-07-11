from pathlib import Path
import pytest
from os.path import join, exists
from src.utils import yaml
from src.add_remote_catalog import cli as add_remote_catalog

# variables used repeatedly throughout testing
VALID_GIT_SSH = 'git@github.com:EvanDyce/test-catalogue.git'
VALID_GIT_HTTPS = 'https://@github.com/EvanDyce/test-catalogue.git'
VALID_REPO_NAME = 'test-catalogue'
VALID_YAML_FILE = 'call-data.yaml'

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
            "real-git-url.git",
            "call-catalog.fake"
        ])
        
    # assert
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0

def test_ssh_yaml_not_exist(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    """Calling cli with a valid ssh git url and a valid yaml filename that is not in repo"""
    # arrange
    monkeypatch.chdir(tmp_path)
    fake_yaml = 'fake-data.yaml'
    
    # act
    exit_code = add_remote_catalog([
        VALID_GIT_SSH,
        fake_yaml,
        '--path', str(tmp_path)
    ])
    
    # assert
    assert exit_code != 0
    assert f'The yaml file {fake_yaml} does not exist in {VALID_REPO_NAME}' in caplog.text
    
def test_https_yaml_not_exist(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    """Calling cli with a valid https git url and a valid yaml filename that is not in repo"""
    # arrange
    monkeypatch.chdir(tmp_path)
    fake_yaml = 'fake-data.yaml'
    
    # act
    exit_code = add_remote_catalog([
        VALID_GIT_HTTPS,
        fake_yaml,
        '--path', str(tmp_path)
    ])
    
    # assert
    assert exit_code != 0
    assert f'The yaml file {fake_yaml} does not exist in {VALID_REPO_NAME}' in caplog.text
    
def test_ssh_yaml_exists(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Adding first catalog with valid arguments. Validate correct file creation"""
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    exit_code = add_remote_catalog([
        VALID_GIT_SSH,
        VALID_YAML_FILE,
        '--path', str(tmp_path)
    ])
    
    # assert program ran successfully
    assert exit_code == 0
    
    # assert files created
    index_file = join(tmp_path, 'index.yaml')
    library_file = join(tmp_path, 'library.yaml')
    
    assert exists(index_file)
    assert exists(library_file)
    assert exists(join(tmp_path, VALID_REPO_NAME + '.json'))
    assert exists(join(tmp_path, VALID_REPO_NAME))
    
    # assert the content of files
    with open(index_file) as index:
        content = yaml.safe_load(index)
        assert VALID_REPO_NAME in content['catalogs']
        
    with open(library_file) as library:
        content = yaml.safe_load(library)
        assert VALID_GIT_SSH in content['catalogs']
    
# TODO: Issue with https clone because of lack of credentials. When run standalone will prompt 
# for authentication credentials, but as a test just fails
@pytest.mark.skip
def test_https_yaml_exists(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Adding first catalog with valid arguments. Validate correct file creation"""
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    exit_code = add_remote_catalog([
        VALID_GIT_HTTPS,
        VALID_YAML_FILE,
        '--path', str(tmp_path)
    ])
    
    # assert program ran successfully
    assert exit_code == 0
    
    # assert files created
    index_file = join(tmp_path, 'index.yaml')
    library_file = join(tmp_path, 'library.yaml')
    
    assert exists(index_file)
    assert exists(library_file)
    assert exists(join(tmp_path, VALID_REPO_NAME + '.json'))
    assert exists(join(tmp_path, VALID_REPO_NAME))
    
    # assert the content of files
    with open(index_file) as index:
        content = yaml.safe_load(index)
        assert VALID_REPO_NAME in content['catalogs']
        
    with open(library_file) as library:
        content = yaml.safe_load(library)
        assert VALID_GIT_HTTPS in content['catalogs']