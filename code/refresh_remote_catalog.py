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
from os.path import dirname, exists
import pandas as pd
import numpy as np
from json import dump, load

def pull_from_remote(path_to_repo, repo_name):
    repo = Repo(path_to_repo)
    try:
        repo.remotes.origin.pull()
    except:
        print(f'There was a problem pulling the changes for repo {repo_name}')    

def get_list_catalogs():
    with open(CATALOGS_PATH + '/library.yaml') as f:
        return yaml.safe_load(f)['catalogs']

def get_name_from_url(url):
    return url[url.rfind('/')+1:len(url)-4]

def is_root_catalog():
    return exists(f'{REPO_ROOT_PATH}/library.yaml')

def update_json_file(repo_name):
    yaml_file = ''
    
    with open(CATALOGS_PATH + '/' + repo_name + '.json', 'r+') as f:
        data = load(f)
        yaml_file = data['yaml-file']
        
    if yaml_file.endswith('.yaml'):
        df, filter, sortables, display, site_details = parse_yaml_to_json(CATALOGS_PATH + '/' + repo_name + '/' + yaml_file)
        export_to_json(df, filter, sortables, display, site_details, repo_name, yaml_file)

def parse_yaml_to_json(yaml_file):
    print('Parsing yaml file to prepare for json dump...')
    with open(yaml_file) as file:
        resources = yaml.safe_load(file)
        
        # will only be true on the first time
        site_details = resources['site-details']
        if is_root_catalog():
            site_details['is_root'] = 'true'
        else:
            site_details['is_root'] = 'false'
                    
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

def export_to_json(df, filters, sortables, display, site_details, file_name, yaml_file):
    print(f'Exporting {file_name} to catalogs/{file_name}.json...')
    with open(CATALOGS_PATH + '/' + file_name + '.json', 'w') as f:
        json = dict()
        # adding the yaml file to the json since we know the json file name, but we don't know the yaml
        # this allows for much easier access to them
        json['yaml-file'] = yaml_file
        json['site-details'] = site_details            
        json['filters'] = filters
        json['sortable'] = sortables
        json['display'] = display
        json['calls'] = df.to_dict('records')
        dump(json, f)
        
    print(f'Successfuly exported call data to catalogs/{file_name}.json', end='\n\n')

if __name__ == '__main__':
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
    
    args = parser.parse_args()
    
    repo_name = args.repo_name
    do_all = args.all
    
    CATALOGS_PATH = dirname(dirname(__file__)) + '/catalogs'
    REPO_ROOT_PATH = CATALOGS_PATH + '/' + repo_name
    
    # a value wasn't passed for the repo name, and do all was not specified
    if repo_name == 'no_repo' and not do_all:
        print('Please specify a catalog name, or use the --all flag to update all catalogs')
        
    # make sure that there is a library.yaml to check before we break it
    elif not exists(CATALOGS_PATH + '/library.yaml'):
        print('No remote catalogs are added. Please add one before updating.')
        
    # we need to do all of the catalogs
    elif do_all:
        print('Updating all catalogs', end='\n\n')
        catalog_list = get_list_catalogs()
        
        for catalog in catalog_list:
            name = get_name_from_url(catalog)
            print(f'Pulling changes from {name}...')
            pull_from_remote(CATALOGS_PATH + '/' + name, name)
            update_json_file(name)
            print(f'Succesfully pulled changes from {name}...', end='\n\n')
            
        print('Succesfully updated all remote catalogs')

    # make sure that the catalog exists
    elif not exists(REPO_ROOT_PATH):
        print(f'The catalog {repo_name} does not exist. Please add it before updating')
        
    # go through the list of catalogs and find the one we are looking for
    # if we don't find it, that means it isn't a remote catalog and we print that error
    else:
        catalog_list = get_list_catalogs()
        found = False
        
        for catalog in catalog_list:
            if f'{repo_name}.git' in catalog:
                found = True
                break
            
        if not found:
            print(f'The catalog {repo_name} is not a remote catalog')
        else:
            print(f'Pulling remote changes from {repo_name}...')
            pull_from_remote(REPO_ROOT_PATH, repo_name)
            update_json_file()
            print(f'Succesfully pulled all changes and {repo_name} is up to date')