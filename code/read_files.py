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


yaml_schema = Map({"call-type": Str(), "clan": Str(), "image-file": Str(), "wav-file": Str(), "matrilines": Null() | Str(), "pod": Str(), "population": Str(), "sample": Null() | Int(), "subclan": Null() | Str(), "subpopulation": Null() | Str()})
"""
try:
    script_folder = os.path.dirname(__file__)
except NameError:
    script_folder = "."
#data_folder = f"{script_folder}simple"
data_folder = ""
file_name = "call-catalog"

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
    
    #generate array
    new_df = df.rename(columns={"thumb": "image-file", "cn": "call-type", "mar": "matrilines", "clan": "clan", "pod": "pod", "filename": "wav-file"})
    new_df['population'] = "SRKW"
    new_df['wav-file'] = data_folder + "/" + new_df['wav-file'] + ".wav" #data_folder + "/" + 
    new_df['image-file'] = data_folder + "/" + new_df['image-file'] #data_folder + "/" + 
    new_df = new_df.drop(['pod_cat'], axis=1)
    #new_df['sample'] = new_df['sample'].astype('float').astype('Int8')  #accommodate None
    
    #print(new_df)
    yaml_dict = { "calls" : new_df.to_dict('records') }
   
    return yaml_dict

def read_yaml(yaml_file):
    with open(yaml_file) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        resource_list = yaml.safe_load(file)
        #print(resource_list)
        df = pd.DataFrame.from_dict(resource_list['calls'])
        #pre-processing and convert to original JSON format
        df['call-type'] = df['call-type']       #assuming call-type now becomes S01 instead of BCS01
        df['pod_cat'] =  df['pod'].str.findall(r'[J|K|L]')
        df['filename'] =  df['image-file'].str.split(".", expand=True)[0]
        df['filename'] =  [x.split("/")[-1] for x in df['filename']]
        df['thumb'] = df['image-file']
        df['sample'] = df['sample'].apply(lambda x: None if np.isnan(x) else str(int(x)))
        
        #check image-file and wav-file
        from os.path import exists
        df['image_exists'] = df['image-file'].apply(lambda x: exists(x))
        df['wav_exists'] = df['wav-file'].apply(lambda x: exists(x))
        #print(df)
        #output if there is case of file not found in image
        if False in df['image_exists'].unique():
            # output all files not found
            # selecting rows based on condition
            no_image_df = df[df['image_exists'] == False]
            print("The following image files are not found:\n", no_image_df[['call-type', 'clan', 'population','image-file']])
            
        #output if there is case of file not found in wav
        if False in df['wav_exists'].unique():
            # output all files not found
            # selecting rows based on condition
            no_wav_df = df[df['wav_exists'] == False]
            print("The following wav files are not found:\n", no_wav_df[['call-type', 'clan', 'population','wav-file']])
    
        #drop 'image_exists' and 'wav_exists' columns
        df.drop(['image_exists', 'wav_exists'], inplace=True, axis=1)
    
        #rename columns
        df = df.rename(columns={"call-type": "cn", "matrilines": "mar", "clan": "clan", "pod": "pod", "image-file":"image_file", "wav-file": "wav_file" })

    return df

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

def export_file(df, data_folder, file_name, file_format = 'json'):
    #df['thumb'] = data_folder + "/" + df['thumb']
    if (file_format == 'json'):
        with open(file_name+'.json', 'w') as f:
            f.write(df.to_json(orient='records'))
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
            

if __name__ == '__main__':
    """
    example:
        python3 read_files.py call-catalog.yaml <--read resources info from yaml file
        python3 read_files.py simple call-catalog yaml<--read resources info from the directory containing resources
    """
    inputs = sys.argv[1]
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

    if inputs.endswith('.yaml'):    #read yaml file
        df = read_yaml(inputs)
        export_file(df, data_folder, output, file_format = file_format)
        print("read_files.py: Completed reading yaml file...")
    else:   #read resource directory
        df = read_data_folder(inputs)
        #print(df)
        export_file(df, inputs, output, file_format = file_format)
        print("read_files.py: Completed reading resource directory...")
        #print("\n".join(df.apply(make_row_html, axis=1)))