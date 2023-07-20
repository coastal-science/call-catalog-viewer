'''
This file returns the name of the current root catalog
Usage: python src/get_root_catalog.py
'''

from os.path import dirname, exists, realpath, basename
from pathlib import Path
import logging
import argparse

logger = logging.getLogger(__name__)

GET_ROOT_CATALOG_ERROR = -1

def cli(args=None):
    
    parser = argparse.ArgumentParser(
        description='Check which remote catalog is the root',
        allow_abbrev=True
    )
    
    parser.add_argument(
        '--path',
        default="default",
        required=False,
        help='Optional paramater to override location of catalogs directory. Default will be ../../catalogs/'
    )
    
    args = parser.parse_args(args)
    
    catalog_path = args.path if args.path != "default" else dirname(dirname(__file__)) + '/catalogs'
    
    # make sure that the library.yaml file exists, i.e. there is at least one remote catalog added
    if not exists(catalog_path + '/library.yaml'):
        logger.error('No remote catalogs have been added to the viewer. One must be added to have a root catalog.')
        return GET_ROOT_CATALOG_ERROR
        
    # get the dirname of the realpath of the library.yaml file
    library_path = Path(catalog_path + '/library.yaml')
    real_path = realpath(library_path)

    # get the directory that the real_path is stored in, this is the repo that is root
    abs_repo_path = dirname(real_path)
    logger.info(f'{basename(abs_repo_path)} is the root catalog')
    return 0
    
if __name__ == '__main__':
    cli()