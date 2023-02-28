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
from os.path import dirname, exists

def pull_from_remote(git_url):
    pass

def get_list_catalogs():
    pass

def get_repo_url(repo_name):
    pass

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
    
    name = args.repo_name
    do_all = args.all
    
    CATALOGS_PATH = dirname(dirname(__file__)) + '/catalogs'
    REPO_ROOT_PATH = CATALOGS_PATH + '/' + name
    
    # There is not a repo that has been added yet
    if not exists(CATALOGS_PATH + '/library.yaml'):
        print('No repos were found. Please add one before refreshing')
        exit(-1)
        
    if not exists(REPO_ROOT_PATH):
        print(f'Could not find the catalog {name}. Please add it before refreshing')
        exit(-1)
    
    if name == 'no_repo' and not do_all:
        print('Please specify a catalog name, or use the --all flag to update all catalogs')
        exit(-1)
        
    if do_all:
        print('Getting list of all catalogs')
        catalogs_list = get_list_catalogs()
        print(f'Retrieved {len(catalogs_list)} catalogs to update')
        
        for catalogs in catalogs_list:
            pull_from_remote(catalogs)
    else:
        repo_url = get_repo_url(name)
        pull_from_remote(repo_url)
        
    print(name)
    print(do_all)
    pass