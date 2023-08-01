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
from os.path import dirname, exists, abspath
from json import load
import utils
import logging

logger = logging.getLogger(__name__)

REFRESH_REMOTE_CATALOG_ERROR = -1

def pull_from_remote(path_to_repo, branch):
    '''
    Pulls all of the changes from the remote repository
    '''
    try:
        repo = Repo(path_to_repo)

        # checkout main to avoid weird stuff with git states
        repo.git.checkout(branch)
            
        # Wouldn't work with passing kwargs so doing it manually
        # Fetch the tags first, then any of the other changes
        repo.git.execute(['git', 'fetch', '--tags'])
        repo.git.execute(['git', 'pull', 'origin', branch])
        
    except Exception as e:
        return REFRESH_REMOTE_CATALOG_ERROR

    return 0

def get_list_catalogs(path_to_catalogs_dir):
    with open(path_to_catalogs_dir + '/library.yaml') as f:
        return yaml.safe_load(f)['catalogs']

def get_name_from_url(url):
    '''
    Gets the name of the catalogue from the git url
    '''
    return url[url.rfind('/')+1:len(url)-4]

def update_json_file(path_to_catalogs_dir, repo_name):
    '''
    Update the values in the json with the new yaml data
    '''
    yaml_file = ''
    
    with open(path_to_catalogs_dir + '/' + repo_name + '.json', 'r+') as f:
        data = load(f)
        yaml_file = data['yaml-file']
        
    if yaml_file.endswith('.yaml'):
        df, population, filter, sortables, display, site_details = utils.parse_yaml_to_json(path_to_catalogs_dir, path_to_catalogs_dir + '/' + repo_name + '/' + yaml_file)
        utils.export_to_json(path_to_catalogs_dir, df, population, filter, sortables, display, site_details, repo_name, yaml_file)

def cli(args=None):
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
    
    parser.add_argument(
        '--branch',
        help='Update all of the remote catalogs',
        dest='branch',
        default='main',
        required=False
    )
    
    parser.add_argument(
        '--path',
        default="default",
        required=False,
        help='Optional paramater to override location of catalogs directory. Default will be ../../catalogs/'
    )
    
    args = parser.parse_args(args)
    
    repo_name = args.repo_name
    do_all = args.all
    branch = args.branch
    
    path_to_catalogs_dir = args.path if args.path != "default" else dirname(dirname(abspath(__file__))) + '/catalogs'
    path_to_repo_dir = path_to_catalogs_dir + '/' + repo_name
    
    # a value wasn't passed for the repo name, and do all was not specified
    if (repo_name == 'no_repo' or repo_name == '') and not do_all:
        logger.error('Please specify a catalog name, or use the --all flag to update all catalogs')
        return REFRESH_REMOTE_CATALOG_ERROR
    
    # if there is no library.yaml, we have no remote catalogs added
    if not exists(path_to_catalogs_dir + '/library.yaml'):
        logger.error('No remote catalogs are added. Please add one before updating.')
        return REFRESH_REMOTE_CATALOG_ERROR
    
    # we need to do all of the catalogs
    if do_all:
        logger.info('Updating all catalogs')
        catalog_list = get_list_catalogs(path_to_catalogs_dir)
        
        for catalog in catalog_list:
            name = get_name_from_url(catalog)
            logger.info(f'Pulling changes from {name}...')
            pull_from_remote(path_to_catalogs_dir + '/' + name, branch)
            update_json_file(path_to_catalogs_dir, name)
            logger.info(f'Successfully pulled changes from {name}...')
            
        logger.info('Successfully updated all remote catalogs')
        return 0

    # make sure that the catalog specified exists
    if not exists(path_to_repo_dir):
        logger.error(f'The catalog {repo_name} does not exist. Please add it before updating')
        return REFRESH_REMOTE_CATALOG_ERROR
        
    # go through the list of catalogs and find the one we are looking for
    # if we don't find it, that means it isn't a remote catalog and we print that error
    catalog_list = get_list_catalogs(path_to_catalogs_dir)
    found = False
    
    for catalog in catalog_list:
        if f'{repo_name}.git' in catalog:
            found = True
            break
        
    if not found:
        logger.error(f'The catalog {repo_name} is not a remote catalog')
        return REFRESH_REMOTE_CATALOG_ERROR
    else:
        logger.info(f'Pulling remote changes from {repo_name}...')
        if pull_from_remote(path_to_repo_dir, branch) != 0:
            logger.error(f'There was a problem pulling the changes for repo {repo_name}')
            return REFRESH_REMOTE_CATALOG_ERROR
        update_json_file(path_to_catalogs_dir, repo_name)
        logger.info(f'Successfully pulled all changes and {repo_name} is up to date')

    return 0

if __name__ == '__main__':
    cli()