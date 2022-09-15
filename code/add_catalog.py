"""
usage: add_catalog.py [-h] [--force | --no-force] [--debug | --no-debug] name folder file

  name                 Name of new catalog to add
  folder               New catalog folder containing catalog data files
  file                 Yaml file within `folder` containing the catalog entries

  --force, --no-force  Remove before adding catalog even if it already exists (default: False)

Example:
`python add_catalog.py srkw-call-catalogue-files ./srkw-call-catalogue-files call-catalog.yaml`
`python add_catalog.py srkw-call-catalogue-files ./srkw-call-catalogue-files call-catalog.yaml --force`

The important files for configuring multiple catalogs are:
```
/var/www/html/catalog-viewer/
├── catalog
│   ├── catalogs.yaml
│   ├── <catalog-A-name>.json # produced by `read_files.py` parser
│   ├── <catalog-A-name> -> /var/www/html/<catalog-A-name> # symbolic link
│   │   ├── call-catalog.yaml
│   │   ├── ...
```
`catalog.yaml`
```yaml
catalogs:
    - srkw-call-catalogue-files
    - nrkw-call-catalogue-files
    - transient-call-catalogue-files
```
Starting with an empty list of catalogs `catalog.yaml`:
```yaml
catalogs:
    - 
```
and the following folder structure:
/var/www/html/catalog-viewer/
├── catalog
│   └── catalog.yaml
├── home.html
└── index.html
```

To `add` a catalog use the command `$ python code/add_catalog.py srkw-call-catalogue-files ./srkw-call-catalogue-files call-catalog.yaml`

`catalog.yaml` updates like so
```yaml
catalogs:
    - srkw-call-catalogue-files
    - nrkw-call-catalogue-files         # independent calls `add_catalog.py`
    - transient-call-catalogue-files    # independent calls `add_catalog.py`
```
And the directories update symbolic links accordingly
```
/var/www/html/catalog-viewer/
├── catalog
│   ├── catalogs.yaml
│   ├── srkw-call-catalogue-files.json  # produced by `read_files.py` parser
│   ├── srkw-call-catalogue-files -> /var/www/html/srkw-call-catalogue-files    # symbolic link
│   │   ├── call-catalog.yaml
│   │   ├── ...
│   │   └── media   # containing jpg, wav, etc
│   └── catalog.yaml
├── home.html
└── index.html
```

To `remove` a catalog use the command `$ python code/remove_catalog.py srkw-call-catalogue-files`
"""


import argparse
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime
from os import PathLike
from pathlib import Path

import yaml

import remove_catalog
from utils import yaml, is_yaml  # represent 'None' values as empty strings ''

ADD_EXIT_ERROR = -1

LIBRARY = "catalogs"
LIBRARY_INDEX = "catalogs.yaml"


def add(catalog_name: str, source_folder, catalog_listing, force=False):
    """Add a catalog to the viewer.

    Args:
        catalog_name (str): _description_
        source_folder (str): Folder where the catalog files are located. A symlink to this folder will be created for the viewer.
        catalog_listing (str): Yaml containing the catalog entries.
        force (bool, optional): Remove `catalog_name` if already present. Removes symlinks and parsed json. Defaults to False.

    Returns:
        int: Exit Code. 0 means success.
    """

    # Remove existing catalog

    print(f"\nRemove {catalog_name=} if already present")

    removed = remove_catalog.remove(catalog_name, force=force)
    if not removed:  # early stopping because `force` could not remove
        exit(ADD_EXIT_ERROR)

    print()

    catalog_listing = Path(catalog_listing).resolve()
    source_folder = Path(source_folder).resolve()

    filename, extension = catalog_listing.stem, catalog_listing.suffix

    # Create
    print(f"Create symlinks to {source_folder.name}")

    # print(f"  mkdir -p catalogs/{catalog_name}/")
    # mkdir -p catalogs/"$name"/
    # source_folder.mkdir(parents=True, exist_ok=True)

    print(f"  ln -s {source_folder} {LIBRARY}/{catalog_name}")
    catalogs = Path(LIBRARY, catalog_name).resolve()

    # print(f"{folder=}, {catalogs=}")
    catalogs.symlink_to(source_folder, target_is_directory=True)

    print(f"Created folder {LIBRARY}/{catalog_name}/ and linked to {source_folder}")
    # print(f"{catalogs}, {catalogs.resolve()}")
    # cd $REPO_DIR/call-catalog-viewer/ || exit # in case cd fails.

    print("\nCalling code/read_files.py...")
    # python code/read_files.py resources_config/call-catalog-desc.yaml resources_config/call-catalog
    cmd = f"{sys.executable} code/read_files.py {LIBRARY}/{catalog_name}/{catalog_listing.name} {LIBRARY}/{catalog_name}"  # {'--force' if force else ''}
    print(f"  {cmd}")
    cmd = shlex.split(cmd)

    if force:
        output = subprocess.run(cmd, universal_newlines=True)
        EXIT_CODE = output.returncode
    else:
        EXIT_CODE = ADD_EXIT_ERROR
    # EXIT_CODE = subprocess.run(cmd, universal_newlines=True).returncode if force else MY_EXIT_ERROR

    if EXIT_CODE != 0:
        # now=`date +%F-%T-%Z`
        now = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        # now = datetime.now()
        print(f"{now}: Could not complete python operation ({EXIT_CODE}).")
        STATE = "failure"
    else:
        # print(f"{now}: python exit code is {EXIT_CODE}")
        STATE = "success"

    # Add the new catalog name to viewer/catalogs/catalogs.yaml
    path = Path(LIBRARY).resolve() / LIBRARY_INDEX

    with open(path, "r+") as f:
        all_catalogs = yaml.safe_load(f)

        if not all_catalogs:
            all_catalogs = {"catalogs": []}
        all_catalogs["catalogs"].append(catalog_name)
        
        # Ensure rewriting existing content, without seek(), the effect is to append to the end of the document.
        f.seek(0)
        yaml.dump(all_catalogs, f)

    return 0 if STATE == "success" else EXIT_CODE


def touch(index_file: str):
    """'Touch' `<index_file.yaml>`

    Checks for the existence and creates the non empty yaml `index_file`.
    The file must contain a root level key "catalogs" containing a list of strings.

    Args:
        index_file (str): Location of yaml file containing list of all catalogs supported by the viewer.
    """

    path = Path(index_file).resolve()
    index_file = path.name  # index.yaml
    print(index_file)

    if not is_yaml(index_file):
        # if not any([catalog_file.lower().endswith(x) for x in [".yaml", ".yml"]]):
        print(f"{thisfile}: {cmd}: {index_file} does not have yaml extension", end="\n\n")
        exit(ADD_EXIT_ERROR)

    if not path.is_file():
        print(f"{thisfile}: {cmd}: {index_file} does not exist. Creating an empty file.")
        path.touch()

    with open(path, "r+") as f:
        all_catalogs = yaml.safe_load(f)
        if not all_catalogs:
            print(f"{thisfile}: {cmd}: {index_file} must containg one key 'catalog' with a list of catalog names.")

            empty = {"catalogs": []}
            print(empty)

            yaml.dump(empty, f)
            print(f"{thisfile}: {cmd}: Created {index_file}")


def is_valid_file(parser, arg):
    """Argparse function to validate whether the file exists
    TODO: Refactor. This function is c/p in many modules.
    """

    if not os.path.exists(arg):
        parser.error("The file %s does not exist or cannot be found!" % arg)
    else:
        # return open(arg, 'r')  # return an open file handle
        return arg


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Add catalogs that this viewer can display", allow_abbrev=True
    )

    parser.add_argument("name", help="Name of new catalog to add/remove", type=str)

    parser.add_argument(
        "folder",
        help="Source folder to be added that contains data files",
        type=lambda x: is_valid_file(parser, x),
    )

    parser.add_argument(
        "index",
        help="Yaml file within `folder` containing the catalog entries",
        # type=lambda x: is_valid_file(parser, x)
    )

    parser.add_argument(
        "--LIBRARY",
        default=LIBRARY,
        required=False,
        help="Library folder for the viewer",
        type=lambda x: is_valid_file(parser, x),
    )

    parser.add_argument(
        "--LIBRARY-INDEX",
        default=LIBRARY_INDEX,
        required=False,
        help="Index yaml within LIBRARY",
    )

    parser.add_argument(
        "--force",
        dest="force",
        required=False,
        help="RRemove before adding catalog even if it already exists",
        default=False,
        # action='store_true', # Python <=3.7
        action=argparse.BooleanOptionalAction,  # Python 3.7+
    )

    parser.add_argument(
        "--debug",
        dest="debug",
        required=False,
        help="Print extra debug information for troubleshooting/developing",
        default=False,
        # action='store_true', # Python <=3.7
        action=argparse.BooleanOptionalAction,  # Python 3.7+
    )

    args = parser.parse_args()
    print(args)

    cmd = "add"
    name = args.name
    source_folder = args.folder
    catalog_listing = args.index
    force = args.force  # default False
    debug = args.debug  # default False

    LIBRARY = args.LIBRARY  # LIBRARY
    LIBRARY_INDEX = args.LIBRARY_INDEX  # LIBRARY_INDEX
    EXIT_CODE = 0

    thisfile = Path(__file__).name
    print(f"{thisfile}: {cmd}:")

    # Check whether `folder` exists and `file` has yaml extension
    if not os.path.isdir(source_folder):
        print(f"{thisfile}: {cmd}: {source_folder=} is not a directory", end="\n\n")
        exit(ADD_EXIT_ERROR)

    p = Path(source_folder, catalog_listing).resolve()
    # print(p)
    # if not file.endswith(".yaml") or not file.endswith('.yml'):
    # if not p.is_file() or not any([p.suffix.lower() in [".yaml", ".yml"]]):
    if not is_yaml(p):
        print(f"{thisfile}: {cmd}: {catalog_listing=} does not exist or does not have yaml extension.", end="\n\n",)
        exit(ADD_EXIT_ERROR)

    print(f" {name=}")
    print(f" folder={Path(source_folder).resolve()}")
    print(f" file={Path(catalog_listing).resolve()}", end="\n\n")

    # catalog_folder = "catalogs"
    # catalog_file = "catalogs.yaml"

    # check for index
    touch(Path(LIBRARY, LIBRARY_INDEX).resolve())

    # Add catalog
    print(f"{thisfile}: add catalog named {name=} with entries {catalog_listing=} from {source_folder=}")
    EXIT_CODE = add(name, source_folder, catalog_listing, force=force)

    print(f"{thisfile}: {cmd}: Complete", end="\n\n")
    exit(EXIT_CODE)
