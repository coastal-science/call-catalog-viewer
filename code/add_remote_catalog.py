'''
Used to add a new catalog from a git URL
Clones the catalog into the catalogs/ directory, generates the necessary files, and adds references to library.yaml and index.yaml
If it is the first catalog, it will be set as the root catalog, creating the library.yaml inside of the cloned directory and linking it
Also takes parameter for yaml file, this is the name (or path if not in root of repo) that contains the call data

Usage: python code/add_remote_catalog.py {catalog_git_url} {yaml_file_name}
'''


import argparse
import yaml
from os.path import dirname, abspath, exists, join
from os import makedirs, chmod, symlink
from git import Repo
import pandas as pd
from json import dump
import numpy as np

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
        
    print(f'Successfully cloned reposity {URL}', end='\n\n')   
    
def create_library_yaml():
    print(f'Creating library.yaml in {REPO_NAME}...')
    
    with open(REPO_ROOT_PATH + '/library.yaml', 'w') as f:
        catalogs = {'catalogs': [URL]}
        yaml.dump(catalogs, f)
    print(f'Succesfully created library.yaml in {REPO_NAME}')
    
    print(f'Creating symlink from {REPO_NAME}/library.yaml to catalogs/library.yaml...')
    symlink(REPO_ROOT_PATH + '/library.yaml', CATALOGS_PATH + '/library.yaml')
    print(f'Succesfully created symlink to {REPO_NAME}/library.yaml', end='\n\n')


def add_library_yaml():
    print(f'Appending {URL} to catalogs/library.yaml...')
    
    with open(CATALOGS_PATH + '/library.yaml', 'r+') as f:
        catalogs = yaml.safe_load(f)
        catalogs['catalogs'].append(URL)
        
        # ensure that the old data is properly overwritten
        f.seek(0)
        yaml.dump(catalogs, f)
    
    print(f'Succesfully added {URL} to catalogs/library.yaml', end='\n\n')
    
def add_index_yaml():
    print(f'Adding {REPO_NAME} to catalogs/index.yaml')
    path = CATALOGS_PATH + '/index.yaml'
    with open(path, 'r+') as f:
        catalogs = yaml.safe_load(f)
        
        # this is the first time we are making index.yaml
        if not catalogs:
            print(f'Creating {CATALOGS_PATH}/index.yaml')
            catalogs = {'catalogs': []}
        catalogs['catalogs'].append(REPO_NAME)
        
        f.seek(0)
        yaml.dump(catalogs, f)
    
    print('Succesfully added catalogs/index.yaml', end='\n\n')  
    
def parse_yaml_to_json(yaml_file):
    print('Parsing yaml file to prepare for json dump...')
    with open(yaml_file) as file:
        resources = yaml.safe_load(file)
        
        site_details = resources['site-details']
        
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
        
        # split any comma seperated values, excluding files
        for index, row in df.iterrows():
            for field in fields:
                if field in ['image-file', 'wav-file', 'description-file']:
                    continue
                if (type(row[field]) == str and ',' in row[field]):
                    df.at[index, field] = row[field].split(',')
        
        # extract the filename from the path
        df['filename'] =  df['image-file'].str.split(".", expand=True)[0]
        df['filename'] =  [x.split("/")[-1] for x in df['filename']]

        # keeping for testing
        df['sample'] = df['sample'].apply(lambda x: 0 if np.isnan(x) else str(int(x)))

        #check image-file and wav-file
        from os.path import exists
        df['image_exists'] = df['image-file'].apply(lambda x: exists(CATALOGS_PATH + '/' + x))
        df['wav_exists'] = df['wav-file'].apply(lambda x: exists(CATALOGS_PATH + '/' + x))
    
        if False in df['image_exists'].unique():
            # output all files not found
            no_image_df = df[df['image_exists'] == False]
            print("The following image files are not found:\n", no_image_df[['call-type', 'image-file']])
            
        #output if there is case of file not found in wav
        if False in df['wav_exists'].unique():
            # output all files not found
            no_wav_df = df[df['wav_exists'] == False]
            print("The following wav files are not found:\n", no_wav_df[['call-type', 'wav-file']])
    
        #drop 'image_exists' and 'wav_exists' columns
        df.drop(['image_exists', 'wav_exists'], inplace=True, axis=1)
    
        #rename columns for better compatibility in GridPanel
        # call-type is in there for testing purposes
        df = df.rename(columns={"image-file": "image_file", "wav-file": "wav_file", "description-file": "description_file", "call-type": "call_type"})

    # returns the dataframe and the filters dictionary
    print('Succesfuly paresed yaml file', end='\n\n')
    return (df, filters, sortables, display, site_details)

def export_to_json(df, filters, sortables, display, site_details, file_name):
    print(f'Exporting {file_name} to catalogs/{file_name}.json...')
    with open(CATALOGS_PATH + '/' + file_name+'.json', 'w') as f:
        json = dict()
        json['site-details'] = site_details
        json['filters'] = filters
        json['sortable'] = sortables
        json['display'] = display
        json['calls'] = df.to_dict('records')
        dump(json, f)
        
    print(f'Successfuly exported call data to catalogs/{file_name}.json', end='\n\n')
        
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
        print(f'Unable to add repo {REPO_NAME} as it alreay exists')
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
    df, filter, sortables, display, site_details = parse_yaml_to_json(REPO_ROOT_PATH + '/' + yaml_file)
    export_to_json(df, filter, sortables, display, site_details, REPO_NAME)