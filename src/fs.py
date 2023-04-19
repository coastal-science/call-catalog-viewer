""" Helper functions for folder structure and file system inspections
`create_fs(yaml_dict)`: Creates files and directories as defined in the yaml document.
`compare_fs(d1, d2)`: Compare folders

A folder is any document name (key) without content (value) and without an extension (suffix).
Anything else is considered a file.

"""


import re
from pathlib import Path
import filecmp
import flatdict  # multiline strings and None values written as empty strings.
from utils import yaml
import logging

global DEBUG

FORMAT = '%(levelname)s - %(asctime)s - %(message)s'
FORMAT_VERBOSE = '%(asctime)s: - %(levelname)s:%(name)s - %(module)s/%(filename)s/%(funcName)s/%(lineno)d:\t%(message)s'

logging.basicConfig(level=logging.INFO, format=FORMAT_VERBOSE)

logger = logging.getLogger(__name__)
# logger.setLevel('DEBUG')
# console = logging.StreamHandler()
# formatter = logging.Formatter(FORMAT_VERBOSE)
# console.setFormatter(formatter)
# logger.addHandler(console)

yaml_str = """
test/data/create:
    Download:
        Music:
        Movies:
    University:
        First year:
            English: |
                    Line 1
                    Line 2
            Maths.txt: E=mc^2
            CS.yaml: "Key: Value"
            History.json:
            Art:
        Second year: 2
        Third year:
"""


def create_fs(yaml_dict: dict, tempdir=""):
    """Create files and directories as defined in the yaml document.
    An path with a suffix (file extension) is considered a file, otherwise a folder.

    Args:
        yaml_str (str): String formatted in yaml format

    Returns:
        bool|exception: True for successful execution or exceptions
    """

    paths = flatdict.FlatDict(yaml_dict, delimiter="/")
    # print("Creating folders/files:")
    # print(" ", *paths, end="\n\n")
    logger.info("Creating folders/files")
    logger.debug(paths)

    if isinstance(tempdir, str):
        cwd = Path(tempdir)
    else:
        cwd = tempdir

    for path, content in paths.items():
        p = (cwd / path).resolve()

        if not content and not p.suffix:  # p is a folder
            folder = Path(p)
            # mkdir -p path/to/folder
            folder.mkdir(parents=True, exist_ok=True)
            # print(f"Folder: {folder}")
            logger.debug(f"Folder: {folder}")

        else:  # p is a file
            file = Path(p)
            file.parent.mkdir(parents=True, exist_ok=True)
            file.touch()
            # print(f"File: {file}")
            logger.debug(f"File: {file}")

            # Open the file pointed to in text mode, write data to it, and close the file
            content = content or ""  # In case of `None` write empty string
            file.write_text(str(content))

            # print("Text:")
            # print(content, end="\n\n")
            logger.debug("Text:")
            logger.debug(content)
    logger.info('Complete')

    return True


def read_str(yaml_str: str) -> dict:
    """Load yaml dictionary from a string definition

    Args:
        yaml_str (str): String formatted in yaml format

    Returns:
        dict
    """

    yaml_dict = yaml.safe_load(yaml_str)
    return yaml_dict


def read_file(yaml_path) -> dict:
    """Load yaml dictionary from a yaml-file

    Args:
        yaml_path (str): Path to file

    Returns:
        dict
    """

    with open(Path(yaml_path).resolve()) as spec_file:
        read_str(yaml_str(spec_file))
        # try:
        #     yaml_dict = yaml.safe_load(spec_file)
        #     return yaml_dict
        # except Exception as err:
        #     print(err)


def compare(left, right) -> bool:
    """Compare whether the documents (files/folders) within the `left` folder match in `right`.

    Args:
        left (str): path to folder
        right (str): path to folder

    Returns:
        bool: Returns True when all documents match and file content (docs with extensions) seem equal
                For more details see [`filecmp.cmp`](https://docs.python.org/3/library/filecmp.html).
              Otherwise, returns False
    """

    # print(f"{left=}, {right=}")
    logger.info(f"{left=}, {right=}")

    left_path, right_path = Path(left), Path(right)

    # left_all = left_path.rglob("*")
    result = {}
    mismatch = {}
    cond = True

    # Using generator and on-demand checking to reduce memory usage instead of in-memory set intersection/difference operations.
    # Also, iteration was necessary for individual filecmp.
    # for i, p in enumerate(left_all):
    for p in left_path.rglob("*"):

        # extract a version of the path relative to `left`
        relative = p.relative_to(left)
        q = right_path / relative
        # logger.debug(p, q, p.relative_to(left))

        if p.is_dir():
            check = q.is_dir()
        if p.is_file():
            # Compare file contents
            filecmp.clear_cache()
            check = q.is_file() and filecmp.cmp(p, q, shallow=False)

        result[str(relative)] = check
        if check is False:
            mismatch[str(relative)] = check

        cond = cond and check

    # print(yaml.dump({'Comparison': result}, indent=2), end='\n\n')
    logger.info(yaml.dump({'Comparison': result}, indent=2))
    # print(yaml.dump({'Comparison mismatches': list(mismatch.keys())}), end='\n\n')
    logger.info(yaml.dump({'Comparison mismatches': sorted(mismatch.keys())}))
    return cond, mismatch.keys()


def smaller_on_left(left, right):
    left_path, right_path = Path(left), Path(right)

    n = len(list(Path(left).rglob("*")))
    m = len(list(Path(right).rglob("*")))

    if m < n:  # Ensure left << right
        left, right = right, left
        left_path, right_path = right_path, left_path
        n, m = m, n
    return left, right, left_path, right_path
# left, right, left_path, right_path = smaller_on_left(left, right)


def compare_fs(left_dir, right_dir) -> tuple[bool, list]:
    """Compare folder structure.

    Args:
        left_name (str): path to folder
        right_name (str): path to folder

    Returns:
        bool: Returns True when all document names match and file content (docs with extensions) seem equal
                For more details see [`filecmp.cmp`](https://docs.python.org/3/library/filecmp.html).
              Otherwise, returns False
    """

    left_path, right_path = Path(left_dir), Path(right_dir)

    # folder_left = [re.sub(f"^{left_name}", "", str(p))
    #                for p in left_path.rglob("*")]
    left_all = left_path.rglob("*")
    # remove the leading {left_name} from the paths so that the comparisons can ignore it
    folder_left = [remove_leading_path(left_dir, p)
                   for p in left_all]
    folder_left = sorted(folder_left)  # for printing purposes

    # files_left = list(left_path.rglob("*.*"))
    files_left = [p for p in left_path.rglob("*") if p.is_file()]

    print(f"{left_dir}...",
          *folder_left, sep='\n  ', end='\n\n')
    print(*files_left, sep='\n', end='\n\n\n')

    # folder_right = [re.sub(f"^{right_name}", "", str(p))
    #                 for p in right_path.rglob("*")]
    right_all = right_path.rglob("*")
    folder_right = [remove_leading_path(right_dir, p)
                    for p in right_all]
    folder_right = sorted(folder_right)

    # files_right = list(right_path.rglob("*.*"))
    files_right = [p for p in right_path.rglob("*") if p.is_file()]

    print(f"{right_dir}...",
          *folder_right, sep='\n  ', end='\n\n')
    print(*files_right, sep='\n', end='\n\n\n')

    # Compare document names
    names_cmp = set(folder_left) == set(folder_right)
    print(f"Compare folder and file names: {names_cmp=}")

    left_all = left_path.rglob("*")
    right_all = right_path.rglob("*")
    diff_all = {
        # (f"{p1}", f"{p2}"): f"{remove_leading_path(left_name, p1)} {remove_leading_path(right_name, p2)}"
        (f"{p1}", f"{p2}"): remove_leading_path(left_dir, p1) == remove_leading_path(right_dir, p2)
        for p1, p2 in zip(left_all, right_all)
    }

    # Compare file contents
    filecmp.clear_cache()
    # Key: tuple(str, str) with left and right paths
    # Value: bool evaluation of comparison
    diff = {
        (f"{f1}", f"{f2}"): filecmp.cmp(f1, f2, shallow=False)
        for f1, f2 in zip(files_left, files_right)
    }
    # in case there are no files to compare, all() will evaluate to True
    files_cmp = all(diff.values())

    print(f"Compare content of all files: {files_cmp=}")
    print(diff.values())
    print(f"{names_cmp=} and {files_cmp=} = {names_cmp and files_cmp}", end='\n\n')

    mismatch = []
    if not names_cmp:
        miss = set(folder_left).symmetric_difference(set(folder_right))
        print("Mismatched folder(s):\n", miss)
        mismatch.extend(miss)

    if not files_cmp:
        miss = [k for k, v in diff.items() if v is False]
        print("Mismatched file(s):\n", miss)
        mismatch.extend([*miss])

    [print(k, ":", v) for k, v in diff_all]
    print(diff_all.keys())
    print(diff_all.values())

    print(end='\n\n')
    return (names_cmp and files_cmp), mismatch


def remove_leading_path(leading_path, p):
    return re.sub(f"^{leading_path}", "", str(p))


if __name__ == '__main__':

    DEBUG, LOGLEVEL = True, logging.DEBUG
    logger.setLevel(LOGLEVEL)

    logger.info(f"Current directory: {Path.cwd()}")

    yaml_dict = read_str("""test/test_fs_create/empty_folder: """)

    # yaml_path = "path/to/directory/spec.yaml"
    # yaml_dict = read_file(yaml_path)

    creation = create_fs(yaml_dict)

    # diff = filecmp.dircmp("TEST0", "TEST")
    # print(end='\n\n\n)
    # diff.report_full_closure()

    # #print(diff.common)
    # #print(diff.common_dirs)
    # #print(diff.common_files)
    # #print(diff.common_funny)

    # folder_left = list(map(str, Path(left_name).rglob("*")))

    expected = "abc/TEST0/"
    right_name = "abc/TEST/"

    # comparison = compare_fs(expected, right_name)
    # print(comparison)
    # print(len(comparison[1]))
    compare(expected, right_name)
