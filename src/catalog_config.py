"""Configure Catalog setup. Add and remove catalogs from the viewer's 'library/'
usage: catalog_config.py [-h] {add,remove} ...

Configure (add/remove) catalogs that this viewer can display

positional arguments:
  {add,remove}  `add` or `remove`
  cmdargs

Example:

`python catalog_config.py add ...<cmd line arguments of add_catalog.py>...`

`python catalog_config.py remove ...<cmd line arguments of remove_catalog.py>...`

To see individual `help` use
```
python catalog_config.py add -h | --help
python catalog_config.py remove -h | --help
```
"""


import argparse
import shlex
import subprocess
import sys
from pathlib import Path

from add_catalog import cli as add_catalog
from remove_catalog import cli as remove_catalog

LIBRARY = "catalogs"
LIBRARY_INDEX = "index.yaml"


if __name__ == "__main__":

    # cmd, name, folder, file  = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    parser = argparse.ArgumentParser(
        description="Configure (add/remove) catalogs that this viewer can display",
        allow_abbrev=True,
    )

    parser.add_argument("cmd", choices=["add", "remove"], help="`add` or `remove`")

    parser.add_argument("cmdargs", nargs=argparse.REMAINDER)

    args = parser.parse_args()
    print(args)

    cmd = args.cmd
    cmdargs = args.cmdargs
    cmdargs = ' '.join(cmdargs)  # to be split comprehensively with shlex.split()

    thisfile = Path(__file__).name
    src = Path(__file__).parent.stem

    """
    The commented section below code is generic, precise, short but obscure.
    It runs **any** python script of the form `src/*_catalog.py` with all cmd line args
    The version below the commenting is explicit but longer.
    """

    # fullcmd = f"{sys.executable} src/{cmd}_catalog.py {' '.join(cmdargs)}"

    print(f"{thisfile}: {cmd} {cmdargs}")
    # print(f"{thisfile}: subprocess: {fullcmd}")

    # fullcmd = shlex.split(fullcmd)
    # output = subprocess.run(fullcmd, universal_newlines=True)

    # print("\nCompleted all subprocesses")
    # print()
    # exit(output.returncode)

    if cmd == "add":
        print("call 'add_catalog.py'")
        fullcmd = f"{sys.executable} {src}/add_catalog.py {cmdargs}"  # instead of call add_catalog()
        # system call instead of method call since add_catalog.py contains extra input arguments 
        # and file validation.

    if cmd == "remove":
        print("call 'remove_catalog.py'")
        fullcmd = f"{sys.executable} {src}/remove_catalog.py {cmdargs}"

    print(f"{thisfile}: subprocess: {fullcmd}")

    fullcmd = shlex.split(fullcmd)
    output = subprocess.run(fullcmd, universal_newlines=True)

    print("\nCompleted all subprocesses")
    print()
    exit(output.returncode)
