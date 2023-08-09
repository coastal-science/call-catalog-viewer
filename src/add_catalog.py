import sys
import argparse
from os.path import dirname, exists, isdir
import logging
from pathlib import Path
import utils
from remove_catalog import cli as remove_catalog

logger = logging.getLogger(__name__)

ADD_CATALOG_ERROR = -1

def is_valid_file(parser, arg):
    path = Path(arg).resolve()
    if not exists(path):
        parser.error("The file %s does not exist or cannot be found!" % (arg))
    else:
        return arg

def cli(args=None):
    if not args:
        args = sys.argv[1:]
        
    parser = argparse.ArgumentParser(
        description='Add a catalog to the viewer',
        allow_abbrev=True
    )
    
    parser.add_argument(
        'name',
        help='Name of the new catalog to add',
    )
    
    parser.add_argument(
        'source',
        help='Source directory containing data files',
        type=lambda x: is_valid_file(parser, x)
    )
    
    parser.add_argument(
        'catalog',
        help='The name of yaml file within source directory containing catalog entries'
    )
    
    parser.add_argument(
        '--LIBRARY',
        default=dirname(dirname(__file__)) + '/catalogs',
        required=False,
        help='Optional parameter to override the path to the catalogs folder'
    )
    
    parser.add_argument(
        '--force',
        dest='force',
        required=False,
        help='Remove catalog and add again if it already exists',
        default=False,
        action=argparse.BooleanOptionalAction
    )
    
    args = parser.parse_args(args)
    repo_name = args.name
    path_to_data_folder = Path(args.source).resolve()
    yaml_data_file_name = args.catalog
    path_to_catalog_dir = args.LIBRARY
    path_to_repo_dir = Path(path_to_catalog_dir + '/' + repo_name).resolve()
    force = args.force
    
    thisfile = Path(__file__).name
    logger.info(f"{thisfile}: Add Catalog")
    logger.info(str(args).replace("Namespace", "Args"))
    
    
    if not isdir(path_to_data_folder):
        logger.error(f"{path_to_data_folder=} is not a directory")
        return ADD_CATALOG_ERROR
    
    path_to_catalog_data_file = Path(str(path_to_data_folder), yaml_data_file_name).resolve()
    if not utils.is_yaml(path_to_catalog_data_file):
        logger.error(f"{yaml_data_file_name=} does not exist or does not have yaml extension.")
        return ADD_CATALOG_ERROR
    
    # create or append to index.yaml 
    utils.add_index_yaml(logger, str(path_to_catalog_dir), repo_name)
    
    logger.info(f'add catalog named {repo_name=} with entries {yaml_data_file_name} from {path_to_data_folder}')
    
    # if force, then remove the old catalog
    if force:
        removed = remove_catalog([
            repo_name,
            '--LIBRARY', path_to_catalog_dir
        ])
        if not removed == 0:
            return ADD_CATALOG_ERROR
        
    if exists(path_to_repo_dir):
        logger.error('Catalog already exists in viewer. Use `--force` to reload it')
        return ADD_CATALOG_ERROR
    
    logger.info(f"Creating symlinks for {repo_name}")
    path_to_repo_dir.symlink_to(path_to_data_folder, target_is_directory=True)
    logger.info(f'Created folder {path_to_repo_dir} and linked to {path_to_data_folder}')
    
    logger.info(f'Generating files for the repo {repo_name}')
    try: 
        df, population, filters, sortables, display, site_details = utils.parse_yaml_to_json(path_to_catalog_dir, str(path_to_repo_dir) + '/' + yaml_data_file_name)
    except FileNotFoundError:
        logger.error(f'The yaml file {yaml_data_file_name} does not exist in {repo_name}. Could not complete add operation')
        return ADD_CATALOG_ERROR
    
    try:
        utils.export_to_json(path_to_catalog_dir, df, population, filters, sortables, display, site_details, repo_name, yaml_data_file_name)
    except:
        logger.error(f'Error exporting data to json file for repo {repo_name}. Add operation could not be completed')
        return ADD_CATALOG_ERROR
    
    logger.info(f'Successfully generated json files for repo {repo_name}')
    
    return 0
    
if __name__ == '__main__':
    cli()