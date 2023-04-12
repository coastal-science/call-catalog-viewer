'''
Versions 
- Can create a catalogs_versions.py 
- Have option for --list to show all of the tags and remotes that are available
- Have another option for -latest that will automatically update to the latest commit 

Usage 
python code/catalog_versions.py {catalog_name} {version_name}
python code/catalog_versions.py {catalog_name} --list
python code/catalog_versions.py {catalog_name} --latest
'''

import argparse
from os.path import dirname, exists
from git import Repo
import RemoteUtils
import json

def list_versions(repo):
    '''
    List all of the versions available for the repo. Lists all tags that have been pulled to local
    '''   
    if len(repo.tags) == 0:
        print('Not versions available for the catalog. View documentation for instructions to create')
        exit(-1)
        
    for v in repo.tags:
        print(v)

def tag_exists(repo, tag):
    '''
    Check whether a tag exists for a specific repository
    '''   
    if len(repo.tags) == 0:
        print('Not versions available for the catalog. View documentation for instructions to create')
        exit(-1)
    
    found = False
    for t in repo.tags:
        if tag == t.name:
            found = True
            break
    
    return found

def rebuild_files():
    '''
    Update the files after a different tag has been checked out
    '''
    # fetch the yaml file name from the json since we know json, but not yaml all the time. Stops from having to specify
    with open(CATALOGS_PATH + '/' + REPO_NAME + '.json') as f:
        data = json.load(f)
        yaml_file = data['yaml-file']
    
    # pass the yaml file to create the new json
    df, filter, sortables, display, site_details = RemoteUtils.parse_yaml_to_json(CATALOGS_PATH, CATALOGS_PATH + '/' + REPO_NAME + '/' + yaml_file)
    RemoteUtils.export_to_json(CATALOGS_PATH, df, filter, sortables, display, site_details, REPO_NAME, yaml_file)
    
if __name__ == '__main__':
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
    
    args = parser.parse_args()
    
    catalog_name = args.catalog_name
    version = args.version
    list_all = args.list_versions
    latest = args.latest_version
    
    CATALOGS_PATH = dirname(dirname(__file__)) + '/catalogs'
    REPO_NAME = catalog_name
    
    # catalog name was not specified
    if catalog_name == 'no_repo':
        print('The name of the catalog must be specified')
        exit(-1)
        
    # specified catalog does not exist
    if not exists(CATALOGS_PATH + '/' + catalog_name):
        print(f'The catalog {catalog_name} does not exist. Please enter a valid catalog name')
        exit(-1)
    
    # we have a valid catalog, so we can set the path and create the repo reference
    ROOT_REPO_PATH = CATALOGS_PATH + '/' + catalog_name
    catalog_repo = Repo(ROOT_REPO_PATH)
    
    # didn't specify what action to do
    if version == 'no_version' and not list_all and not latest:
        print('Please specify the version or use --list or --latest')
        exit(-1)
        
    # specified more than one action
    if (version != 'no_version' and list_all) or (version != 'no_version' and latest) or (latest and list_all):
        print('Please specify only one of catalog version, --list, or --latest')
        exit(-1)
        
    # we are down to have only one valid action and can handle all of them
    if list_all:
        list_versions(catalog_repo)
    elif latest:
        # checkout the main to avoid weird git states and conflicts
        catalog_repo.git.checkout('main')
        rebuild_files()
    else:
        if not tag_exists(catalog_repo, version):
            print(f'The version {version} does not exist. To view available options use --list')
            exit(-1)
            
        catalog_repo.git.checkout(version)
        rebuild_files()
