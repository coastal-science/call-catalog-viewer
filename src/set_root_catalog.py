'''
This file is used to change the root catalog of the viewer
Setting the root catalog changes where the library.yaml file is stored.
It does not remove any of the data, it just changes the file location and where the symlink points

Usage: python src/set_root_catalog.py {new_root_catalog_name}
'''

from os.path import exists, dirname, realpath, abspath
from os import remove, symlink
from pathlib import Path
import yaml
import argparse
import json
import utils
import sys
from utils import logging

logger = logging.getLogger(__name__)

SET_ROOT_CATALOG_ERROR = -1


def is_remote_catalog(repo_name, catalog_path):
    found = False
    
    if not exists(catalog_path + '/library.yaml'):
        return False
    
    with open(catalog_path + '/library.yaml') as f:
        catalogs = yaml.safe_load(f)
        remotes = catalogs['catalogs']
        
        for remote in remotes:
            if f'{repo_name}.git' in remote:
                found = True
                break
    
    return found
  
def retrieve_old_root_data(catalog_path):
    logger.info('Retrieving data from old root catalog...')
    
    root_path = catalog_path + '/library.yaml'
    with open(root_path, 'r') as f:
        old_data = yaml.safe_load(f)
            
    logger.info('Successfully retrieved old root catalog data')
    return old_data    

def remove_old_library(catalog_path):
    logger.info('Removing symlink and old library.yaml from root catalog')
    link_path = Path(catalog_path + '/library.yaml')
    real_path = realpath(link_path)
    
    # remove symlink
    link_path.unlink(missing_ok=True)
    
    # delete old file
    try:
        remove(real_path)
    except:
        logger.info('There was a problem removing the old library.yaml file. Exiting program')
        return SET_ROOT_CATALOG_ERROR
    
    logger.info('Successfully remove symlink and old library file')
   
def update_old_site_details(repo_name):
    # Open the json file, named repo_name.json
    # Edit the site details so that is_root is false
    
    with open(repo_name + '.json', 'r+') as f:
        logger.info('Updating old site data...')
        data = json.load(f)
        data['site-details']['catalogue']['is_root'] = 'false'
        
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        logger.info('Old data updated')

def update_new_site_details(repo_name, catalog_path):
    # Open the repo_name.json file
    # write the site details with the data that is in the yaml
    # Set the is_root to be true
    
    with open(catalog_path + '/' + repo_name + '.json', 'r+') as f:
        logger.info('Setting new site details...')
        data = json.load(f)
        data['site-details']['catalogue']['is_root'] = 'true'
        
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        logger.info('Site details updated')
 
def create_new_files(repo_name, catalog_path, repo_root_path, old_library_data):
    logger.info(f'Creating library.yaml in {repo_name}...')
    with open(repo_root_path + '/library.yaml', 'w') as f:
        yaml.dump(old_library_data, f)
    logger.info(f'Successfully created library.yaml in {repo_name}')
    
    logger.info(f'Creating symlink to catalogs/library.yaml from {repo_name}/library.yaml...')
    symlink(repo_root_path + '/library.yaml', catalog_path + '/library.yaml')
    logger.info(f'Successfully created symlink to catalogs/library.yaml')


def cli(args=None):
    if not args:
        args = sys.argv[1:]
        
    parser = argparse.ArgumentParser(
        description='Set a new root catalog for viewer',
        allow_abbrev=True
    )
    
    parser.add_argument(
        'repo_name',
        help='Repo name to set as the root catalog'
    )
    
    parser.add_argument(
        '--path',
        default="default",
        required=False,
        help='Optional parameter to override location of catalogs directory. Default will be ../../catalogs/'
    )
    
    args = parser.parse_args(args)
    
    repo_name = args.repo_name
    
    # create variables
    catalog_path = args.path if args.path != "default" else dirname(dirname(abspath(__file__))) + '/catalogs'
    repo_root_path = catalog_path + '/' + repo_name
    
    if repo_name == '':
        logger.error('Please enter a non-empty catalog name')
        return SET_ROOT_CATALOG_ERROR
    
    # check if the repo actually exists
    if not exists(repo_root_path):
        logger.error(f'The repo {repo_name} does not exist, cannot set it as root catalog.')
        return SET_ROOT_CATALOG_ERROR
        
    # check if the repo is already the root catalog
    if utils.is_root_catalog(repo_root_path):
        logger.error(f'The repo {repo_name} is already the root catalog. Doing nothing')
        return SET_ROOT_CATALOG_ERROR
    
    # check if the new repo is a remote one, cannot set a local as a root catalogs
    if not is_remote_catalog(repo_name, catalog_path):
        logger.error(f'The local catalog {repo_name} is not a remote catalog. Cannot be set as the root catalog')
        return SET_ROOT_CATALOG_ERROR
        
    # get the old root repository
    old_repo = dirname(realpath(catalog_path + '/library.yaml'))
    
    # setting the old json site-details is_root to false
    update_old_site_details(old_repo)
    
    # open the old root catalog and store the old data
    old_catalog = retrieve_old_root_data(catalog_path)

    # removing the symlink and deleting the old file
    remove_old_library(catalog_path)
    
    # create new files and symlinks
    create_new_files(repo_name, catalog_path, repo_root_path, old_catalog)
    
    # set the new json site-details is_root as true
    update_new_site_details(repo_name, catalog_path)
    
    logger.info(f'Successfully set {repo_name} as new root catalog')
    return 0
    
if __name__ == '__main__':
    cli()