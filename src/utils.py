import yaml
import re
import json
import pandas as pd
import numpy as np
from os.path import dirname, exists
from pathlib import Path
import logging
import yaml

FORMAT = '%(levelname)s - %(asctime)s - %(message)s'
FORMAT_VERBOSE = '%(asctime)s: - %(levelname)s:%(name)s - %(module)s/%(filename)s/%(funcName)s/%(lineno)d:\t%(message)s'

logging.basicConfig(level=logging.INFO, format=FORMAT_VERBOSE)

is_yaml = lambda file: re.search(r"\.ya?ml$", str(file), flags=re.IGNORECASE)  # .yaml or .yml
is_yaml = lambda file: Path(file).resolve().suffix.lower() in [".yaml", ".yml"]  # .yaml or .yml


def is_yaml(file) -> bool:
    return Path(file).resolve().suffix.lower() in [".yaml", ".yml"]  # .yml or .yml

def is_root_catalog(path_to_repo_root):
    '''
    Determines if the catalog is the current root repo
    '''
    return exists(path_to_repo_root + '/library.yaml')
    
def parse_yaml_to_json(path_to_catalogs_directory, yaml_file_path):
    print('Parsing yaml file to prepare for json dump...')
    path_to_repo_root = dirname(yaml_file_path)
    with open(yaml_file_path) as file:
        resources = yaml.safe_load(file)
        
        # will only be true on the first time
        site_details = resources['site-details']
        if is_root_catalog(path_to_repo_root):
            site_details['catalogue']['is_root'] = 'true'
        else:
            site_details['catalogue']['is_root'] = 'false'
                    
        display_info = resources['display']
        display = []
        for value in display_info:
            if type(value) == dict:
                key = list(dict(value).keys())[0]
                
                if key == 'display-one':
                    if value[key] is None or len(value[key]) == 0:
                        display.append({'d1': 'sample'})
                    else:
                        display.append({'d1': value[key][0]})
                    continue
                if key == 'display-two':
                    if value[key] is None or len(value[key]) == 0:
                        display.append({'d2': 'sample'})
                    else:
                        display.append({'d2': value[key][0]})
                    continue
        
        # create a list of lists with the param name as 0th element for easier handling in json
        f = resources['fields']
        fields, filters, sortables = [], [], []
        population = site_details['catalogue']['population']
        if isinstance(population, list) and len(population) > 1:
                        print("There are multiple populations specified in one catalog, please only use one")
                        exit(-1)
        for val in f:
            # if type is dict then it is key in key, value pair and thus is filterable
            if type(val) == dict:
                key = list(dict(val).keys())[0]
                
                if key == 'sortable':
                    if val[key] is None or len(val[key]) == 0:
                        sortables = ['sortable', 'call-type']
                    else:
                        params = [x.split(',') for x in val[key]]
                        arr = [key]
                        for x in params[0]:
                            arr.append(x)
                        sortables = arr
                    continue
                        
                params = [x.split(',') for x in val[key]]
                arr = [key]
                for x in params[0]:
                    arr.append(x)
                    
                # if key == 'population':
                #     population = params[0]

                #     if type(population) == list and len(population) > 1:
                #         print("There are multiple populations specified in one catalog, please only use one")
                #         exit(-1)
                    
                filters.append(arr)
                fields.append(key)
            else:
                fields.append(val)
                
        # Set the required fields for each call
        REQUIRED_FIELDS = ['sample', 'call-type', 'image-file', 'wav-file', 'description-file']
        for field in REQUIRED_FIELDS:
            if field not in fields:
                print(f"Field '{field}' is required")
                exit(-1)

        if len(display) != 2:
            print("The fields 'display-one' and 'display-two' must both be included")
            exit(-1)
            
        # create df and process for json dump
        df = pd.DataFrame.from_dict(resources['calls'])
        ## add it back because the front end depends on it. It expects a flat table.
        df['population'] = population[0]
        
        from os.path import exists
        #check image-file and audio-file
        df['audio_exists'] = df['wav-file'].apply(lambda x: exists(path_to_catalogs_directory + '/' + x))
        df['wav-file'] = df['wav-file'].replace({".wav":".mp3"}, regex=True) # assumption that all wav files will be converted to mp3 in a later step
        df = df.rename(columns={'wav-file':'audio-file'})
        fields[fields.index('wav-file')] = "audio-file" # hack rename
        
        # split any comma separated values, excluding files
        for index, row in df.iterrows():
            for field in fields:
                if field in ['image-file', 'audio-file', 'description-file']:
                    continue
                if (type(row[field]) == str and ',' in row[field]):
                    df.at[index, field] = row[field].split(',')
        
        df['image_exists'] = df['image-file'].apply(lambda x: exists(path_to_catalogs_directory + '/' + x))
        df['image-file'] = df['image-file'].replace({".png":".webp", ".jpeg":".webp", ".jpg":".webp"}, regex=True) # assumption that all images will be converted to webp format in a later step
    
        # extract the filename from the path
        df['filename'] =  df['image-file'].str.split(".", expand=True)[0]
        df['filename'] =  [x.split("/")[-1] for x in df['filename']]

        # keeping for testing
        df['sample'] = df['sample'].apply(lambda x: 0 if np.isnan(x) else str(int(x)))

        if False in df['image_exists'].unique():
            # output all files not found
            no_image_df = df[df['image_exists'] == False]
            print("The following image files are not found:\n", no_image_df[['call-type', 'image-file']])
            
        #output if there is case of file not found in wav
        if False in df['audio_exists'].unique():
            # output all files not found
            no_wav_df = df[df['audio_exists'] == False]
            print("The following wav files are not found:\n", no_wav_df[['call-type', 'audio-file']])
    
        #drop 'image_exists' and 'audio_exists' columns
        df = df.drop(['image_exists', 'audio_exists'], axis=1)
    
        #rename columns for better compatibility in GridPanel
        # call-type is in there for testing purposes
        df = df.rename(columns={"image-file": "image_file", "audio-file": "audio_file", "description-file": "description_file", "call-type": "call_type"})

        # returns the dataframe and the filters dictionary
        print('Successfully parsed yaml file', end='\n\n')
        return (df, population, filters, sortables, display, site_details)
    
def export_to_json(path_to_catalogs_directory, df, population, filters, sortables, display, site_details, file_name, yaml_file):
    print(f'Exporting {file_name} to catalogs/{file_name}.json...')
    with open(path_to_catalogs_directory + '/' + file_name+'.json', 'w') as f:
        data = dict()
        # adding the yaml file to the json since we know the json file name, but we don't know the yaml
        # this allows for much easier access to them
        data['yaml-file'] = yaml_file
        data['site-details'] = site_details 
        # since each catalogue belongs to one population, population is not filterable at this point and can be removed
        data['population'] = population
        data['filters'] = filters
        data['sortable'] = sortables
        data['display'] = display
        data['calls'] = df.to_dict('records')
        json.dump(data, f)
            
    print(f'Successfully exported call data to catalogs/{file_name}.json', end='\n\n')

def add_index_yaml(logger, path_to_catalogs_dir, repo_name):
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