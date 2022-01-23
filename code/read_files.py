"""Read data folder with .jpg and .wav files, parse filenames

The script expects a folder "SRKW catalogue - J clan" 
under the parent folder of this script's folder.
"""

import pandas as pd
import os

try:
    script_folder = os.path.dirname(__file__)
except NameError:
    script_folder = "."
data_folder = f"{script_folder}SRKW catalogue - J clan"

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

df = read_data_folder(data_folder)
df.to_csv('srkw_call_data.csv')
with open('srkw_call_data.json', 'w') as f:
    f.write(df.to_json(orient='records'))


print("\n".join(df.apply(make_row_html, axis=1)))
