import argparse
import shlex
import subprocess
import sys
from pathlib import Path

import add_catalog
import remove_catalog

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

    catalog_folder = "catalogs"
    catalog_file = "catalog.yaml"

    thisfile = Path(__file__).name
    fullcmd = f"{sys.executable} code/{cmd}_catalog.py {cmdargs}"

    print(f"{thisfile}: {cmd} {cmdargs}")
    print(f"  {fullcmd}")
    fullcmd = shlex.split(fullcmd)

    output = subprocess.run(fullcmd, universal_newlines=True)

    if cmd == "add":
        print("call 'add_catalog.py'")
        # print(f"{thisfile}: add catalog named {name=} with entries {file=} from {folder=}")
        # EXIT_CODE = add_catalog.add(name, folder, file, force=True)
        fullcmd = f"{sys.executable} code/add_catalog.py {cmdargs}"
    if cmd == "remove":
        print("call 'remove_catalog.py'")
        # print(f"{thisfile}: remove catalog named {name=} listed in {catalog_folder}/{catalog_file=}")
        # EXIT_CODE = remove_catalog.remove(name, catalog_folder, catalog_file, force=True)
        fullcmd = f"{sys.executable} code/remove_catalog.py {cmdargs}"

    fullcmd = shlex.split(fullcmd)
    output = subprocess.run(fullcmd, universal_newlines=True)
    EXIT_CODE = output.returncode

    print("Complete")
    print()
    exit(EXIT_CODE)
