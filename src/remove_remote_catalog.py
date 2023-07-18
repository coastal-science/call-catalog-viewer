'''
This file is used to remove a catalog that was previously added with add_remote_catalog.py
It will remove the reference to the repo in index.yaml, library.yaml, as well as all the associated files. 
A root catalog cannot be removed. A new root catalog must be set with set_root_catalog.py before removing the catalog.

Usage: python src/remove_remote_catalog.py {catalog_to_remove}
'''
import argparse
from os.path import dirname, exists
from os import remove
from shutil import rmtree
import yaml
import utils
from pathlib import Path
import sys
import logging

logger = logging.getLogger(__name__)

REMOVE_REMOTE_CATALOG_ERROR = -1


def remove_from_index_yaml(path_to_catalog_dir, repo_name):
    '''
    Remove the repo name from the index.yaml to stop it from showing up
    '''
    
    logger.info(f'Removing repo {repo_name} from catalogs/index.yaml...')
    
    # loading in current list of repos
    index_path = f'{path_to_catalog_dir}/index.yaml'
    with open(index_path) as f:
        catalogs = yaml.safe_load(f)
        logger.info(f"Found {catalogs} in catalogs/index.yaml")
        
    if repo_name not in catalogs['catalogs']:
        logger.error(f'Catalog {repo_name} not in {index_path}. Nothing to remove.')
        return REMOVE_REMOTE_CATALOG_ERROR
    
    # remove the old repo
    catalogs['catalogs'].remove(repo_name)
    
    # make sure that we don't leave and empty file
    if not catalogs['catalogs']:
        catalogs = {'catalogs': [None]}
        
    with open(index_path, 'w') as f:
        yaml.safe_dump(catalogs, f)
        
    logger.info(f'Successfully removed {repo_name} from index.yaml\n')
    return 0


def remove_from_library_yaml(path_to_catalog_dir, repo_name):
    '''
    Remove the catalog url from the library.yaml
    '''
    logger.info(f'Removing repo {repo_name} from library.yaml...')
    
    path = f'{path_to_catalog_dir}/library.yaml'
    
    if not exists(path):
        logger.error(f'Library.yaml does not exist. Please add a remote catalog before removing')
        return REMOVE_REMOTE_CATALOG_ERROR
        
    found = False
    with open(path, 'r+') as f:
        catalogs = yaml.safe_load(f)
        
        if not catalogs:
            logger.error(f'Nothing to remove in {path_to_catalog_dir}/library.yaml.')
            return REMOVE_REMOTE_CATALOG_ERROR
        
        current_catalogs = catalogs['catalogs']
        for index, url in enumerate(current_catalogs):
            if f'{repo_name}.git' in url:
                found = True
                current_catalogs.pop(index)
                break
            
    # could not find a matching url        
    if not found:
        logger.error(f'Could not find repo {repo_name} in library.yaml. Please ensure it is a remote catalog')
        return REMOVE_REMOTE_CATALOG_ERROR
    
    catalogs['catalogs'] = current_catalogs
    with open(path, 'w') as f:
        yaml.safe_dump(catalogs, f)

    logger.info(f'Successfully removed {repo_name} from library.yaml\n')
    return 0

def remove_catalog_files(path_to_catalog_dir, repo_name):
    '''
    Remove all of the old files from the catalog that was added
    '''
    logger.info(f'Removing file catalogs/{repo_name}.json...')    
    try:
        remove(f'{path_to_catalog_dir}/{repo_name}.json')
    except:
        logger.error(f'Unable to remove file {repo_name}.json.')
        return REMOVE_REMOTE_CATALOG_ERROR
    
    logger.info(f'Removing catalogs/{repo_name} directory')
    try:
        rmtree(f'{path_to_catalog_dir}/{repo_name}')
    except:
        logger.error(f'Unable to remove directory {path_to_catalog_dir}/{repo_name}.')
        return REMOVE_REMOTE_CATALOG_ERROR
    
    logger.info(f'Successfully removed all files for repo {repo_name}\n')
    return 0 

def is_last_catalog(path_to_catalog_dir):
    path = f'{path_to_catalog_dir}/library.yaml'
    
    with open(path, 'r+') as f:
        catalogs = yaml.safe_load(f)
        
        if not catalogs:
            logger.error(f'Nothing to remove in {path_to_catalog_dir}/library.yaml')
            return False
        
        return len(catalogs['catalogs']) == 1
    
def remove_root_catalog(path_to_catalog_dir, repo_name):
    '''
    Get rid of all catalog files as well as index.yaml and library.yaml
    '''
    # removing the catalog specific files and add a newline
    remove_catalog_files(path_to_catalog_dir, repo_name)
    
    logger.info('Removing index.yaml and library.yaml from catalogs directory...')
    p = Path(path_to_catalog_dir, 'library.yaml')
    p.unlink(missing_ok=True)
    
    remove(path_to_catalog_dir + '/index.yaml')
    logger.info('Successfully removed index.yaml and library.yaml')
    
def cli(args=None):
    if not args:
        args = sys.argv[1:]
        
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
    
    parser.add_argument(
        '--path',
        default="default",
        required=False,
        help='Optional paramater to override location of catalogs directory. Default will be ../../catalogs/'
    )
    
    args = parser.parse_args(args)
    
    repo_name = args.repo_name
    force_remove = args.force
    path_to_catalog_dir = args.path if args.path != "default" else dirname(dirname(__file__)) + '/catalogs'
    cmd = "remote remove"
    
    thisfile = Path(__file__).name
    logger.info(f"{thisfile}: {cmd}:")
    logger.info(str(args).replace("Namespace", "Args"))
    
    if repo_name == "":
        logger.error("Please input a valid repo name to remove")
        return REMOVE_REMOTE_CATALOG_ERROR
    # extract information
    # path_to_catalog_dir = dirname(dirname(__file__)) + '/catalogs'
    path_to_repo_dir = f'{path_to_catalog_dir}/{repo_name}'
    EXIT_CODE = 0
    
    is_root = utils.is_root_catalog(path_to_repo_dir)
    
    if is_root and force_remove:
        if not is_last_catalog(path_to_catalog_dir):
            logger.error(f'Cannot remove the root catalog {repo_name} while other catalogs are in the viewer. Please remove all other catalogs first.')
            return REMOVE_REMOTE_CATALOG_ERROR
        
        remove_root_catalog(path_to_catalog_dir, repo_name)
        
    elif is_root and not force_remove:
        logger.error('Attempting to remove root catalog. Please set a new root catalog or specify --force.')
        return REMOVE_REMOTE_CATALOG_ERROR
    
    else:
        if remove_from_library_yaml(path_to_catalog_dir, repo_name):
            logger.error(f'Error removing from library.yaml. Could not complete removal')
            return REMOVE_REMOTE_CATALOG_ERROR
        
        if remove_from_index_yaml(path_to_catalog_dir, repo_name):
            logger.error('Error removing from index.yaml. Could not complete removal')
            return REMOVE_REMOTE_CATALOG_ERROR
        
        if remove_catalog_files(path_to_catalog_dir, repo_name):
            logger.error('Error removing catalog files. Could not complete removal')
            return REMOVE_REMOTE_CATALOG_ERROR
        
    logger.info(f'Successfully removed remote catalog {repo_name}')
    return EXIT_CODE
        
if __name__ == '__main__':
    cli()