'''
This file is used to change the root catalog of the viewer
Setting the root catalog changes where the library.yaml file is stored.
It does not remove any of the data, it just changes the file location and where the symlink points

Usage: python code/set_root_catalog.py {new_root_catalog_name}
'''

from os.path import exists, dirname, realpath
from os import remove, symlink
from pathlib import Path
import yaml
import argparse
import json

REPO_NAME = ''
CATALOG_PATH = ''
REPO_ROOT_PATH = ''


def is_remote_catalog(repo_name):
    found = False
    with open(CATALOG_PATH + '/library.yaml') as f:
        catalogs = yaml.safe_load(f)
        remotes = catalogs['catalogs']
        
        for remote in remotes:
            if f'{repo_name}.git' in remote:
                found = True
                break
    
    return found
    
def is_root_catalog(repo_path):
    return exists(f'{repo_path}/library.yaml')
  
def retrieve_old_root_data():
    print(f'Retrieving data from old root catalog...')
    
    root_path = CATALOG_PATH + '/library.yaml'
    with open(root_path, 'r') as f:
        old_data = yaml.safe_load(f)
            
    print('Successfully retrieved old root catalog data', end='\n\n')
    return old_data    

def remove_old_library():
    print('Removing symlink and old library.yaml from root catalog')
    link_path = Path(CATALOG_PATH + '/library.yaml')
    real_path = realpath(link_path)
    
    # remove symlink
    link_path.unlink(missing_ok=True)
    
    # delete old file
    try:
        remove(real_path)
    except:
        print('There was a problem removing the old library.yaml file. Exiting program')
        exit(-1)
    
    print('Successfully remove symlink and old library file', end='\n\n')
   
def update_old_site_details(repo_name):
    # Open the json file, named repo_name.json
    # Edit the site details so that is_root is false
    
    with open(repo_name + '.json', 'r+') as f:
        print('Updating old site data...')
        data = json.load(f)
        data['site-details']['catalogue']['is_root'] = 'false'
        
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        print('Old data updated')

def update_new_site_details():
    # Open the repo_name.json file
    # write the site details with the data that is in the yaml
    # Set the is_root to be true
    
    with open(CATALOG_PATH + '/' + REPO_NAME + '.json', 'r+') as f:
        print('Setting new site details...')
        data = json.load(f)
        data['site-details']['catalogue']['is_root'] = 'true'
        
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        print('Site details updated')
 
def create_new_files(old_library_data):
    print(f'Creating library.yaml in {REPO_NAME}...')
    with open(REPO_ROOT_PATH + '/library.yaml', 'w') as f:
        yaml.dump(old_library_data, f)
    print(f'Successfully created library.yaml in {REPO_NAME}')
    
    print(f'Creating symlink to catalogs/library.yaml from {REPO_NAME}/library.yaml...')
    symlink(REPO_ROOT_PATH + '/library.yaml', CATALOG_PATH + '/library.yaml')
    print(f'Successfully created symlink to catalogs/library.yaml', end='\n\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Set a new root catalog for viewer',
        allow_abbrev=True
    )
    
    parser.add_argument(
        'repo_name',
        help='Repo name to set as the root catalog'
    )
    
    args = parser.parse_args()
    
    REPO_NAME = args.repo_name
    
    # create variables
    CATALOG_PATH = dirname(dirname(__file__)) + '/catalogs'
    REPO_ROOT_PATH = CATALOG_PATH + '/' + REPO_NAME
    
    # check if the repo actually exists
    if not exists(REPO_ROOT_PATH):
        print(f'The repo {REPO_NAME} does not exist, cannot set it as root catalog.')
        exit(-1)
        
    # check if the repo is already the root catalog
    if is_root_catalog(REPO_ROOT_PATH):
        print(f'The repo {REPO_NAME} is already the root catalog. Doing nothing')
        exit()
    
    # check if the new repo is a remote one, cannot set a local as a root catalogs
    if not is_remote_catalog(REPO_NAME):
        print(f'The local directory {REPO_NAME} is not a remote catalog. Cannot be set as the root catalog')
        exit(-1)
        
    # get the old root repository
    old_repo = dirname(realpath(CATALOG_PATH + '/library.yaml'))
    
    # setting the old json site-details is_root to false
    update_old_site_details(old_repo)
    
    # open the old root catalog and store the old data
    old_catalog = retrieve_old_root_data()

    # removing the symlink and deleting the old file
    remove_old_library()
    
    # create new files and symlinks
    create_new_files(old_catalog)
    
    # set the new json site-details is_root as true
    update_new_site_details()
    
    print(f'Successfully set {REPO_NAME} as new root catalog')