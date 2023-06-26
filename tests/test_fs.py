from pathlib import Path
import filecmp
import pytest
from src import fs

from tests.TestFiles import all_tests as files_tests
from tests.TestFolders import all_tests as folders_tests
from tests.TestCornerCases import all_tests as corner_tests


class TestCreate:

    @pytest.fixture(scope='function', params=[*files_tests, *folders_tests, *corner_tests])
    def get_creates(self, request, datadir):
        # _ = datadir.rglob("*")
        # [_.expected for _ in files_tests]
        # yield (datadir / request.param)
        return request.param
        # (_.relative_to(datadir/request) for _ in datadir.rglob("*"))
        # datadir.rglob(*).relative_to(datadir)

    def test_create_empty_folder(self, tmp_path: Path, tmp_path_factory: Path, datadir: Path):
        print(f"{tmp_path=}")
        # print(type(tmp_path))
        # print(f"{shared_datadir=}")
        # print(type(shared_datadir))
        print(f"{datadir=}")
        here = Path.cwd()
        target = tmp_path_factory.getbasetemp()
        case = fs.read_str("empty_folder: ")
        assert fs.create_fs(case, tempdir=target)

        target / 'empty_folder'
        expected = datadir / 'empty_folder'
        
        # print(*list( _.relative_to(tmp_path) for _ in tmp_path.rglob("*") ), sep='\n  ')
        assert filecmp.dircmp(expected, target)
        # assert False
    
    def test_create(self, tmp_path_factory: Path, datadir, get_creates):
        # print(f"{tmp_path=}")
        print(f"tmp_path_factory={tmp_path_factory.getbasetemp()}")
        # print(type(tmp_path))
        # print(f"{shared_datadir=}")
        # print(type(shared_datadir))
        # print(f"{datadir=}")
        print('hello sample')
        # print(get_test)

        print()

        target = tmp_path_factory.getbasetemp()
        print(get_creates.test_case)

        if get_creates.expected.endswith("Error"):  # Expect an exception
            with pytest.raises(Exception):
                expected = get_creates.expected
                case = fs.read_str(get_creates.test_case)
                result = fs.create_fs(case, tempdir=target)
                assert False
            return

        # expect a boolean evaluation prior to any exception
        elif isinstance(get_creates.expected, bool):
            try:
                case = fs.read_str(get_creates.test_case)
                result = case
                result = fs.create_fs(case, tempdir=target)
            except:
                assert result is get_creates.expected
            finally:
                return

        else:   # expected folder structure
            print(datadir / get_creates.expected)
            expected = datadir / get_creates.expected
            case = fs.read_str(get_creates.test_case)
            assert fs.create_fs(case, tempdir=target)

        print(f"{expected=}\n{target=}", end='\n\n')
        print(*list(expected.rglob("*")), sep='\n  ', end='\n\n')
        print(*list(target.rglob("*")), sep='\n  ', end='\n\n')

        return expected, target
        assert fs.compare(expected, target)
        # print(*list( _.relative_to(tmp_path) for _ in tmp_path.rglob("*") ), sep='\n  ')
        # assert False

    @pytest.fixture(scope='function')
    def get_compares(self, tmp_path_factory: Path, datadir, get_creates):
        target = tmp_path_factory.getbasetemp()
        expected = datadir / get_creates.expected

        if get_creates.expected.endswith("Error"):  # Expect an exception
            with pytest.raises(Exception):
                expected = get_creates.expected
                case = fs.read_str(get_creates.test_case)
                result = fs.create_fs(case, tempdir=target)
                assert False
            return

        elif isinstance(get_creates.expected, bool):
            try:
                case = fs.read_str(get_creates.test_case)
                result = case
                result = fs.create_fs(case, tempdir=target)
            except:
                assert result is get_creates.expected
            finally:
                return
        else:
            case = fs.read_str(get_creates.test_case)
            assert fs.create_fs(case, tempdir=target)
            return expected, target

    def test_compare(self, get_compares):
        if get_compares:
            expected, target = get_compares
        else:
            pytest.skip("unsupported configuration")
        assert fs.compare(expected, target)
