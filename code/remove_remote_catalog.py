# will have to pass the remote url or repo name to remove
# Possibly a flag to determine this
# python code/remove_remote_catalog.py ssh@github.....
# python code/remove_remote_catalog.py --name repo-name

# Will steal logic from remove_catalog.py to remove from index.yaml 
# Delete the json generated file
# Will have to do some funky things maybe with library.yaml
# If it is the root catalog, can check through the len of lbrary.yaml, then delete link
# Else it will be very similar to the index.yaml removal, just with library.yaml instead

import argparse
from os.path import dirname, abspath, exists
from os import remove
from shutil import rmtree
import yaml
from pathlib import Path

CATALOG_PATH = ''

def is_root_catalog(path):
    return exists(f'{path}/library.yaml')

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


def remove_from_library_yaml(repo_name, is_url=False):
    print(f'Removing repo {repo_name} from library.yaml...')
    
    path = f'{CATALOG_PATH}/library.yaml'
    with open(path, 'r+') as f:
        catalogs = yaml.safe_load(f)
        
        if not catalogs:
            print(f'Nothing to remove in {CATALOG_PATH}/library.yaml. Exiting')
            exit(-1)
        
        current_catalogs = catalogs['catalogs']
        if is_url:
            if repo_name not in current_catalogs:
                print(f'Could not remove {repo_name} from library.yaml. Please add if before removing')
                exit(-1)
            else:
                current_catalogs.remove(repo_name)
        else:
            found = False
            for index, catalog in enumerate(current_catalogs):
                if f'{repo_name}.git' in catalog:
                    current_catalogs.pop(index)
                    found = True
            
            if not found:
                print(f'Could not find repo {repo_name} in library.yaml. Please add it before removing.')
                exit(-1)

        f.seek(0)
        yaml.dump(current_catalogs, f)
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
        help='Url (or repo name with --name flag) to be remove'
    )
    
    parser.add_argument(
        '--name',
        dest='is_name',
        required=False,
        help='Use flag when specifying repo name, not the git url',
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    
    args = parser.parse_args()
    
    repo_url = args.repo_name
    is_name = args.is_name
    
    # extrac information
    CATALOG_PATH = dirname(dirname(__file__)) + '/catalogs'
    if not is_name:
        repo_name = repo_url[repo_url.refind('/')+1:len(repo_url)-4]
    else:
        repo_name = repo_url
    repo_path = f'{CATALOG_PATH}/{repo_name}'
    
    is_root = is_root_catalog(repo_path)
    
    if is_root:
        print('Ruh roh that is the root catalog')
        # print('Attempting to remove root catalog. Please set a new root catalog before removing this one.')
        # exit(-1)
        
    remove_from_index_yaml(repo_name)
    remove_from_library_yaml(repo_name)
    remove_files(repo_name)