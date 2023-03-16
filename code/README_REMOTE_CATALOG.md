# Common Questions

## What is a `viewer`?
A `viewer` (this repository) contains all of the files that are used in running the website, as well as manage which catalogs are displyaed in it. Keeping the `viewer` seperate from the `catalogs` allows for easier control in adding and removing catalogs to be shown on the website. 

## What is a `catalog` and a `remote catalog`?
A `catalog` is a collection of files containing infromation about a group of calls. It contains information such as a sound file, an image file, and information about the pod or call-type. A `remote catalog` is just a catalog that has been added to a remote git repository for easier collaboration and sharing.

## What is a `root catalog`?
A `root catalog` is one of the added `remote catalogs` that is designated to store the library.yaml file. A symbolic link is created from the `root catalog` library.yaml to the catalogs directory root. Doing it this way allows for the `viewer` and `catalog` to remain totally independent. 


# Configuring catalogs

## Adding Remote Catalogs

To add a remote catalog the `git url` and the `yaml file` containing the call data must both be specified

Adding the srkw-call-catalogue-files catalogue where the call data is stored in call-catalog.yaml:
``` bash
SSH
python code/add_remote_catalog.py git@github.com:sfu-bigdata/srkw-call-catalogue-files.git call-catalog.yaml

HTTPS
python code/add_remote_catalog.py https://github.com/sfu-bigdata/srkw-call-catalogue-files.git call-catalog.yaml
```
Note: If this is the first catalog to be added, it will default to being the root catalog and store the library.yaml file. 

## Removing Remote Catalog

To remove a remote catalog the `catalog name` as seen in index.yaml must be specified

Removing the srkw-call-catalogue-files catalogue:
``` bash
python code/remove_remote_catalog.py srkw-call-catalogue-files 
```
Note: The root catalog cannot be removed and must be changed before removing the catalog

## Setting New Root Catalog

To set a new root catalog the `catalog name` of the new root catalog must be specified

Setting srkw-call-catalogue-files as the new root catalog:
``` bash
python code/set_root_catalog.py srkw-call-catalogue-files
```

## Refreshing Catalogs

To pull any of the remote changes to a catalog and refresh the local catalogs and site the name of the catalog or the --all flag must be specified

Refreshing the srkw-call-catalogue-files remote catalogue
```bash
python code/refresh_remote_catalog.py srkw-call-catalogue-files 
```

Refreshing all of the remote catalogues
```bash
python code/refresh_remote_catalog.py --all
```

## Getting Root Catalog

To determine which of the remote catalogs is currently set as the root catalog

```bash
python code/get_root_catalog.py
```

## Changing Catalog Version

To change the versions of the catalog that is displayed in the viewer. Specify name of catalog and version name, --latest, or --list. See examples below

List all possible catalog versions for the catalog 'example-catalog'. Replace 'example-catalog' with desired catalog name
```bash
python code/catalog_versions.py example-catalog --list
``` 

Checkout version 'v1.0' of catalog 'example-catalog'. Replace 'example-catalog' and 'v1.0' with desired catalog name and version name respectively
```bash
python code/catalog_versions.py example-catalog v1.0
```

Update catalog to the most up to date version available locally. Replace 'example-catalog' with desired catalog name
```bash
python code/catalog_versions.py example-catalog --latest
```
Note: To get remote changes refer to section `Refreshing Catalogs` above.

For more information on catalog versions, view the section `Creating a Catalog Version` below. 

# Creating Catalog Versions

Catalog versions are managed through the use of git tags. Once the catalog is in a state that you wish to create a version of, execute the below command to create a tag, replacing {version_name} and {message} with your desired version name and tag message respectively. 
```bash
git tag -a {version_name} -m {message}
```

After creating a tag, it will be available to be checked out using the above commands in the section `Changing Catalog Versions`. In order to push the tag to the remote catalog repository, the below command can be executed where {version_name} is the version name used in the creation of the tag. 
```bash
git push {version_name}
```

Any versions/tags that are pushed to the remote catalog repository will be automatically updated and available for use with the next refreshing of the catalog as demonstrated in `Refreshing Catalogs`