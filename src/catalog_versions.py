'''
Versions 
- Can create a catalogs_versions.py 
- Have option for --list to show all of the tags and remotes that are available
- Have another option for -latest that will automatically update to the latest commit 

Usage 
python src/catalog_versions.py {catalog_name} {version_name}
python src/catalog_versions.py {catalog_name} --list
python src/catalog_versions.py {catalog_name} --latest
'''

import argparse
from os.path import dirname, exists
from git import Repo
import utils
import json
import logging

logger = logging.getLogger(__name__)

CATALOG_VERSIONS_ERROR = -1

def list_versions(repo):
    '''
    List all of the versions available for the repo. Lists all tags that have been pulled to local
    '''   
    if len(repo.tags) == 0:
        logger.error('Not versions available for the catalog. View documentation for instructions to create')
        return CATALOG_VERSIONS_ERROR
        
    for v in repo.tags:
        logger.info(v)

def tag_exists(repo, tag):
    '''
    Check whether a tag exists for a specific repository
    '''   
    if len(repo.tags) == 0:
        logger.error('Not versions available for the catalog. View documentation for instructions to create')
        return CATALOG_VERSIONS_ERROR
    
    found = False
    for t in repo.tags:
        if tag == t.name:
            found = True
            break
    
    return found

def rebuild_files(path_to_catalogs_dir, catalog_name):
    '''
    Update the files after a different tag has been checked out
    '''
    # fetch the yaml file name from the json since we know json, but not yaml all the time. Stops from having to specify
    with open(path_to_catalogs_dir + '/' + catalog_name + '.json') as f:
        data = json.load(f)
        yaml_file = data['yaml-file']
    
    # pass the yaml file to create the new json
    df, population, filter, sortables, display, site_details = utils.parse_yaml_to_json(path_to_catalogs_dir, path_to_catalogs_dir + '/' + catalog_name + '/' + yaml_file)
    utils.export_to_json(path_to_catalogs_dir, df, population, filter, sortables, display, site_details, catalog_name, yaml_file)
    
def cli(args=None):
    parser = argparse.ArgumentParser(
        description='Change the versions of a remote catalogs', 
        allow_abbrev=True
    )
    
    parser.add_argument(
        'catalog_name',
        help='Name of catalog to change versions',
        nargs='?',
        default='no_repo'
    )
    
    parser.add_argument(
        'version',
        help='Name of version to revert/update to',
        nargs='?',
        default='no_version'
    )
    
    parser.add_argument(
        '--list',
        help='List all of the versions for the remote catalog specified',
        dest='list_versions',
        default=False,
        required=False,
        action=argparse.BooleanOptionalAction
    )
    
    parser.add_argument(
        '--latest',
        help='Update to the latest catalog version',
        dest='latest_version',
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
    
    catalog_name = args.catalog_name
    version = args.version
    list_all = args.list_versions
    latest = args.latest_version
    
    path_to_catalogs_dir = args.path if args.path != 'default' else dirname(dirname(__file__)) + '/catalogs'
    
    # catalog name was not specified
    if catalog_name == 'no_repo':
        logger.error('The name of the catalog must be specified')
        return CATALOG_VERSIONS_ERROR
        
    # specified catalog does not exist
    if not exists(path_to_catalogs_dir + '/' + catalog_name):
        logger.error(f'The catalog {catalog_name} does not exist. Please enter a valid catalog name')
        return CATALOG_VERSIONS_ERROR
    
    # we have a valid catalog, so we can set the path and create the repo reference
    ROOT_REPO_PATH = path_to_catalogs_dir + '/' + catalog_name
    catalog_repo = Repo(ROOT_REPO_PATH)
    
    # didn't specify what action to do
    if version == 'no_version' and not list_all and not latest:
        logger.error('Please specify the version or use --list or --latest')
        return CATALOG_VERSIONS_ERROR
        
    # specified more than one action
    if (version != 'no_version' and list_all) or (version != 'no_version' and latest) or (latest and list_all):
        logger.error('Please specify only one of catalog version, --list, or --latest')
        return CATALOG_VERSIONS_ERROR
        
    # we are down to have only one valid action and can handle all of them
    if list_all:
        list_versions(catalog_repo)
    elif latest:
        # checkout the main to avoid weird git states and conflicts
        catalog_repo.git.checkout('main')
        rebuild_files(path_to_catalogs_dir, catalog_name)
    else:
        if not tag_exists(catalog_repo, version):
            logger.error(f'The version {version} does not exist. To view available options use --list')
            return CATALOG_VERSIONS_ERROR
            
        catalog_repo.git.checkout(version)
        rebuild_files(path_to_catalogs_dir, catalog_name)

    return 0

if __name__ == '__main__':
    cli()