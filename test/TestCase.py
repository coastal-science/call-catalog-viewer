"""Run with: `srkw-call-catalogue$ python -m test.TestCase`
Returns:
    _type_: _description_
"""
# import __init__ as __
# import fs
from src import fs
import sys

from pathlib import Path

print(Path.cwd(), sys.path)


class TestCase:
    """Helper class to use as a struct"""

    def __init__(self, case_id, test_case, expected, desc) -> None:
        self.case_id = case_id
        self.test_case = test_case
        self.expected = expected
        self.desc = desc

    def __repr__(self) -> str:
        line = self.test_case.splitlines()[0:2]
        line = line[0] if line[0] != "" else line[1]
        return f"<case_id={self.case_id}, desc={self.desc}, expected={self.expected}, test_case='{line}'>"

    def __str__(self) -> str:
        line = self.test_case.splitlines()[0:2]
        line = line[0] if line[0] != "" else line[1]
        return f"<case_id={self.case_id} desc={self.desc} expected={self.expected} test_case='{line}'>"


if __name__ == '__main__':
    """Create files and folders to function as expected test cases for the comparison.
    Use the `create_fs` function to bootstrap the creation of files/folders.
    Subsequently a person should check whether the documents are created as expected.
    """

    from test.TestFiles import all_tests as files_tests
    from test.TestFolders import all_tests as folders_tests
    from test.TestFolders import all_tests as corner_tests

    all_tests = files_tests + folders_tests  # + corner_tests


    print(*all_tests, sep='\n', end='\n\n')

    for _ in all_tests:
        try:
            print(_)
            print(fs.create_fs(fs.read_str(_.test_case), tempdir='test/test_fs_create'))
        except Exception as err:
            print(err)
