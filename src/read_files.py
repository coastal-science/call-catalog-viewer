"""Read data folder with .jpg and .wav files, parse filenames

The script expects a folder "SRKW catalogue - J clan" 
under the parent folder of this script's folder.
"""

import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import pandas as pd
import os
import yaml
import numpy as np

from yaml.representer import Representer
from yaml.dumper import Dumper
from yaml.emitter import Emitter
from yaml.serializer import Serializer
from yaml.resolver import Resolver

# for strictyaml
#from ensure import Ensure
"""
from strictyaml import as_document


from strictyaml import load, Map, Str, Int, Seq, YAMLError
from strictyaml.scalar import ScalarValidator

YAML_NULL = ["null", "Null", "NULL", "~"]

class Null(ScalarValidator):

    #'null'->None

    @staticmethod
    def validate_scalar(chunk):
        if any([chunk.contents == n for n in YAML_NULL]):
            return None
        chunk.expecting_but_found(f"when expecting any of {YAML_NULL}")


yaml_schema = Map({"call-type": Str(), "clan": Str(), "image-file": Str(), "audio-file": Str(), "matrilines": Null() | Str(), "pod": Str(), "population": Str(), "sample": Null() | Int(), "subclan": Null() | Str(), "subpopulation": Null() | Str()})
"""

try:
    script_folder = os.path.dirname(__file__)
except NameError:
    script_folder = "."
#data_folder = f"{script_folder}simple"
data_folder = ""
file_name = "call-catalog"
library = "catalogs"

def get_filenames(folder):
    #print(folder)
    names = []
    for dirpath, dirnames, filenames in os.walk(folder):
        #print(dirpath)
        #print(filenames)
        for name in filenames:
            names.append(name)
        break
    return names

def make_row_html(r):
    return (
f"""<figure>
    <img src="{r.filename}.jpg"/>
    Pod: {r.pod}
</figure>""")

def read_data_folder(data_folder):
    filenames = get_filenames(data_folder)
    #print(filenames)
    ps = pd.Series(filenames)
    df = ps.str.split(".", expand=True).rename(columns={0:"filename",1:"filetype"})

    assert all(df.groupby('filename').size() == 2), "There are unmatched .jpg/.wav file pairs"
    # drop jpg/wav filetype, so each call appears only once in df
    df = df[['filename']].drop_duplicates()
    
    df['thumb'] = df['filename'].apply(lambda x: x + '.jpg' if x + '.jpg' in filenames else (x + '.png' if x + '.png' in filenames else ''))
    #df['thumb'] = df['filename'] + '.jpg'
    df['clan'] = 'J'
    df['mar'] = None 
    df['subpopulation'] = None
    df['subclan'] = None

    df[['cn','pod','sample']] = df['filename'].str.split("-", n=2, expand=True)

    df['pod_cat'] =  df['pod'].str.findall(r'[J|K|L]')
    #df['html'] = df.apply(make_row_html, axis=1)
    return df
    
def generate_yaml(data_folder, df):
    
    # TODO: Specifics in the creation of the yaml files
    #generate array
    new_df = df.rename(columns={"thumb": "image-file", "cn": "call-type", "mar": "matrilines", "clan": "clan", "pod": "pod", "filename": "audio-file"})
    new_df['population'] = "SRKW"
    new_df['audio-file'] = data_folder + "/" + new_df['audio-file'] + ".wav" #data_folder + "/" + 
    new_df['image-file'] = data_folder + "/" + new_df['image-file'] #data_folder + "/" + 
    new_df = new_df.drop(['pod_cat'], axis=1)
    print("Generate yaml called")
    #new_df['sample'] = new_df['sample'].astype('float').astype('Int8')  #accommodate None
    
    #print(new_df)
    yaml_dict = { "calls" : new_df.to_dict('records') }
   
    return yaml_dict

def split_params(fields, row):
    for field in fields:
        print(field)


def read_yaml(yaml_file):
    with open(yaml_file) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        resource_list = yaml.safe_load(file) # generates a dictionary from the yaml file
        # print(resource_list)

        site_details = resource_list['site-details']
        
        d = resource_list['display']
        display = list()
        for val in d:
            if type(val) == dict:
                key = list(dict(val).keys())[0]
                
                if key == 'display-one':
                    if val[key] is None or len(val[key]) == 0:
                        display.append({'d1': 'sample'})
                    else:
                        display.append({'d1': val[key][0]})
                    continue
                    
                if key == 'display-two':
                    if val[key] is None or len(val[key]) == 0:
                        display.append({'d2': 'sample'})
                    else:
                        display.append({'d2': val[key][0]})
                    continue
                    

        # create a list of lists with the parameter name as 0th element and everything else after
        #  makes for easier handling in json than dictionaries with unknown keys
        f = resource_list['fields'] # is a list a dictionary objects containing all of the filterable datas
        fields = list()
        filters = list()
        sortables = list()
        for val in f:
            if type(val) == dict: # this means that it is filterable item
                key = list(dict(val).keys())[0]
                
                if key == 'sortable':
                    if val[key] is None or len(val[key])  == 0:
                        sortables = ['sortable', 'call-type']
                    else:
                        params = [x.split(',') for x in val[key]]
                        arr = [key]
                        for x in params[0]:
                            arr.append(x)
                        sortables = arr
                    continue
                
                params = [x.split(',') for x in val[key]] # options are put in as a comma separated string. This splits them
                arr = [key]
                for x in params[0]:
                    arr.append(x)
                filters.append(arr) # adds arr with structures ['field_name', 'value1', 'value2'...] to the filters list
                fields.append(key)
            else:
                fields.append(val)

        REQUIRED_FIELDS = ['sample', 'call-type', 'image-file', 'wav-file', 'description-file']
        for field in REQUIRED_FIELDS:
            if field not in fields:
                print(f"Field '{field}' is required")
                exit(-1)
        fields[fields.index('wav-file')] = "audio-file" # hack rename

        if len(display) != 2:
            print("Fields 'display-one' and 'display-two' must be included")
            exit(-1)
        # What can I do with these fields???
        # OPTIONAL_FIELDS = ['call-type', 'pod', 'clan']
        # for field in OPTIONAL_FIELDS:
        #     if field not in fields:
        #         print(f"Field '{field}' can be specified")

        # pre-processing and convert to original JSON format
        # create dataframe with all of the call data and do special handling form image-file, audio-file and description-file
        df = pd.DataFrame.from_dict(resource_list['calls'])
        df['wav-file'] = df['wav-file'].replace({".wav":".mp3"}, regex=True)
        df = df.rename(columns={'wav-file':'audio-file'})

        # need to iterate through all of the rows in DataFrame to split any values that may exist. J,L -> [J, L]
        for index, row in df.iterrows():
            for field in fields:
                if field in ['image-file', 'audio-file']:
                    continue # don't want to change anything with the image or sound files. They could be valid commas
                if (type(row[field]) == str and ',' in row[field]):
                    df.at[index,field] = row[field].split(',')

        # extract the filename from the path
        df['image-file'] = df['image-file'].replace({".png":".webp", ".jpeg":".webp", ".jpg":".webp"}, regex=True)
        df['filename'] =  df['image-file'].str.split(".", expand=True)[0]
        df['filename'] =  [x.split("/")[-1] for x in df['filename']]


        # keeping for testing
        df['sample'] = df['sample'].apply(lambda x: 0 if np.isnan(x) else str(int(x)))

        #check image-file and audio-file
        from os.path import exists
        df['image_exists'] = df['image-file'].apply(lambda x: exists(library + '/' + x))
        df['audio_exists'] = df['audio-file'].apply(lambda x: exists(library + '/' + x))
        #print(df)
        #output if there is case of file not found in image
        if False in df['image_exists'].unique():
            # output all files not found
            # selecting rows based on condition
            no_image_df = df[df['image_exists'] == False]
            print("The following image files are not found:\n", no_image_df[['call-type', 'image-file']])
            
        #output if there is case of file not found in wav
        if False in df['audio_exists'].unique():
            # output all files not found
            # selecting rows based on condition
            no_audio_df = df[df['audio_exists'] == False]
            print("The following audio files are not found:\n", no_audio_df[['call-type', 'audio-file']])
    
        #drop 'image_exists' and 'wav_exists' columns
        df.drop(['image_exists', 'audio_exists'], inplace=True, axis=1)
    
        #rename columns for better compatibility in GridPanel
        # call-type is in there for testing purposes
        df = df.rename(columns={"image-file": "image_file", "audio-file": "audio_file", "description-file": "description_file", "call-type": "call_type"})

    # returns the dataframe and the filters dictionary
    return (df, filters, sortables, display, site_details)

def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

def str_presenter(dumper, data):
    try:
        dlen = len(data.splitlines())
        if (dlen > 1):
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        elif ((len(data) <= 2) and (data.isdigit())):
            return dumper.represent_scalar('tag:yaml.org,2002:int', data)
    except TypeError as ex:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

def export_file(df, data_folder, filters, sortables, display, site_details, file_name, file_format = 'json'):
    from json import dump
    #df['thumb'] = data_folder + "/" + df['thumb']
    if (file_format == 'json'):
        with open(file_name+'.json', 'w') as f: # this is where it writes to the json.
            json = dict()
            json['site-details'] = site_details
            json['filters'] = filters
            json['sortable'] = sortables
            json['display'] = display
            json['calls'] = df.to_dict('records')
            dump(json, f)
    elif (file_format == 'csv'):
            df.to_csv(file_name+'.csv')
    elif (file_format == 'yaml'):
        with open(file_name+'.yaml', 'w') as file:
            yaml_dict = generate_yaml(data_folder, df)
            
            yaml.add_representer(type(None), represent_none)
            #yaml.add_representer(type(np.int8(None)), represent_none)
            yaml.add_representer(str, str_presenter)
            documents = yaml.dump(yaml_dict, file)
            
            # Can also use regular dict if an arbitrary ordering is ok
            #print(yaml_dict['calls'])
            
            #yaml_records = load(yaml_dict['calls'], yaml_schema)
            #yaml_text = as_document(yaml_dict['calls'], yaml_schema)
            #yaml_text.as_yaml()
            #file.write(yaml_text.as_yaml())
            

# if __name__ == '__main__':
def main(args=None):
    """
    example:
        python3 read_files.py call-catalog.yaml <--read resources info from yaml file
        python3 read_files.py simple call-catalog yaml<--read resources info from the directory containing resources
    """

    inputs = sys.argv[1] # inputs is path to index file in the catalog to be added
    if len(sys.argv) == 3:
        output = sys.argv[2]
        file_format = 'json'
        print("read_files.py: Generate json file...")
    elif len(sys.argv) == 4:
        output = sys.argv[2]
        file_format = sys.argv[3]
        print("read_files.py: Generate yaml file...")
    else:
        output = file_name
        file_format = 'json'
        print("read_files.py: Generate json file...")

    if inputs.endswith('.yaml'):    # input file is a yaml. Read it
        df, filter, sortables, display, site_details = read_yaml(inputs)
        export_file(df, data_folder, filter, sortables, display, site_details, output, file_format = file_format)
        print("read_files.py: Completed reading yaml file...")
    else:   #read resource directory
        df = read_data_folder(inputs)
        #print(df)
        export_file(df, inputs, output, file_format = file_format)
        print("read_files.py: Completed reading resource directory...")
        #print("\n".join(df.apply(make_row_html, axis=1)))
    return 0

def cli(args=None):
    try:
        if not args:
            args = sys.argv[1:]
        else:
            sys.argv = [sys.argv[0]] + args
        return main(args)
    except Exception as err:
        print(err.with_traceback())
        return -1    
    

if __name__ == '__main__':
    cli()
    