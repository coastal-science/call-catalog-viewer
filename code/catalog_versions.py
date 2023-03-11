'''
Versions 
- Can create a catalogs_versions.py 
- Have option for --list to show all of the tags and remotes that are available
- Have another option for -latest that will automatically update to the latest commit 

Usage 
python code/catalog_versions.py {catalog_name} {version_name}
python code/catalog_versions.py {cadtalog_name} --list
python code/catalog_versions.py {catalog_name} --latest
'''

import argparse
from os.path import dirname, exists
from git import Repo
import RemoteUtils
import json

def list_versions(path_to_catalog):
    repo = Repo(path_to_catalog)
    
    if len(repo.tags) == 0:
        print('Not versions available for the catalog. View documentation for instructions to create')
        exit(-1)
        
    for v in repo.tags:
        print(v)

def tag_exists(path_to_catalog, tag):
    repo = Repo(path_to_catalog)
    
    if len(repo.tags) == 0:
        print('Not versions available for the catalog. View documentation for instructions to create')
        exit(-1)
    
    found = False
    for t in repo.tags:
        if tag == t.name:
            found = True
            break
    
    return found

def checkout_version(path_to_catalog, tag):
    repo = Repo(path_to_catalog)
    
    if 'latest' not in [x.name for x in repo.tags]:
        repo.create_tag('latest')
        
    repo.git.checkout(tag)

def rebuild_files():
    # get the yaml file from the json
    with open(CATALOGS_PATH + '/' + REPO_NAME + '.json') as f:
        data = json.load(f)
        yaml_file = data['yaml-file']
    
    # pass the yaml file to create the new json
    df, filter, sortables, display, site_details = RemoteUtils.parse_yaml_to_json(CATALOGS_PATH, CATALOGS_PATH + '/' + REPO_NAME + '/' + yaml_file)
    RemoteUtils.export_to_json(CATALOGS_PATH, df, filter, sortables, display, site_details, REPO_NAME, yaml_file)

def checkout_latest():
    repo = Repo(ROOT_REPO_PATH)
    
    if 'latest' not in [x.name for x in repo.tags]:
        print(f'Already at the most up to date version of the catalog {REPO_NAME}')
        exit(-1)
        
    repo.git.checkout('latest')
    
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
    
    # we have a valid catalog, so we can set the path
    ROOT_REPO_PATH = CATALOGS_PATH + '/' + catalog_name
    
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
        list_versions(ROOT_REPO_PATH)
    elif latest:
        checkout_latest()
    else:
        if not tag_exists(ROOT_REPO_PATH, version):
            print(f'The version {version} does not exist. To view available options use --list')
            exit(-1)
            
        checkout_version(ROOT_REPO_PATH, version)
        rebuild_files()