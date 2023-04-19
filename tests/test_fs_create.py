from pathlib import Path
import fs
import filecmp

class TestCreate:

    # @pytest.mark.datafiles()
    def test_folder_empty(self, tmp_path: Path, datadir):
        print('hello')
        print(tmp_path)
        print(type(tmp_path))
        
        d1 = fs.read_str("empty_folder: ")
        fs.create_fs(d1, tempdir=tmp_path)

        print(datadir)
        print(type(datadir))
        expected = datadir

        print(*list(tmp_path.rglob("*")), sep='\n')
        assert 0
        # assert filecmp.dircmp(expected, tmp_path)
