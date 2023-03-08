'''
This file is used to remove a catalog that was previously added with add_remote_catalog.py
It will remove the reference to the repo in index.yaml, library.yaml, as well as all the associated files. 
A root catalog cannot be removed. A new root catalog must be set with set_root_catalog.py before removing the catalog.

Usage: python code/remove_remote_catalog.py {catalog_to_remove}
'''
import argparse
from os.path import dirname
from os import remove
from shutil import rmtree
import yaml
import RemoteUtils

CATALOG_PATH = ''

def remove_from_index_yaml(repo_name):
    print(f'Removing repo {repo_name} from catalogs/index.yaml...')
    
    # loading in current list of repos
    index_path = f'{CATALOG_PATH}/index.yaml'
    with open(index_path) as f:
        catalogs = yaml.safe_load(f)
        print(f"Found {catalogs} in catalogs/index.yaml")
        
    if repo_name not in catalogs['catalogs']:
        print(f'Catalog {repo_name} not in {index_path}. Nothing to remove. Exiting')
        exit(-1)
    
    # remove the old repo
    catalogs['catalogs'].remove(repo_name)
    
    # make sure that we don't leave and empty file
    if not catalogs['catalogs']:
        catalogs = {'catalogs': [None]}
        
    with open(index_path, 'w') as f:
        yaml.safe_dump(catalogs, f)
        
    print(f'Successfully removed {repo_name} from index.yaml', end='\n\n')


def remove_from_library_yaml(repo_name):
    print(f'Removing repo {repo_name} from library.yaml...')
    
    path = f'{CATALOG_PATH}/library.yaml'
    found = False
    with open(path, 'r+') as f:
        catalogs = yaml.safe_load(f)
        
        if not catalogs:
            print(f'Nothing to remove in {CATALOG_PATH}/library.yaml. Exiting')
            exit(-1)
        
        current_catalogs = catalogs['catalogs']
        for index, url in enumerate(current_catalogs):
            if f'{repo_name}.git' in url:
                found = True
                current_catalogs.pop(index)
                break
            
    # could not find a matching url        
    if not found:
        print(f'Could not find repo {repo_name} in library.yaml. Please add it before removing it')
        exit(-1)
    
    catalogs['catalogs'] = current_catalogs
    with open(path, 'w') as f:
        yaml.safe_dump(catalogs, f)

    print(f'Successfully removed {repo_name} from library.yaml', end='\n\n')

def remove_files(repo_name):
    print(f'Removing file catalogs/{repo_name}.json...')    
    try:
        remove(f'{CATALOG_PATH}/{repo_name}.json')
    except:
        print(f'Unable to remove file {repo_name}.json. Exiting')
        exit(-1)
    
    print(f'Removing catalogs/{repo_name} directory')
    try:
        rmtree(f'{CATALOG_PATH}/{repo_name}')
    except:
        print(f'Unable to remove direcotyr {CATALOG_PATH}/{repo_name}. Exiting')
        exit(-1)
    
    print(f'Successfully removed all files for repo {repo_name}', end='\n\n')    



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Remove a remote repo from viewer',
        allow_abbrev=True
    )
    
    parser.add_argument(
        'repo_name',
        help='Repo name to be removed'
    )
    
    args = parser.parse_args()
    
    repo_name = args.repo_name
    
    # extract information
    CATALOG_PATH = dirname(dirname(__file__)) + '/catalogs'
    REPO_PATH = f'{CATALOG_PATH}/{repo_name}'
    
    is_root = RemoteUtils.is_root_catalog(CATALOG_PATH + '/library.yaml', REPO_PATH)
    
    if is_root:
        print('Attempting to remove root catalog. Please set a new root catalog before removing this one.')
        exit(-1)
        
    remove_from_index_yaml(repo_name)
    remove_from_library_yaml(repo_name)
    remove_files(repo_name)