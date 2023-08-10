from os.path import dirname
from utils import yaml, json, parse_yaml_to_json,  export_to_json

# set this to the path of the catalogs on machine. This assumes location is ../../catalogs/
CATALOGS_PATH = dirname(dirname(__file__)) + '/catalogs'

with open(CATALOGS_PATH + '/index.yaml', 'r') as index_yaml:
    added_catalogs = yaml.safe_load(index_yaml)['catalogs']
    
    for catalog in added_catalogs:
        # open the json file so we can get the name of the yaml-file
        with open(CATALOGS_PATH + f'/{catalog}.json', 'r') as json_file:
            yaml_file_name = json.load(json_file)['yaml-file']
            
        # have extraced all of the information we need, now regenerate files
        df, population, filters, sortables, display, site_details = parse_yaml_to_json(CATALOGS_PATH, CATALOGS_PATH + f'/{catalog}/{yaml_file_name}')
        export_to_json(CATALOGS_PATH, df, population, filters, sortables, display, site_details, catalog, yaml_file_name)