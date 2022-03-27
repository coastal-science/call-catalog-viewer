"""Read data folder with .jpg and .wav files, parse filenames

The script expects a folder "SRKW catalogue - J clan" 
under the parent folder of this script's folder.
"""

import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import pandas as pd
import os
import yaml

from yaml.representer import Representer
from yaml.dumper import Dumper
from yaml.emitter import Emitter
from yaml.serializer import Serializer
from yaml.resolver import Resolver


try:
    script_folder = os.path.dirname(__file__)
except NameError:
    script_folder = "."
data_folder = f"{script_folder}simple"
file_name = "call-catalog"

def get_filenames(folder):
    print(folder)
    names = []
    for dirpath, dirnames, filenames in os.walk(folder):
        print(dirpath)
        print(filenames)
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
    ps = pd.Series(filenames)
    df = ps.str.split(".", expand=True).rename(columns={0:"filename",1:"filetype"})

    assert all(df.groupby('filename').size() == 2), "There are unmatched .jpg/.wav file pairs"
    # drop jpg/wav filetype, so each call appears only once in df
    df = df[['filename']].drop_duplicates()
    
    df['thumb'] = df['filename'] + '.jpg'
    df['clan'] = 'J'

    df[['cn','pod','mar']] = df['filename'].str.split("-", n=2, expand=True)
    df['pod_cat'] =  df['pod'].str.findall(r'[J|K|L]')
    #df['html'] = df.apply(make_row_html, axis=1)
    return df
    
def generate_yaml(data_folder, df):
    
    #generate array
    new_df = df.rename(columns={"thumb": "image-file", "cn": "call-type", "mar": "matrilines", "clan": "clan", "pod": "pod", "filename": "wav-file"})
    new_df['population'] = "SRKW"
    new_df['wav-file'] = data_folder + "/" + new_df['wav-file'] + ".wav"
    new_df['image-file'] = data_folder + "/" + new_df['image-file']
    new_df = new_df.drop(['pod_cat'], axis=1)
    
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
        df = df.rename(columns={"call-type": "cn", "matrilines": "mar", "clan": "clan", "pod": "pod", "image-file":"image_file", "wav-file": "wav_file" })
        #print(df)
    return df

def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

def export_file(df, data_folder, file_name, file_format = 'json'):
    if (file_format == 'json'):
        with open(file_name+'.json', 'w') as f:
            f.write(df.to_json(orient='records'))
    elif (file_format == 'csv'):
            df.to_csv(file_name+'.csv')
    elif (file_format == 'yaml'):
        with open(file_name+'.yaml', 'w') as file:
            yaml_dict = generate_yaml(data_folder, df)
            yaml.add_representer(type(None), represent_none)
            documents = yaml.dump(yaml_dict, file)

if __name__ == '__main__':
    """
    example:
        python3 read_files.py call-catalog.yaml <--read resources info from yaml file
        python3 read_files.py simple <--read resources info from the directory containing resources
    """
    inputs = sys.argv[1]
    if len(sys.argv) == 3:
        output = sys.argv[2]
    else:
        output = file_name

    if inputs.endswith('.yaml'):    #read yaml file
        df = read_yaml(inputs)
        export_file(df, data_folder, output, file_format = 'json')
        print("read_files.py: Completed reading yaml file...")
    else:   #read resource directory
        df = read_data_folder(inputs)
        export_file(df, data_folder, output, file_format = 'yaml')
        print("read_files.py: Completed reading resource directory...")
        #print("\n".join(df.apply(make_row_html, axis=1)))