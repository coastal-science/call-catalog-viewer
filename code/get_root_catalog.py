'''
This file returns the name of the current root catalog
Usage: python code/get_root_catalog.py
'''

from os.path import dirname, exists, realpath, basename
from pathlib import Path
    
if __name__ == '__main__':
    # get the catalog path
    CATALOG_PATH = dirname(dirname(__file__)) + '/catalogs'
    
    # make sure that the library.yaml file exists, i.e. there is at least one remote catalog added
    if not exists(CATALOG_PATH + '/library.yaml'):
        print('No remote catalogs have been added to the viewer. One must be added to have a root catalog.')
        exit(-1)
        
    # get the dirname of the realpath of the library.yaml file
    library_path = Path(CATALOG_PATH + '/library.yaml')
    real_path = realpath(library_path)

    # get the directory that the real_path is stored in, this is the repo that is root
    abs_repo_path = dirname(real_path)
    print(f'{basename(abs_repo_path)} is the root catalog')