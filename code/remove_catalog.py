"""
usage: remove_catalog.py [-h] [--catalog-folder CATALOG_FOLDER] [--catalog-file CATALOG_FILE]
                         [--force | --no-force] [--debug | --no-debug]
                         name
  
  name                  Name of catalog to remove
  --catalog-folder CATALOG_FOLDER
                        Folder containing catalog data files (default: 'catalogs')
  --catalog-file CATALOG_FILE
                        Yaml file within `folder` containing the catalog entries for the viewer (default: 'catalogs.yaml')
  --force, --no-force   Remove catalog even if it already exists (default: True)

Example:
`python remove_catalog.py srkw-call-catalogue-files`
`python remove_catalog.py srkw-call-catalogue-files catalog catlogs.yaml --force`
"""


import argparse
import os
from pathlib import Path
import re

import yaml


MY_EXIT_ERROR = -1

def remove(catalog_name: str,
           catalog_file: str = "catalogs.yaml",
           catalog_folder: str = "catalogs",
           force: bool = False):
    """Remove the specified catalog 'name' from the viewer.

    Args:
        catalog_name (str): _Name of the catalog to remove. This name must listed in `catalog_file`
        catalog_file (str, optional): Yaml file containing a list of the catalogs. Defaults to "catalog.yaml".
        catalog_folder (str, optional): Parent folder of `catalog_file`. Defaults to "catalogs".
        force (bool, optional): Remove a catalog even if it already exists. Applies to removing symlinks and parsed json  Defaults to False.
    
    Returns:
        bool: True is removal is sucessful. False if 'catalog_name' is already part of {catalog_file}.
    """
    
    catalog = Path(catalog_folder).resolve()
    # print(catalog, catalog/catalog_file)
    
    with open(catalog / catalog_file) as f:
        all_catalogs = yaml.safe_load(f)
        print(f"In {catalog_file} found: {all_catalogs}")

    if catalog_name not in all_catalogs['catalogs']:
        print(f"Catalog named '{catalog_name}' is not part of {catalog_file}, nothing to remove here.")
    
    elif force:
        print(f"Removed '{catalog_name}' from the catalogs listed in {catalog_file}.")
        all_catalogs['catalogs'].remove(catalog_name)
        
        if not all_catalogs: # ensure key and an empty list remains when removing last entry
            all_catalogs['catalogs'] = {'catalogs': [None]}
    
    else:
        print(f"{catalog_name=} is already part of {catalog_file}. Use `--force` to remove anyway.")
        return False


    # remove symlink and parsed json
    print('Removing symlink folders and parsed json')
    p = catalog / catalog_name
    print(f"  {p}")
    p.unlink(missing_ok=force)
    
    p = catalog / (catalog_name + '.json')
    print(f"  {p}")
    p.unlink(missing_ok=force)

    with open(catalog / catalog_file, 'w') as f:
        yaml.dump(all_catalogs, f)

    print('Removal presisted')

    return True

def is_valid_file(parser, arg):
    """ Argparse function to validate whether the file exists
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
        allow_abbrev=True)

    parser.add_argument("name",
                        help="Name of catalog to remove",
                        type=str
                        )

    parser.add_argument("--catalog-folder",
                        default='catalogs',
                        help="Folder containing catalog data files",
                        type=lambda x: is_valid_file(parser, x)
                        )

    parser.add_argument("--catalog-file",
                        default='catalogs.yaml',
                        help="Yaml file within `folder` containing the catalog entries for the viewer",
                        # type=lambda x: is_valid_file(parser, x)
                        )

    parser.add_argument("--force", dest="force", required=False,
                        help="Remove catalog even if it exists",
                        default=True,
                        # action='store_true', # Python <=3.7
                        action=argparse.BooleanOptionalAction # Python 3.7+
                        )

    parser.add_argument("--debug", dest="debug", required=False,
                        help="Print extra debug information for troubleshooting/developing",
                        default=False,
                        # action='store_true', # Python <=3.7
                        action=argparse.BooleanOptionalAction # Python 3.7+
                        )

    args = parser.parse_args()
    print(args)

    cmd = "remove"
    name = args.name
    catalog_folder = args.catalog_folder
    catalog_file = args.catalog_file
    force = args.force # default True
    debug = args.debug # default False

    EXIT_CODE = 0

    thisfile = Path(__file__).name
    print(f"{thisfile}: {cmd}:")

    # Check for existence of `catalog_folder` and `catalog_folder/catalog_file` (and yaml extension)
    if not os.path.isdir(catalog_folder):
        print(f"{thisfile}: {cmd}: {catalog_folder=} is not a directory", end='\n\n')
        exit(MY_EXIT_ERROR)

    p = (Path(catalog_folder).resolve()/catalog_file)
    # print(p)
    
    extension =  re.search(r"\.ya?ml$", p, flags=re.IGNORECASE) # .yaml or .yml
    # if not p.endswith(".yaml") or not p.endswith('.yml'):
    # if not p.is_file() or not any([p.suffix.lower() in [".yaml", ".yml"]]):
    if not extension:
        print(f"{thisfile}: {cmd}: catalog_folder/{catalog_file=} does not exist or does not have yaml extension", end='\n\n')
        exit(MY_EXIT_ERROR)

    print(f" {name=}")
    print(f" folder={Path(catalog_folder).resolve()}")
    print(f" file={Path(catalog_folder).resolve()/catalog_file}", end='\n\n')

    # Remove catalog
    print(f"{thisfile}: remove the catalog named {name=} listed in {catalog_folder}/{catalog_file=}")
    EXIT_CODE = remove(name, catalog_file, catalog_folder, force=force)

    print(f"{thisfile}: {cmd}: Complete", end='\n\n')
    
    exit(EXIT_CODE)
