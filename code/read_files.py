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
data_folder = f"{script_folder}/../SRKW catalogue - J clan"

def get_filenames(folder):
    for dirpath, dirnames, filenames in os.walk(folder):
        break
    return filenames

def read_data_folder(data_folder):
    filenames = get_filenames(data_folder)
    ps = pd.Series(filenames)
    df = ps.str.split(".", expand=True).rename(columns={0:"filename",1:"filetype"})

    assert all(df.groupby('filename').size() == 2), "There are unmatched .jpg/.wav file pairs"
    # drop jpg/wav filetype, so each call appears only once in df
    df = df[['filename']].drop_duplicates()

    df[['callname','pods','matrilines']] = df['filename'].str.split("-", n=2, expand=True)
    return df

df = read_data_folder(data_folder)

def make_row_html(r):
    return (
f"""<figure>
    <img src="{r.filename}.jpg"/>
    Pod: {r.pods}
</figure>""")

print("\n".join(df.apply(make_row_html, axis=1)))
