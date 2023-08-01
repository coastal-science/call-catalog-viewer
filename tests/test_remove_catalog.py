from pathlib import Path
import pytest
from src.remove_catalog import cli as remove_catalog
from src.utils import yaml
from tests.test_add_catalog import make_library, make_index, make_existing


def test_remove_cli_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Calling cli without arguments should exit and warn about missing arguments"""
    
    # arrange
    monkeypatch.chdir(tmp_path)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        exit_code = remove_catalog([""])

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0


def test_remove_from_uninitialized_library(tmp_path: Path, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch):
    """Remove a catalog from uninitialized index.yaml"""
    
    # arrange
    monkeypatch.chdir(tmp_path)

    # act
    print(f"{tmp_path=}")
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        exit_code = remove_catalog(["nonexistent_catalog_name"])
    
    # assert
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0
    
    # cleanup
    # operations occur in the `tmp_path` folder,
    # which is unique to each invocation of the test function handled by `monkeypatch`


def test_remove_from_empty_library(tmp_path: Path, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch):
    """Remove a catalog from an empty index.yaml"""
    
    # arrange
    print(f"{tmp_path=}")
    monkeypatch.chdir(tmp_path)

    lib_name = make_library(library_name="catalogs")
    print(f"test_remove:{lib_name=}")
    index = make_index(lib_name, index_name="index.yaml")
    
    # print("ls:")
    # print(*list( _.relative_to(tmp_path) for _ in tmp_path.rglob("*") ), sep='\n  ')

    # act
    print(f"{tmp_path=}")
    exit_code = remove_catalog(["nonexistent_catalog_name",
                                "--LIBRARY", str(lib_name)])
    # assert
    captured = caplog.text

    print(f"{exit_code=},{captured=}.")
    assert exit_code == 0
    assert "nothing to remove here" in str(captured)

    # cleanup
    # operations occur in the `tmp_path` folder,
    # which is unique to each invocation of the test function handled by `monkeypatch`


def test_remove_last_catalog(tmp_path: Path, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch):
    """Remove a catalog from index.yaml such that no catalog entries remain"""
    
    # arrange
    print(f"{tmp_path=}")
    monkeypatch.chdir(tmp_path)

    lib_name = make_library(library_name="catalogs")
    print(f"test_remove:{lib_name=}")
    index = make_index(lib_name, index_name="index.yaml")
    make_existing(lib_name, index)

    # print("ls:")
    # print(*list( _.relative_to(tmp_path) for _ in tmp_path.rglob("*") ), sep='\n  ')

    # act
    print(f"{tmp_path=}")
    exit_code = remove_catalog(["ABCW",
                                "--LIBRARY", str(lib_name)])
    # assert
    captured = caplog.text
    print(f"{exit_code=},{captured=}.")
    
    assert exit_code == 0

    assert not (lib_name / "ABCW").exists()
    assert not (lib_name / "ABCW.json").exists()

    assert index.exists() and index.name == "index.yaml"
    with open(index) as f:
        content = yaml.safe_load(f)
        assert not content['catalogs']  # must be an empty array
        assert len(content['catalogs']) == 0

    # cleanup
    # operations occur in the `tmp_path` folder,
    # which is unique to each invocation of the test function handled by `monkeypatch`


def test_remove_catalog(tmp_path: Path, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch):
    """Remove a catalog from index.yaml and leave other catalogs unaffected"""
    
    # arrange
    print(f"{tmp_path=}")
    monkeypatch.chdir(tmp_path)

    lib_name = make_library(library_name="catalogs")
    print(f"test_remove:{lib_name=}")
    index = make_index(lib_name, index_name="index.yaml")
    make_existing(lib_name, index, catalog_name="ABCW")
    make_existing(lib_name, index, catalog_name="IJKW")

    # print("ls:")
    # print(*list( _.relative_to(tmp_path) for _ in tmp_path.rglob("*") ), sep='\n  ')

    # act
    print(f"{tmp_path=}")
    exit_code = remove_catalog(["ABCW",
                                "--LIBRARY", str(lib_name)])
    # assert
    captured = caplog.text
    print(f"{exit_code=},{captured=}.")
    
    assert exit_code == 0

    assert not (lib_name / "ABCW").exists()
    assert not (lib_name / "ABCW.json").exists()

    assert (lib_name / "IJKW").is_dir()
    assert (lib_name / "IJKW.json").is_file()

    assert index.exists() and index.name == "index.yaml"
    with open(index) as f:
        content = yaml.safe_load(f)
        assert "ABCW" not in content['catalogs']
        assert "IJKW" in content['catalogs']
        assert len(content['catalogs']) == 1

    # cleanup
    # operations occur in the `tmp_path` folder,
    # which is unique to each invocation of the test function handled by `monkeypatch`
