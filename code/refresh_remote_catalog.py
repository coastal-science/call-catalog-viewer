'''
Need optional arguments, for either --all, or the repo name. 
Assumption is made that it is main, but we can have an option to specify it. 

Repo Name
- Make sure that the repo exists
- Get the remote with the Repo git thing
- Pull from main

--all
- Iterate through each of the remotes found in library.yaml 
- Call the above on each of them
'''

import argparse
from git import Repo
import yaml
from os.path import dirname, exists

def pull_from_remote(git_url):
    pass

def get_list_catalogs():
    with open(CATALOGS_PATH + '/library.yaml') as f:
        return yaml.safe_load(f)['catalogs']
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Updating local changes from a remote repo',
        allow_abbrev=True
    )
    
    parser.add_argument(
        'repo_name',
        help='Name of the catalog to update',
        nargs='?',
        default='no_repo'
    )
    
    parser.add_argument(
        '--all',
        help='Update all of the remote catalogs',
        dest='all',
        default=False,
        required=False,
        action=argparse.BooleanOptionalAction
    )
    
    args = parser.parse_args()
    
    repo_name = args.repo_name
    do_all = args.all
    
    CATALOGS_PATH = dirname(dirname(__file__)) + '/catalogs'
    REPO_ROOT_PATH = CATALOGS_PATH + '/' + repo_name
    
    # a value wasn't passed for the repo name, and do all was not specified
    if repo_name == 'no_repo' and not do_all:
        print('Please specify a catalog name, or use the --all flag to update all catalogs')
        
    # make sure that there is a library.yaml to check before we break it
    elif not exists(CATALOGS_PATH + '/library.yaml'):
        print('No remote catalogs are added. Please add one before updating.')
        
    # we need to do all of the catalogs
    elif do_all:
        print('Updating all catalogs')
        catalog_list = get_list_catalogs()
        
        for catalog in catalog_list:
            print(f'Pulling changes from {catalog}')
            pull_from_remote(catalog)
            
        print('Succesfully updated all remote catalogs')

    # make sure that the catalog exists
    elif not exists(REPO_ROOT_PATH):
        print(f'The catalog {repo_name} does not exist. Please add it before updating')
        
    # go through the list of catalogs and find the one we are looking for
    # if we don't find it, that means it isn't a remote catalog and we print that error
    else:
        catalog_list = get_list_catalogs()
        git_url = ''
        
        for catalog in catalog_list:
            if f'{repo_name}.git' in catalog:
                git_url = catalog
                break
            
        if git_url == '':
            print(f'The catalog {repo_name} is not a remote catalog')
        else:
            print(f'Pulling remote changes from {git_url}...')
            pull_from_remote(git_url)