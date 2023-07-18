import yaml
from pathlib import Path
from os.path import join, exists
from os import symlink, mkdir
     
def dummy_remote_add(catalog_url: str, catalog_name: str, path: Path):    
    # create the directory we need
    mkdir(join(path, catalog_name))
    
    # If our library doesn't exist, create a root catalog, else just append to already there library.yaml
    library_already_exists = exists(join(path, 'library.yaml'))
    if not library_already_exists:
        with open(join(path, catalog_name, 'library.yaml'), 'w') as f:
            catalogs = {'catalogs': [catalog_url]}
            f.seek(0)
            yaml.dump(catalogs, f)
            symlink(join(path, catalog_name, 'library.yaml'), join(path, 'library.yaml'))
    else:
        with open(join(path, 'library.yaml'), 'r+') as f:
            existing_catalogs = yaml.safe_load(f)
            catalogs = existing_catalogs if existing_catalogs is not None else {'catalogs': []}
            catalogs['catalogs'].append(catalog_url)
            f.seek(0)
            yaml.dump(catalogs, f)

    index_already_exists = exists(join(path, 'index.yaml'))
    if not index_already_exists:
        with open(join(path, 'index.yaml'), 'w') as f:
            catalogs = {'catalogs': [catalog_name]}
            f.seek(0)
            yaml.dump(catalogs, f)
    else:
        with open(join(path, 'index.yaml'), 'r+') as f:
            existing_catalogs = yaml.safe_load(f)
            catalogs = existing_catalogs if existing_catalogs is not None else {'catalogs': []}
            catalogs['catalogs'].append(catalog_name)
            f.seek(0)
            yaml.dump(catalogs, f)
                
    # create the json file
    with open(join(path, catalog_name + '.json'), 'a') as f:
        f.write('dummy data for testing')

def dummy_local_add(catalog_name: str, path: Path):
    # need to append index.yaml if it is there, create repo_name directory and json file
    mkdir(join(path, catalog_name))
    
    # create index.yaml and {catalog_name}.json
    with open(join(path, 'index.yaml'), '+a') as f:
        catalogs = yaml.safe_load(f) if yaml.safe_load(f) is not None else {'catalogs': []}
        catalogs['catalogs'].append(catalog_name)
        f.seek(0)
        yaml.dump(catalogs, f)
    
    with open(join(path, catalog_name + '.json'), 'a') as f:
        f.write('dummy data for testing')
        
def make_library(library_name="catalogs"):
    # print(f"make_library:{tmp_path}:")
    d = Path(library_name)
    d.mkdir()
    # print(f"{d}")
    return d


def make_index(lib_name=None, index_name="index.yaml"):
    # print(f"make_index:{index_name=}")
    index = lib_name / index_name
    index.touch()
    index.write_text(yaml.dump(
        {"catalogs": []}
        ))
    print(f"make_index:{index}:")
    return index

def make_existing(lib_name: Path, index: Path, catalog_name="ABCW"):
    """Configure library and index with an existing catalog entry"""

    index.write_text(yaml.dump(
        {"catalogs": [catalog_name]}
        ))  # overwrites previous file
    
    p = (lib_name / catalog_name)
    p.mkdir()
    
    p.touch("call-catalog.yaml")
    (lib_name / f"{catalog_name}.json").touch()
    
    return p