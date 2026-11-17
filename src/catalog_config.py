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
import subprocess
import sys
from pathlib import Path

LIBRARY = "catalogs"
LIBRARY_INDEX = "index.yaml"


if __name__ == "__main__":
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
    thisfile = Path(__file__).name
    src = Path(__file__).parent

    if cmd == "add":
        print("call 'add_catalog.py'")
        script = src / "add_catalog.py"
        fullcmd = [sys.executable, str(script), *cmdargs]

    elif cmd == "remove":
        print("call 'remove_catalog.py'")
        script = src / "remove_catalog.py"
        fullcmd = [sys.executable, str(script), *cmdargs]

    else:
        raise ValueError(f"Unsupported command: {cmd!r}")

    print(f"{thisfile}: subprocess: {fullcmd}")
    output = subprocess.run(fullcmd, text=True)

    print("\nCompleted all subprocesses")
    print()
    raise SystemExit(output.returncode)
