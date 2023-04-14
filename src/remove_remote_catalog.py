'''
This file is used to remove a catalog that was previously added with add_remote_catalog.py
It will remove the reference to the repo in index.yaml, library.yaml, as well as all the associated files. 
A root catalog cannot be removed. A new root catalog must be set with set_root_catalog.py before removing the catalog.

Usage: python src/remove_remote_catalog.py {catalog_to_remove}
'''
import argparse
from os.path import dirname
from os import remove
from shutil import rmtree
import yaml
import Utils
from pathlib import Path


def remove_from_index_yaml(repo_name):
    '''
    Remove the repo name from the index.yaml to stop it from showing up
    '''
    
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
    '''
    Remove the catalog url from the library.yaml
    '''
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

def remove_catalog_files(repo_name):
    '''
    Remove all of the old files from the catalog that was added
    '''
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
        print(f'Unable to remove directory {CATALOG_PATH}/{repo_name}. Exiting')
        exit(-1)
    
    print(f'Successfully removed all files for repo {repo_name}', end='\n')    

def is_last_catalog():
    path = f'{CATALOG_PATH}/library.yaml'
    
    with open(path, 'r+') as f:
        catalogs = yaml.safe_load(f)
        
        if not catalogs:
            print(f'Nothing to remove in {CATALOG_PATH}/library.yaml. Exiting')
            exit(-1)
        
        return len(catalogs['catalogs']) == 1
    
def remove_root_catalog(repo_name):
    '''
    Get rid of all catalog files as well as index.yaml and library.yaml
    '''
    # removing the catalog specific files and add a newline
    remove_catalog_files(repo_name)
    print()
    
    print('Removing index.yaml and library.yaml from catalogs directory...')
    p = Path(CATALOG_PATH, 'library.yaml')
    p.unlink(missing_ok=True)
    
    remove(CATALOG_PATH + '/index.yaml')
    print('Successfully removed index.yaml and library.yaml')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Remove a remote repo from viewer',
        allow_abbrev=True
    )
    
    parser.add_argument(
        'repo_name',
        help='Repo name to be removed'
    )
    
    parser.add_argument(
        '--force',
        help='Force remove the root catalog. Must be the only catalog in the viewer',
        dest='force',
        default=False,
        required=False,
        action=argparse.BooleanOptionalAction
    )
    
    args = parser.parse_args()
    
    repo_name = args.repo_name
    force_remove = args.force
    
    # extract information
    CATALOG_PATH = dirname(dirname(__file__)) + '/catalogs'
    REPO_PATH = f'{CATALOG_PATH}/{repo_name}'
    
    is_root = Utils.is_root_catalog(REPO_PATH)
    
    if is_root and force_remove:
        if not is_last_catalog():
            print(f'Cannot remove the root catalog {repo_name} while other catalogs are in the viewer. Please remove all other catalogs first.')
            exit(1)
        
        remove_root_catalog(repo_name)
        
    elif is_root and not force_remove:
        print('Attempting to remove root catalog. Please set a new root catalog or specify --force.')
        exit(-1)
    else:
        remove_from_index_yaml(repo_name)
        remove_from_library_yaml(repo_name)
        remove_catalog_files(repo_name)
        
        