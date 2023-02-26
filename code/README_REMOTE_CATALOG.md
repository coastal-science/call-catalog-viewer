# Common Questions

## What is a `viewer`?
A `viewer` (this repository) contains all of the files that are used in running the website, as well as manage which catalogs are displyaed in it. Keeping the `viewer` seperate from the `catalogs` allows for easier control in adding and removing catalogs to be shown on the website. 

## What is a `catalog` and a `remote catalog`?
A `catalog` is a collection of files containing infromation about a group of calls. It contains information such as a sound file, an image file, and information about the pod or call-type. A `remote catalog` is just a catalog that has been added to a remote git repository for easier collaboration and sharing.

## What is a `root catalog`?
A `root catalog` is one of the added `remote catalogs` that is designated to store the library.yaml file. A symbolic link is created from the `root catalog` library.yaml to the catalogs directory root. Doing it this way allows for the `viewer` and `catalog` to remain totally independent. 


# Configuring catalogs

## Adding a remote catalogs

To add a remote catalog the `git url` and the `yaml file` containing the call data must both be specified

Adding the srkw-call-catalogue-files catalogue where the call data is stored in call-catalog.yaml:
``` bash
SSH
python code/add_remote_catalog.py git@github.com:sfu-bigdata/srkw-call-catalogue-files.git call-catalog.yaml

HTTPS
python code/add_remote_catalog.py https://github.com/sfu-bigdata/srkw-call-catalogue-files.git call-catalog.yaml
```
Note: If this is the first catalog to be added, it will default to being the root catalog and store the library.yaml file. 

## Removing a remote catalog

To remove a remote catalog the `catalog name` as seen in index.yaml must be specified

Removing the srkw-call-catalogue-files catalogue:
``` bash
python code/remove_remote_catalog.py srkw-call-catalogue-files 
```
Note: The root catalog cannot be removed and must be changed before removing the catalog

## Setting a new root catalog

To set a new root catalog the `catalog name` of the new root catalog must be specified

Setting srkw-call-catalogue-files as the new root catalog:
``` bash
python code/set_root_catalog.py srkw-call-catalogue-files
```

## Refreshing catalogs

### In progress