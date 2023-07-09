'''
Used to add a new catalog from a git URL
Clones the catalog into the catalogs/ directory, generates the necessary files, and adds references to library.yaml and index.yaml
If it is the first catalog, it will be set as the root catalog, creating the library.yaml inside of the cloned directory and linking it
Also takes parameter for yaml file, this is the name (or path if not in root of repo) that contains the call data

Usage: python src/add_remote_catalog.py {catalog_git_url} {yaml_file_name}
'''


import argparse
from pathlib import Path
import yaml
from os.path import dirname, abspath, exists
from os import makedirs, chmod, symlink
from git import Repo
import utils
from utils import logging
import sys

logger = logging.getLogger(__name__)

REMOTE_ADD_EXIT_ERROR = -1

def clone_repo(path_to_catalogs_dir, repo_name, url):
    logger.info(f'Cloning repo {url} into catalogs/{repo_name}...')
    
    # create repo and set ownership
    repo_directory = path_to_catalogs_dir + '/' + repo_name
    makedirs(repo_directory)
    chmod(repo_directory, 0o0777)
    
    # clone the repo into it
    try:
        Repo.clone_from(url, repo_directory)
    except:
        logger.error(f'Error cloning the git repository')
        return REMOTE_ADD_EXIT_ERROR
    
    logger.info(f'Successfully cloned repository {url}\n')  
    
def create_library_yaml(path_to_catalogs_dir, path_to_repo_dir, repo_name, url):
    logger.info(f'Creating library.yaml in {repo_name}...')
    
    with open(path_to_repo_dir + '/library.yaml', 'w') as f:
        catalogs = {'catalogs': [url]}
        yaml.dump(catalogs, f)
    logger.info(f'Successfully created library.yaml in {repo_name}')
    
    logger.info(f'Creating symlink from {repo_name}/library.yaml to catalogs/library.yaml...')
    symlink(path_to_repo_dir + '/library.yaml', path_to_catalogs_dir + '/library.yaml')
    logger.info(f'Successfully created symlink to {repo_name}/library.yaml\n')


def add_library_yaml(path_to_catalogs_dir, url):
    logger.info(f'Appending {url} to catalogs/library.yaml...')
    
    with open(path_to_catalogs_dir + '/library.yaml', 'r+') as f:
        catalogs = yaml.safe_load(f)
        catalogs['catalogs'].append(url)
        
        # ensure that the old data is properly overwritten
        f.seek(0)
        yaml.dump(catalogs, f)
    
    logger.info(f'Successfully added {url} to catalogs/library.yaml\n')
    
def add_index_yaml(path_to_catalogs_dir, repo_name):
    logger.info(f'Adding {repo_name} to catalogs/index.yaml')
    path = path_to_catalogs_dir + '/index.yaml'
    
    # index.yaml does not exist, creating it
    if not exists(path):
        logger.info(f'catalogs/index.yaml does not exist, creating it before adding files....')
        
        with open(path, 'w') as f:
            # catalogs = yaml.safe_load(f)
            catalogs = dict()
            catalogs['catalogs'] = [repo_name]
            
            yaml.dump(catalogs, f)
            
    else: 
        with open(path, 'r+') as f:
            catalogs = yaml.safe_load(f)
            
            catalogs['catalogs'].append(repo_name)
            
            f.seek(0)
            yaml.dump(catalogs, f)
    
    logger.info('Successfully added catalogs/index.yaml\n')  

def cli(args=None):
    if not args:
        args = sys.argv[1:]
        
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
    url = args.URL
    yaml_file = args.yaml_file
    cmd = 'Remote Add'
    
    thisfile = Path(__file__).name
    logger.info(f"{thisfile}: {cmd}:")
    logger.info(str(args).replace("Namespace", "Args"))
    
    if not yaml_file.endswith('.yaml'):
        logger.error(f'{yaml_file} must be a valid yaml file and end with \'.yaml\'')
        return REMOTE_ADD_EXIT_ERROR

    if not url.endswith('.git'):
        logger.error(f'\'{url}\' must be a valid git repo and end with \'.git\'')
        return REMOTE_ADD_EXIT_ERROR
    
    # extract catalogs path and reponame from url and store in global
    path_to_catalogs_dir = dirname(dirname(abspath(__file__))) + '/catalogs'
    repo_name = url[url.rfind('/')+1:len(url)-4]
    path_to_repo_dir = path_to_catalogs_dir + '/' + repo_name
    
    if exists(path_to_repo_dir):
        logger.error(f'Unable to add repo {repo_name} as it already exists in this catalogue')
        return REMOTE_ADD_EXIT_ERROR
    
    # clone the repository
    clone_repo(path_to_catalogs_dir, repo_name, url)

    # If the library doesn't exist (this is the first one), then create the library.yaml and symlink int
    # else we just append it to the existing library.yaml
    if not exists(path_to_catalogs_dir + '/library.yaml'):
        create_library_yaml(path_to_catalogs_dir, path_to_repo_dir, repo_name, url)
    else:
        add_library_yaml(path_to_catalogs_dir, url)
    
    # create/append catalogs/index.yaml
    add_index_yaml(path_to_catalogs_dir, repo_name)
    
    # parse the yaml, creating the json output used by website
    df, population, filter, sortables, display, site_details = utils.parse_yaml_to_json(path_to_catalogs_dir, path_to_repo_dir + '/' + yaml_file)
    utils.export_to_json(path_to_catalogs_dir, df, population, filter, sortables, display, site_details, repo_name, yaml_file)

if __name__ == '__main__':
    cli()