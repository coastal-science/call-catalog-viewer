import argparse
import yaml
from os.path import dirname, abspath, exists, join
from os import makedirs, chmod, symlink
from git import Repo

repo_name = ''
catalogs_path = ''
repo_root_path = ''

def clone_repo(url):
    print(f'Cloning repo {url} into {catalogs_path}/{repo_name}')    
    
    # create repo and set ownership
    repo_directory = catalogs_path + '/' + repo_name
    print(repo_directory)
    makedirs(repo_directory)
    chmod(repo_directory, 0o0777)
    
    # clone the repo into it
    try:
        Repo.clone_from(url, repo_directory)
    except:
        print('Unable to clone repository')
        exit(1)
        
    print(f'Successfully cloned reposity {url}')   
    
def create_library_yaml():
    library_yaml_path = catalogs_path + '/library.yaml'
    if not exists(library_yaml_path):
        print(f'Creating library.yaml in {repo_root_path}')
        with open(repo_root_path + '/library.yaml', 'w') as f:
            catalogs = {'catalogs': [url]}
            yaml.dump(catalogs, f)
            
        print(f'Creating symlink from {repo_root_path}/library.yaml to {catalogs_path}/library.yaml')
        symlink(repo_root_path + '/library.yaml', catalogs_path + '/library.yaml')
        
    else:
        print(f'Appending {url} to {catalogs_path}/library.yaml')
        with open(catalogs_path + '/library.yaml', 'r+') as f:
            catalogs = yaml.safe_load(f)
            catalogs['catalogs'].append(url)
            
            # ensure old data is overwritten not appended to end
            f.seek(0)
            yaml.dump(catalogs, f)
        print(f'Succesfully added {url} to {catalogs_path}/library.yaml')   

def add_index_yaml():
    print(f'Adding {repo_name} to index.yaml')
    path = catalogs_path + '/index.yaml'
    with open(path, 'r+') as f:
        catalogs = yaml.safe_load(f)
        
        # this is the first time we are making index.yaml
        if not catalogs:
            print(f'Creating {catalogs_path}/index.yaml')
            catalogs = {'catalogs': []}
        catalogs['catalogs'].append(repo_name)
        
        f.seek(0)
        yaml.dump(catalogs, f)
        print('Succesfully added {catalogs_path}/index.yaml')  
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Add a remote repo to display in viewer',
        allow_abbrev=True
    )
    
    parser.add_argument(
        'url', 
        help='Url for git repo to display in viewer',
    )
    
    parser.add_argument(
        'yaml_file',
        help='Path to .yaml file containing call data. repo_name/{yaml_file}'
    )
    
    args = parser.parse_args()
    url = args.url
    yaml_file = args.yaml_file
    
    if not yaml_file.endswith('.yaml'):
        print(f'File {yaml_file} does not end with .yaml')
        exit(1)

    # extract catalogs path and repo_name from url and store in global
    catalogs_path = dirname(dirname(abspath(__file__))) + '/catalogs'
    repo_name = url[url.rfind('/')+1:len(url)-4]
    repo_root_path = catalogs_path + '/' + repo_name
    
    if exists(catalogs_path + '/' + repo_name):
        print(f'Unable to add repo {repo_name} as it alreay exists')
        exit(1)
    
    # clone the repository
    clone_repo(url)

    # If the library.yaml exists just add to it
    # else we create repo/library.yaml and symlink to catalogs/library.yaml
    create_library_yaml()
    
    # create/append catalogs/index.yaml
    add_index_yaml()