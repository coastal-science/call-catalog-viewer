"""
usage: add_catalog.py [-h] [--LIBRARY LIBRARY] [--LIBRARY-INDEX LIBRARY_INDEX] [--force | --no-force]
                      [--debug | --no-debug]
                      name source_folder index

required arguments:
  name                  Name of new catalog to add
  source_folder         Source directory containing data files
  index                 Yaml file within `source` containing the catalog entries

optional arguments:
  --LIBRARY LIBRARY     Library folder for the viewer. This is directory must exist beforehand.
  --LIBRARY-INDEX LIBRARY_INDEX
                        Index yaml within LIBRARY
  --force, --no-force   Remove before adding catalog even if it already exists (default: False)

Example:

`python add_catalog.py srkw-call-catalogue-files ./srkw-call-catalogue-files call-catalog.yaml`

`python add_catalog.py srkw-call-catalogue-files ./srkw-call-catalogue-files call-catalog.yaml --force`

To construct the catalog with a new directory and index use --LIBRARY and --LIBRARY-INDEX arguments
`python add_catalog.py srkw-call-catalogue-files srkw-call-catalogue-files call-catalog.yaml --LIBRARY catalog --LIBRARY-INDEX index.yaml --force `

The relevant files for configuring multiple catalogs are:
```
/var/www/html/catalog-viewer/
├── catalog
│   ├── index.yaml
│   ├── <catalog-A-name>.json # produced by `read_files.py` parser
│   ├── <catalog-A-name> -> /var/www/html/<catalog-A-name> # symbolic link
│   │   ├── call-catalog.yaml
│   │   ├── ...
```
`index.yaml` contains a listing of available catalogs
```yaml
catalogs:
    - srkw-call-catalogue-files
    - nrkw-call-catalogue-files
    - transient-call-catalogue-files
```
Starting with an empty list of catalogs `index.yaml`:
```yaml
catalogs:
    - 
```
and the following folder structure:
```
/var/www/html/catalog-viewer/
├── catalog
│   └── index.yaml
├── home.html
├── ...
└── index.html
```

To `add` a catalog use the command `$ python src/add_catalog.py srkw-call-catalogue-files ./srkw-call-catalogue-files call-catalog.yaml`

`index.yaml` updates like so
```yaml
catalogs:
    - srkw-call-catalogue-files
    - nrkw-call-catalogue-files         # independent calls `add_catalog.py`
    - transient-call-catalogue-files    # independent calls `add_catalog.py`
```
And the directories update symbolic links accordingly
```
/var/www/html/
├── catalog-viewer
    ├── catalog
    │   ├── index.yaml
    │   ├── srkw-call-catalogue-files.json  # produced by `read_files.py` parser
    │   ├── srkw-call-catalogue-files -> /var/www/html/srkw-call-catalogue-files    # symbolic link
    │   │   ├── call-catalog.yaml
    │   │   ├── ...
    │   │   └── media   # containing jpg, wav, etc
    ├── home.html
    └── index.html
├── srkw-call-catalogue-files
        ├── call-catalog.yaml
        ├── ...
        └── media   # containing jpg, wav, etc
```

To `remove` a catalog use the command `$ python src/remove_catalog.py srkw-call-catalogue-files`
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

import remove_catalog
from read_files import cli as read_files
import utils
from utils import yaml
from utils import logging

logger = logging.getLogger(__name__)

ADD_EXIT_ERROR = -1

# LIBRARY = None #"catalogs"
# LIBRARY_INDEX = None #"index.yaml"

# TODO: index.yaml holds catalog-name as well as path to catalog listing (call-catalog.yaml)
"""`index.yaml` updates like so
```yaml
catalogs:
    - srkw-call-catalogue-files/call-catalog.yaml
    - nrkw-call-catalogue-files/call-catalog.yaml         # independent calls `add_catalog.py`
    - transient-call-catalogue-files/call-catalog.yaml    # independent calls `add_catalog.py`
```
"""


def add(catalog_name: str, source_folder, catalog_listing, force=False, LIBRARY="catalogs", LIBRARY_INDEX="index.yaml"):
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
    logger.warning(f"Remove {catalog_name=} if already present")

    removed = remove_catalog.remove(catalog_name, library_index=LIBRARY_INDEX, library=LIBRARY, force=force)
    if not removed:  # early stopping because `force` could not remove
        return ADD_EXIT_ERROR

    catalog_listing = Path(catalog_listing).resolve()
    source_folder = Path(source_folder).resolve()

    filename, extension = catalog_listing.stem, catalog_listing.suffix

    # Create
    logger.info(f"Create symlinks to {source_folder.name}")

    # print(f"  mkdir -p catalogs/{catalog_name}/")
    # mkdir -p catalogs/"$name"/
    # source_folder.mkdir(parents=True, exist_ok=True)

    logger.info(f"  ln -s {source_folder} {LIBRARY}/{catalog_name}")
    catalogs = Path(LIBRARY, catalog_name).resolve()

    catalogs.symlink_to(source_folder, target_is_directory=True)

    logger.info(f"Created folder {LIBRARY}/{catalog_name}/ and linked to {source_folder}")
    # print(f"{catalogs}, {catalogs.resolve()}")
    # cd $REPO_DIR/call-catalog-viewer/ || exit # in case cd fails.

    logger.info("\nCalling src/read_files.py...")
    # python src/read_files.py resources_config/call-catalog-desc.yaml resources_config/call-catalog
    
    cmd = f"{sys.executable} src/read_files.py {LIBRARY}/{catalog_name}/{catalog_listing.name} {LIBRARY}/{catalog_name}"  # {'--force' if force else ''}
    logger.info(f"{cmd}")
    # cmd = shlex.split(cmd)

    # output = subprocess.run(cmd, universal_newlines=True) # before it wouldn't run if not --force?
    # EXIT_CODE = output.returncode

    EXIT_CODE = read_files([str(f"{LIBRARY}/{catalog_name}/{catalog_listing.name}"),
                            str(f"{LIBRARY}/{catalog_name}"),
                            # f"{'--force' if force else ''}""
                            ])
    
    # if force:
    #     output = subprocess.run(cmd, universal_newlines=True)
    #     EXIT_CODE = output.returncode
    # else:
    #     EXIT_CODE = ADD_EXIT_ERROR
    # EXIT_CODE = subprocess.run(cmd, universal_newlines=True).returncode if force else MY_EXIT_ERROR

    if EXIT_CODE != 0:
        # now=`date +%F-%T-%Z`
        now = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        # now = datetime.now()
        logger.error(f"Could not complete read_files.py operation ({EXIT_CODE}).")
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

    if not Utils.is_yaml(index_file):
        # if not any([catalog_file.lower().endswith(x) for x in [".yaml", ".yml"]]):
        logger.error(f"{index_file} does not have yaml extension", end="\n\n")
        return ADD_EXIT_ERROR

    if not path.is_file():
        logger.warning(f"{index_file} does not exist. Creating an empty file.")
        path.touch()

    with open(path, "r+") as f:
        all_catalogs = yaml.safe_load(f)
        if not all_catalogs:
            logger.warning(f"{index_file} must containing one key 'catalog' with a list of catalog names.")

            empty = {"catalogs": []}

            yaml.dump(empty, f)
            logger.info(f"Created {index_file}")


def is_valid_file(parser, arg):
    """Argparse function to validate whether the file exists
    TODO: Refactor. This function is c/p in many modules.
    """

    path = Path(arg).resolve()
    if not os.path.exists(path):
        parser.error("The file %s does not exist or cannot be found!" % (arg))
    else:
        # return open(arg, 'r')  # return an open file handle
        return arg


# if __name__ == "__main__":
def cli(args=None):
    if not args:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Add catalogs that this viewer can display", allow_abbrev=True
    )

    parser.add_argument("name", help="Name of new catalog to add", type=str)

    parser.add_argument(
        "source",
        help="Source directory containing data files",
        type=lambda x: is_valid_file(parser, x),
    )

    parser.add_argument(
        "catalog",
        help="Yaml file within `source` containing the catalog entries",
        # type=lambda x: is_valid_file(parser, x)
    )

    parser.add_argument(
        "--LIBRARY",
        default="catalogs",
        required=False,
        help="Library folder for the viewer. This is directory must exist beforehand.",
        type=lambda x: is_valid_file(parser, x),
    )

    parser.add_argument(
        "--LIBRARY-INDEX",
        default="index.yaml",
        required=False,
        help="Index yaml within LIBRARY",
    )

    parser.add_argument(
        "--force",
        dest="force",
        required=False,
        help="Remove before adding catalog even if it already exists",
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

    args = parser.parse_args(args)
    cmd = "add"
    name = args.name
    source_folder = args.source
    catalog_listing = args.catalog
    force = args.force  # default False
    debug = args.debug  # default False

    LIBRARY = args.LIBRARY  # LIBRARY
    LIBRARY_INDEX = args.LIBRARY_INDEX  # LIBRARY_INDEX
    EXIT_CODE = 0

    thisfile = Path(__file__).name
    logger.info(f"{thisfile}: {cmd}:")
    logger.info(str(args).replace("Namespace", "Args"))

    # Check whether `source_folder` exists and `file` has yaml extension
    if not os.path.isdir(source_folder):
        logger.error(f"{source_folder=} is not a directory")
        return ADD_EXIT_ERROR

    p = Path(source_folder, catalog_listing).resolve()

    # if not file.endswith(".yaml") or not file.endswith('.yml'):
    # if not p.is_file() or not any([p.suffix.lower() in [".yaml", ".yml"]]):
    if not is_yaml(p):
        logger.error(f"{catalog_listing=} does not exist or does not have yaml extension.")
        return ADD_EXIT_ERROR

    print(f" {name=}")
    print(f" source_folder={Path(source_folder).resolve()}")
    print(f" file={Path(catalog_listing).resolve()}", end="\n\n")

    # catalog_folder = "catalogs"
    # catalog_file = "catalogs.yaml"

    # check for index
    touch(Path(LIBRARY, LIBRARY_INDEX).resolve())

    # Add catalog
    logger.info(f"add catalog named {name=} with entries {catalog_listing=} from {source_folder=}")
    EXIT_CODE = add(name, source_folder, catalog_listing, 
                    force=force, LIBRARY=LIBRARY, LIBRARY_INDEX=LIBRARY_INDEX)

    logger.info(f"Catalog addition complete\n")
    return EXIT_CODE


if __name__ == "__main__":
    cli()
