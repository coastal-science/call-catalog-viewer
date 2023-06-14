from pathlib import Path
import pytest
from src.remove_catalog import cli as remove_catalog
from src.utils import yaml
from tests.test_add_catalog import make_library, make_index, make_existing

def test_remove_cli_empty():
    """Calling cli without arguments should exit and want about missing arguments"""

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        exit_code = remove_catalog()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0


def test_remove_to_nonfolder(tmp_path: Path):
    """Attempt to remove a catalog to a nonexistent catalog folder should exit"""

    print(f"{tmp_path=}")
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        exit_code = remove_catalog(["my_catalog",
                                 "nonexistent_catalog_folder",
                                 "catalog.yaml"])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code != 0
