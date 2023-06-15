from pathlib import Path
import pytest
from src.add_catalog import cli as add_catalog
from src.utils import yaml


def test_add_cli_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Calling cli without arguments should exit and warn about missing arguments"""

    # arrange
    monkeypatch.chdir(tmp_path)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        exit_code = add_catalog([""])

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0


def test_add_null_folder_catalog(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Add a catalog of a nonexistent catalog folder should exit"""
    
    # arrange
    print(f"{tmp_path=}")
    monkeypatch.chdir(tmp_path)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        exit_code = add_catalog(["my_catalog",
                                 "nonexistent_catalog_folder",
                                 "catalog.yaml"])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0


def make_library(library_name="catalogs"):
    # print(f"make_library:{tmp_path}:")
    d = Path(library_name)
    d.mkdir()
    # print(f"{d}")
    return d


def make_index(lib_name=None, index_name="index.yaml"):
    # print(f"make_index:{index_name=}")
    index = lib_name / index_name
    index.touch()
    index.write_text(yaml.dump(
        {"catalogs": []}
        ))
    print(f"make_index:{index}:")
    return index


def test_add(tmp_path: Path, tmp_path_factory: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch):
    """Add a files directory to the catalog in the default folder names/space and index.
    Using a real files directory and yaml."""
    
    # arrange
    print(f"{tmp_path=},{shared_datadir=}")
    monkeypatch.chdir(tmp_path)

    lib_name = make_library(library_name="catalogs")
    print(f"test_add:{lib_name=}m {Path.cwd()}")
    index = make_index(lib_name, index_name="index.yaml")
    
    # print(f"test_add:{f=}")
    # print("ls:")
    # print(*list( _.relative_to(tmp_path) for _ in tmp_path.rglob("*") ), sep='\n  ')
    # print("ls:")
    # print(*list( _.relative_to(shared_datadir) for _ in shared_datadir.rglob("*") ), sep='\n  ')

    # act
    exit_code = add_catalog(["ABCW",
                             str(shared_datadir / 'abcw-call-catalog-files'), #"catalogs",
                             "call-catalog.yaml",
                             "--LIBRARY", str(lib_name)])

    # assert
    assert exit_code == 0

    assert lib_name.exists() and lib_name.name == "catalogs"
    
    assert (lib_name / "ABCW").is_dir()
    assert (lib_name / "ABCW.json").is_file()
    
    assert index.exists() and index.name == "index.yaml"
    with open(index) as f:
        content = yaml.safe_load(f)
        assert "ABCW" in content['catalogs']

    # cleanup
    # operations occur in the `tmp_path` folder,
    # which is unique to each invocation of the test function handled by `monkeypatch`


def test_add_2(tmp_path: Path, tmp_path_factory: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch):
    """Add a files directory to the catalog in a custom folder names/space and index.
    Using a real files directory and yaml"""

    # arrange
    monkeypatch.chdir(tmp_path)

    lib_name = make_library(library_name="library")

    index = make_index(lib_name, index_name="directory.yaml")
    
    # act
    exit_code = add_catalog(["ABCW",
                             str(shared_datadir / 'abcw-call-catalog-files'), #"catalogs",
                             "call-catalog.yaml",
                             "--LIBRARY", str(lib_name),
                            "--LIBRARY-INDEX", 'directory.yaml'])
    
    # assert
    assert exit_code == 0
    
    assert lib_name.exists() and lib_name.name == "library"
    
    assert (lib_name / "ABCW").is_dir()
    assert (lib_name / "ABCW.json").is_file()
    
    assert index.exists() and index.name == "directory.yaml"
    with open(index) as f:
        content = yaml.safe_load(f)
        assert "ABCW" in content['catalogs']
    
    # cleanup
    # operations occur in the `tmp_path` folder,
    # which is unique to each invocation of the test function handled by `monkeypatch`


def test_sub(tmp_path: Path, tmp_path_factory: Path, monkeypatch: pytest.MonkeyPatch):
    print(f"{tmp_path=}")
    monkeypatch.chdir(tmp_path)
    lib_name = make_library(library_name="library")
    print(f"test_sub:{lib_name=}")
    f = make_index(lib_name, index_name="list.yaml")
    print(f"test_sub:{f=}")
    print("ls:")
    print(*list( _.relative_to(tmp_path) for _ in tmp_path.rglob("*") ), sep='\n  ')

    # assert True


def make_existing(lib_name: Path, index: Path, catalog_name="ABCW"):
    """Configure library and index with an existing catalog entry"""

    index.write_text(yaml.dump(
        {"catalogs": [catalog_name]}
        )) # overwrites previous file
    
    p = (lib_name / catalog_name)
    p.mkdir()
    
    p.touch("call-catalog.yaml")
    (lib_name / f"{catalog_name}.json").touch()
    
    return p


def test_add_3(tmp_path: Path, tmp_path_factory: Path, shared_datadir: Path, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch):
    """Adding a catalog twice must reject the addition"""

    # arrange
    monkeypatch.chdir(tmp_path)
    lib_name = make_library()

    index = make_index(lib_name)
    make_existing(lib_name, index)

    # act
    exit_code = add_catalog(["ABCW",
                            str(shared_datadir / 'abcw-call-catalog-files'), #"catalogs",
                            "call-catalog.yaml",
                            "--LIBRARY", str(lib_name)])
    # assert
    captured = caplog.text
    assert exit_code != 0
    assert "Use `--force`" in str(captured)

    # cleanup
    # operations occur in the `tmp_path` folder,
    # which is unique to each invocation of the test function handled by `monkeypatch`


def test_add_4(tmp_path: Path, tmp_path_factory: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch):
    """Adding a catalog twice with `--force` should allow the addition."""

    # arrange
    monkeypatch.chdir(tmp_path)
    lib_name = make_library()

    index = make_index(lib_name)
    make_existing(lib_name, index)
    
    # act
    # with pytest.raises(FileExistsError) as pytest_wrapped_e:
    # with pytest.raises(PermissionError) as pytest_wrapped_e:
    exit_code = add_catalog(["ABCW",
                            str(shared_datadir / 'abcw-call-catalog-files'), #"catalogs",
                            "call-catalog.yaml",
                            "--LIBRARY", str(lib_name),
                            "--force"])

    # assert
    # if pytest_wrapped_e.type == PermissionError:
    #     pytest.skip("Cannot complete test due to file permission error, skipping the rest of the test scenario. {LIBRARY}/{catalog_name} may be a non-empty folder.")

    assert exit_code == 0

    assert lib_name.exists() and lib_name.name == "catalogs"

    assert (lib_name / "ABCW").is_dir()
    assert (lib_name / "ABCW.json").is_file()
    
    assert index.exists() and index.name == "index.yaml"
    with open(index) as f:
        content = yaml.safe_load(f)
        assert "ABCW" in content['catalogs']
        assert len(content['catalogs']) == 1
   
    # cleanup
    # operations occur in the `tmp_path` folder,
    # which is unique to each invocation of the test function handled by `monkeypatch`


def test_add_5(tmp_path: Path, tmp_path_factory: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch):
    """Adding two catalogs: Adding the same catalog with 2 different names"""

    # arrange
    monkeypatch.chdir(tmp_path)
    lib_name = make_library()

    index = make_index(lib_name)
    make_existing(lib_name, index)
    
    # act
    exit_code = add_catalog(["XYZW",
                        str(shared_datadir / 'abcw-call-catalog-files'), #"catalogs",
                        "call-catalog.yaml",
                        "--LIBRARY", str(lib_name)])
    # assert
    assert exit_code == 0

    assert lib_name.exists() and lib_name.name == "catalogs"

    assert (lib_name / "ABCW").is_dir()
    assert (lib_name / "ABCW.json").is_file()
    assert (lib_name / "XYZW").is_dir()
    assert (lib_name / "XYZW.json").is_file()
    
    assert index.exists() and index.name == "index.yaml"
    with open(index) as f:
        content = yaml.safe_load(f)
        assert "ABCW" in content['catalogs']
        assert "XYZW" in content['catalogs']
        assert len(content['catalogs']) == 2
    
    # cleanup
    # operations occur in the `tmp_path` folder,
    # which is unique to each invocation of the test function handled by `monkeypatch`


def test_add_6(tmp_path: Path, tmp_path_factory: Path, shared_datadir: Path, monkeypatch: pytest.MonkeyPatch):
    """Adding the same catalog folder with 2 different names"""

    # arrange
    monkeypatch.chdir(tmp_path)
    lib_name = make_library()

    index = make_index(lib_name)
    make_existing(lib_name, index)
    
    # act
    exit_code = add_catalog(["IJKW",
                            str(shared_datadir / 'ijkw-call-catalog-files'), #"catalogs",
                            "call-catalog.yaml",
                            "--LIBRARY", str(lib_name)])
    # assert
    assert exit_code == 0

    assert lib_name.exists() and lib_name.name == "catalogs"

    assert (lib_name / "ABCW").is_dir()
    assert (lib_name / "ABCW.json").is_file()
    assert (lib_name / "IJKW").is_dir()
    assert (lib_name / "IJKW.json").is_file()
    
    assert index.exists() and index.name == "index.yaml"
    with open(index) as f:
        content = yaml.safe_load(f)
        assert "ABCW" in content['catalogs']
        assert "IJKW" in content['catalogs']
        assert len(content['catalogs']) == 2
    
    # cleanup
    # operations occur in the `tmp_path` folder,
    # which is unique to each invocation of the test function handled by `monkeypatch`
