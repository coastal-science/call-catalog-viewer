from pathlib import Path
import pytest
from os.path import join, exists
from os import mkdir, symlink
from src.utils import yaml
from src.add_remote_catalog import cli as add_remote_catalog

# variables used repeatedly throughout testing
VALID_GIT_SSH = 'git@github.com:EvanDyce/test-catalogue.git'
VALID_GIT_HTTPS = 'https://@github.com/EvanDyce/test-catalogue.git'
VALID_REPO_NAME = 'test-catalogue'
VALID_YAML_FILE = 'call-data.yaml'

###### UTIL FUNCTIONS
def make_or_append_yaml(path: Path, value: str):
    """path to the yaml file to append to and the value to add to it"""
    with open(join(path), 'a+') as f:
        catalogs = yaml.safe_load(f) if yaml.safe_load(f) is not None else {'catalogs': []}
        catalogs['catalogs'].append(value)
        f.seek(0)
        yaml.dump(catalogs, f)
        
def dummy_remote_add(catalog_url: str, catalog_name: str, path: Path):    
    # create the directory we need
    mkdir(join(path, catalog_name))
    
    # add our data to yaml and then create a symlink
    make_or_append_yaml(join(path, catalog_name, 'library.yaml'), catalog_url)
    make_or_append_yaml(join(path, 'index.yaml'), catalog_name)
    symlink(join(path, catalog_name, 'library.yaml'), join(path, 'library.yaml'))
            
    # create the json file
    with open(join(path, catalog_name + '.json'), 'a') as f:
        f.write('dummy data for testing')

def dummy_local_add(catalog_name: str, path: Path):
    # need to append index.yaml if it is there, create repo_name directory and json file
    mkdir(join(path, catalog_name))
    
    # create index.yaml and {catalog_name}.json
    make_or_append_yaml(join(path, 'index.yaml'), catalog_name)
    
    with open(join(path, catalog_name + '.json'), 'a') as f:
        f.write('dummy data for testing')

def test_add_cli_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Calling cli without arguments should exit and warn about missing arguments"""

    # arrange
    monkeypatch.chdir(tmp_path)

    # act
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_remote_catalog([""])

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0
    
def test_invalid_git_url_format(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    """Calling cli with an invalid git url"""
    
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_remote_catalog([
            "fake-git-url",
            VALID_YAML_FILE
        ])
        
    # assert
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0
    
def test_invalid_yaml_file_format(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Calling cli with an invalid yaml file. Will fail with argparser validation"""
    
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # act
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_remote_catalog([
            VALID_GIT_SSH,
            "call-data.fake"
        ])
        
    # assert
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0

def test_yaml_not_exist(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
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
    
@pytest.mark.skip
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
    
def test_yaml_exists(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
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
    
def test_add_same_catalog_twice(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture):
    """Adding same catalog twice should succeed the first time and fail the second"""
    
    # arrange
    monkeypatch.chdir(tmp_path)
    
    # create our 'existing' entry with same data
    dummy_remote_add(VALID_GIT_SSH, VALID_REPO_NAME, tmp_path)
    
    # act 
    EXIT_CODE = add_remote_catalog([
        VALID_GIT_SSH,
        VALID_YAML_FILE, 
        '--path', str(tmp_path)
    ])
    
    assert EXIT_CODE != 0
    
    assert f'Unable to add repo {VALID_REPO_NAME} as it already exists in this catalogue' in caplog.text

def test_add_remote_to_existing_remote(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Simulate adding one remote catalogs to create file structure and then add a real remote to verify allowance"""
    
    # arrange
    monkeypatch.chdir(tmp_path)
    dummy_remote_add("fake-repo.git", "fake-repo", tmp_path)
    
    # act
    EXIT_CODE = add_remote_catalog([
        VALID_GIT_SSH, 
        VALID_YAML_FILE,
        '--path', str(tmp_path)
    ])
    
    assert EXIT_CODE == 0
    
    # assert files created 
    index_file = join(tmp_path, 'index.yaml')
    library_file = join(tmp_path, 'library.yaml')
    
    assert exists(index_file)
    assert exists(library_file)
    assert exists(join(tmp_path, VALID_REPO_NAME + '.json'))
    assert exists(join(tmp_path, VALID_REPO_NAME))
    assert exists(join(tmp_path, "fake-repo.json"))
    
    # assert the addition of new content and non-removal of old
    with open(index_file) as index:
        content = yaml.safe_load(index)
        assert VALID_REPO_NAME in content['catalogs']
        assert "fake-repo" in content['catalogs']
        
    with open(library_file) as library:
        content = yaml.safe_load(library)
        assert VALID_GIT_SSH in content['catalogs']
        assert "fake-repo.git" in content['catalogs']
        
def test_add_remote_to_local_existing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Add a remote catalog to existing local add file structure"""
    
    # arrange
    monkeypatch.chdir(tmp_path)
    dummy_local_add("fake-repo", tmp_path)
    
    # act
    EXIT_CODE = add_remote_catalog([
        VALID_GIT_SSH,
        VALID_YAML_FILE,
        "--path", str(tmp_path)
    ])
    
    assert EXIT_CODE == 0
    
    # assert files created 
    index_file = join(tmp_path, 'index.yaml')
    library_file = join(tmp_path, 'library.yaml')
    
    assert exists(index_file)
    assert exists(library_file)
    assert exists(join(tmp_path, VALID_REPO_NAME + '.json'))
    assert exists(join(tmp_path, VALID_REPO_NAME))
    assert exists(join(tmp_path, "fake-repo.json"))
    
    # assert the addition of new content and non-removal of old
    with open(index_file) as index:
        content = yaml.safe_load(index)
        assert VALID_REPO_NAME in content['catalogs']
        assert "fake-repo" in content['catalogs']
        
    with open(library_file) as library:
        content = yaml.safe_load(library)
        assert VALID_GIT_SSH in content['catalogs']
        assert len(content['catalogs']) == 1
        
def test_add_local_to_existing_remote(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """This seems like a test that should be more for the add_remote_catalog tests"""
    pass