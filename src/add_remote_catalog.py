'''
Used to add a new catalog from a git URL
Clones the catalog into the catalogs/ directory, generates the necessary files, and adds references to library.yaml and index.yaml
If it is the first catalog, it will be set as the root catalog, creating the library.yaml inside of the cloned directory and linking it
Also takes parameter for yaml file, this is the name (or path if not in root of repo) that contains the call data

Usage: python src/add_remote_catalog.py {catalog_git_url} {yaml_file_name}
'''


import argparse
import yaml
from os.path import dirname, abspath, exists
from os import makedirs, chmod, symlink
from git import Repo
import RemoteUtils
import Utils

REPO_NAME = ''
CATALOGS_PATH = ''
REPO_ROOT_PATH = ''
URL = ''

def clone_repo(URL):
    print(f'Cloning repo {URL} into catalogs/{REPO_NAME}...')    
    
    # create repo and set ownership
    repo_directory = CATALOGS_PATH + '/' + REPO_NAME
    makedirs(repo_directory)
    chmod(repo_directory, 0o0777)
    
    # clone the repo into it
    try:
        Repo.clone_from(URL, repo_directory)
    except:
        print('Unable to clone repository')
        exit(1)
        
    print(f'Successfully cloned repository {URL}', end='\n\n')   
    
def create_library_yaml():
    print(f'Creating library.yaml in {REPO_NAME}...')
    
    with open(REPO_ROOT_PATH + '/library.yaml', 'w') as f:
        catalogs = {'catalogs': [URL]}
        yaml.dump(catalogs, f)
    print(f'Successfully created library.yaml in {REPO_NAME}')
    
    print(f'Creating symlink from {REPO_NAME}/library.yaml to catalogs/library.yaml...')
    symlink(REPO_ROOT_PATH + '/library.yaml', CATALOGS_PATH + '/library.yaml')
    print(f'Successfully created symlink to {REPO_NAME}/library.yaml', end='\n\n')


def add_library_yaml():
    print(f'Appending {URL} to catalogs/library.yaml...')
    
    with open(CATALOGS_PATH + '/library.yaml', 'r+') as f:
        catalogs = yaml.safe_load(f)
        catalogs['catalogs'].append(URL)
        
        # ensure that the old data is properly overwritten
        f.seek(0)
        yaml.dump(catalogs, f)
    
    print(f'Successfully added {URL} to catalogs/library.yaml', end='\n\n')
    
def add_index_yaml():
    print(f'Adding {REPO_NAME} to catalogs/index.yaml')
    path = CATALOGS_PATH + '/index.yaml'
    
    # index.yaml does not exist, creating it
    if not exists(path):
        print(f'catalogs/index.yaml does not exist, creating it before adding files....')
        
        with open(path, 'w') as f:
            # catalogs = yaml.safe_load(f)
            catalogs = dict()
            catalogs['catalogs'] = [REPO_NAME]
            
            yaml.dump(catalogs, f)
            
    else: 
        with open(path, 'r+') as f:
            catalogs = yaml.safe_load(f)
            
            catalogs['catalogs'].append(REPO_NAME)
            
            f.seek(0)
            yaml.dump(catalogs, f)
    
    print('Successfully added catalogs/index.yaml', end='\n\n')  
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Add a remote repo to display in viewer',
        allow_abbrev=True
    )
    
    parser.add_argument(
        'URL', 
        help='Url for git repo to display in viewer',
    )
    
    parser.add_argument(
        'yaml_file',
        help='Path to .yaml file containing call data. REPO_NAME/{yaml_file}'
    )
    
    args = parser.parse_args()
    URL = args.URL
    yaml_file = args.yaml_file
    
    if not yaml_file.endswith('.yaml'):
        print(f'File {yaml_file} does not end with .yaml')
        exit(-1)

    # extract catalogs path and REPO_NAME from URL and store in global
    CATALOGS_PATH = dirname(dirname(abspath(__file__))) + '/catalogs'
    REPO_NAME = URL[URL.rfind('/')+1:len(URL)-4]
    REPO_ROOT_PATH = CATALOGS_PATH + '/' + REPO_NAME
    
    if exists(CATALOGS_PATH + '/' + REPO_NAME):
        print(f'Unable to add repo {REPO_NAME} as it already exists')
        exit(-1)
    
    # clone the repository
    clone_repo(URL)

    # If thee library doesn't exist (this is the first one), then create the library.yaml and symlink int
    # else we just append it to the existing library.yaml
    if not exists(CATALOGS_PATH + '/library.yaml'):
        create_library_yaml()
    else:
        add_library_yaml()
    
    # create/append catalogs/index.yaml
    add_index_yaml()
    
    # parse the yaml, creating the json output used by website
    df, population, filter, sortables, display, site_details = RemoteUtils.parse_yaml_to_json(CATALOGS_PATH, REPO_ROOT_PATH + '/' + yaml_file)
    RemoteUtils.export_to_json(CATALOGS_PATH, df, population, filter, sortables, display, site_details, REPO_NAME, yaml_file)
