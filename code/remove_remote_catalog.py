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

CATALOG_PATH = ''

def is_root_catalog(path):
    return exists(f'{path}/library.yaml')

def remove_from_index_yaml(repo_name):
    print(f'Removing repo \'{repo_name}\' from index.yaml')
    
    path = f'{CATALOG_PATH}/index.yaml'
    with open(path, 'r+') as f:
        catalogs = yaml.safe_load(f)
        
        if not catalogs:
            print(f'Nothing in {CATALOG_PATH}/index.yaml to remove. Exiting')
            exit(-1)
            
        catalogs['catalgs'].remove(repo_name)
        f.seek(0)
        yaml.dump(catalogs, f)
        
    print(f'Succesfully removed {repo_name} from index.yaml')

def remove_from_library_yaml(repo_name, is_url=False):
    print(f'Removing repo {repo_name} from library.yaml')
    
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
    print(f'Successfully added {repo_name} to library.yaml')

def remove_files(repo_name):
    print(f'Removing file {repo_name}.json')
    try:
        remove(f'{CATALOG_PATH}/{repo_name}.json')
    except:
        print(f'Unable to remove file {repo_name}.json. Exiting')
        exit(-1)
    
    print(f'Removing {CATALOG_PATH}/{repo_name} directory')
    try:
        rmtree(f'{CATALOG_PATH}/{repo_name}')
    except:
        print(f'Unable to remove direcotyr {CATALOG_PATH}/{repo_name}. Exiting')
        exit(-1)
    
    print(f'Successfully remove all files for repo {repo_name}')    



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
        print('Attempting to remove root catalog. Please set a new root catalog before removing this one.')
        exit(-1)
        
    remove_from_index_yaml(repo_name)
    remove_from_library_yaml(repo_name)
    remove_files(repo_name)
    # if is_name:
    #     remove_from_name(repo_name)
    # else:
    #     pass