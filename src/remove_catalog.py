"""
usage: remove_catalog.py [-h] [--LIBRARY LIBRARY] [--LIBRARY-INDEX LIBRARY_INDEX] [--force | --no-force]
                         [--debug | --no-debug]
                         name

required arguments:
  name                  Name of catalog to remove

optional arguments:
  --LIBRARY LIBRARY     Folder containing catalog data files. (default: 'catalogs')
  --LIBRARY-INDEX LIBRARY_INDEX
                        Yaml file within `folder` containing the catalog entries for the viewer. (default:
                        'index.yaml')
  --force, --no-force   Remove catalog even if it already exists (default: True)

Example:

`python remove_catalog.py srkw-call-catalogue-files`

`python remove_catalog.py srkw-call-catalogue-files catalog catalogs.yaml --force`
"""


import argparse
import os
import re
from pathlib import Path

import yaml

import Utils

REMOVE_EXIT_ERROR = -1

LIBRARY = "catalogs"
LIBRARY_INDEX = "index.yaml"


def remove(
    catalog_name: str,
    library_index: str = LIBRARY_INDEX,
    library: str = LIBRARY,
    force: bool = False,
):
    """Remove the specified 'catalog_name' from the viewer.

    Args:
        catalog_name (str): _Name of the catalog to remove. This name must listed in `library_index`
        library_index (str, optional): Yaml file containing a list of the catalogs. Defaults to "catalog.yaml".
        library (str, optional): Parent folder of `library_index`. Defaults to "catalogs".
        force (bool, optional): Remove a catalog even if it already exists. Applies to removing symlinks and parsed json  Defaults to False.

    Returns:
        bool: True is removal is successful. False if 'catalog_name' is already part of {library_index}.
    """

    listings = Path(library, library_index).resolve()
    # print(catalog, catalog/library_index)

    with open(listings) as f:
        all_catalogs = yaml.safe_load(f)
        print(f"In {library_index} found: {all_catalogs}")

    if catalog_name not in all_catalogs["catalogs"]:
        print(f"Catalog named '{catalog_name}' is not part of {library_index}, nothing to remove here.")

    elif force:
        # catalog_name already exists and remove anyway.
        print(f"{catalog_name=} already exists in the catalogs listed in {library_index}. Replacing anyway...")
        all_catalogs["catalogs"].remove(catalog_name)

        if not all_catalogs:
            # ensure key and an empty list remains when removing last entry
            all_catalogs["catalogs"] = {"catalogs": [None]}

    else:
        # catalog_name already exists and skip removal.
        print(f"{catalog_name=} is already part of {library_index}. Use `--force` to remove anyway.\n")
        return False

    # remove symlink and parsed json
    print("Removing symlink folders and parsed json")
    p = Path(library, catalog_name)
    print(f"  {p}")
    # If missing_ok is true, FileNotFoundError exceptions will be ignored (same behavior as the POSIX rm -f command).
    p.unlink(missing_ok=True)

    p = Path(library, catalog_name + ".json")
    print(f"  {p}")
    p.unlink(missing_ok=True)

    with open(listings, "w") as f:
        yaml.dump(all_catalogs, f)

    print("Removal persisted")

    return True


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
        description="Remove catalogs available for this viewer to display",
        allow_abbrev=True,
    )

    parser.add_argument("name", help="Name of catalog to remove", type=str)

    parser.add_argument(
        "--LIBRARY",
        default=LIBRARY,
        help=f"Folder containing catalog data files. (default: '{LIBRARY}')",
        type=lambda x: is_valid_file(parser, x),
    )

    parser.add_argument(
        "--LIBRARY-INDEX",
        default=LIBRARY_INDEX,
        help=f"Yaml file within `folder` containing the catalog entries for the viewer. (default: '{LIBRARY_INDEX}')",
        # type=lambda x: is_valid_file(parser, x)
    )

    parser.add_argument(
        "--force",
        dest="force",
        required=False,
        help="Remove catalog even if it already exists",
        default=True,
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

    cmd = "remove"
    name = args.name
    library = args.LIBRARY
    library_index = args.LIBRARY_INDEX
    force = args.force  # default True
    debug = args.debug  # default False

    # LIBRARY = args.LIBRARY  # LIBRARY
    # LIBRARY_INDEX = args.LIBRARY_INDEX  # LIBRARY_INDEX
    EXIT_CODE = 0

    thisfile = Path(__file__).name
    print(f"{thisfile}: {cmd}:")

    # Check for existence of `library` and `library/library_index` (and yaml extension)
    if not os.path.isdir(library):
        print(f"{thisfile}: {cmd}: {library=} is not a directory", end="\n\n")
        exit(REMOVE_EXIT_ERROR)

    p = Path(library, library_index).resolve()
    # print(p)

    if not Utils.is_yaml(p):
        print(f"{thisfile}: {cmd}: library/{library_index=} does not exist or does not have yaml extension.", end="\n\n",)
        exit(REMOVE_EXIT_ERROR)

    print(f" {name=}")
    print(f" folder={Path(library).resolve()}")
    print(f" file={Path(library, library_index).resolve()}", end="\n\n")

    # Remove catalog
    print(f"{thisfile}: remove the catalog named {name=} listed in {library}/{library_index=}")
    EXIT_CODE = remove(name, library_index, library, force=force)

    print(f"{thisfile}: {cmd}: Complete", end="\n\n")

    exit(EXIT_CODE)
