# Common Questions

## What is a viewer?
A viewer (this repository) contains all of the files that are used in running the website, as well as manage which catalogs are displayed in it. Keeping the viewer separate from the catalogs allows for easier control in adding and removing catalogs to be shown on the website. 

## What is a catalog and a remote catalog?
A catalog is a collection of files containing information about a group of calls. It contains information such as a sound file, an image file, and information about the pod or call-type. A remote catalog is just a catalog that has been added to a remote git repository for easier collaboration and sharing.

## What is a root catalog?
A root catalog is one of the added remote catalogs that is designated to store the library.yaml file. A symbolic link is created from the root catalog library.yaml to the catalogs directory root. Doing it this way allows for the viewer and catalog to remain totally independent. 



<!-- CUTOFF FOR CREATING REMOTE CATALOGS -->

# Creating Remote Catalogs

## How It Works

Using Git and Git Tags, versions of a catalog can be created and revisited at any time. This is can be a useful feature for chronological releases, i.e. 'June-2022' release, or before any other significant changes. See below for how to get started creating versions and updating them in the viewer

## Creating a Version

Creating a version involves creating a git tag and the optional step of pushing the tag to the remote catalog to make it a part of the repository.

### Creating a Git Tag

Once a state has been reached that you wish to create a version of (new calls added, new time period, etc.), then a git tag must be created. 

To create a git tag make sure all of your changes have been made and committed and execute the command below.

```bash
# Replace version_name with the version name you wish to create. Do not include spaces
# Replace message with the tag message you wish to create. 
git tag -a {version_name} -m {message}
```

Now the tag has been created locally and can be used with the viewer. However, if has not been pushed to the remote catalog so will not be available for others or on other versions of the same catalog. If you wish to add to the remote then continue into the next section, else you may skip to 'Catalog Versions in the Viewer' section.

### (Optional) Pushing Version to Remote Catalog 

Pushing a version to the remote catalog allows for it to become part of the catalog history and available in all instances of the catalog, not just the single instance where it was created. To update the remote catalog to contain the new version, execute the below command.

Pushing a version to remote catalog
```bash
# Replace 'version_name' with the version name specified in the creation of the tag
# If forgotten, all versions can be listed by using executing 'git tag'
git push {version_name}
```

## Catalog Version in the Viewer

Now that a catalog version has been created, it can now be revisited in the catalog viewer, showcasing the state of the catalog at the time of the version creation. If the version must be retrieved from the remote (the version was created in a different instances of the catalog and pushed to the remote), then executing the below command will make it available. If it was created on the same version, disregard the next command and continue to the 'Catalog Version Options' section. 

Retrieving tag pushed to remote catalog
```bash
# Replacing catalog_name with the catalog that has the new version
# For more information on refreshing remote catalogs look at documentation/README_remote_catalogs.md
python code/refresh_remote_catalog.py {catalog_name}
```

### Catalog Version Options

Now that the versions are available on the local catalog, they can be used in the viewer. Details on the options are shown below. 

Base command for working with catalog versions
```bash
# Replace catalog_name with the name of catalog the action should be performed on 
# Specify one of --list, --latest, version_name, where version_name is replaced by the version you wish to checkout
# Note that more than one option cannot be specified. See below for how each one can be used 
python code/catalog_versions.py {catalog_name} [{--list} {--latest} {version_name}]

# This will list all of the versions for the specified catalog_name
python code/catalog_versions.py {catalog_name} --list

# This will revert the catalog to the most up to date commit that has been retrieved locally
python code/catalog_versions.py {catalog_name} --latest

# This will checkout the version 'v2.0' in the catalog specified by catalog_name
python code/catalog_versions.py {catalog_name} v2.0
```


<!-- SECTION FOR WORKING WITH REMOTE CATALOGS IN THE VIEWER -->

# Working With Remote Catalogs in the Viewer

## Adding Remote Catalogs

To add a remote catalog the `git url` and the `yaml file` containing the call data must both be specified

``` bash
# Generic command for adding a remote catalog
python code/add_remote_catalog.py {remote_catalog_git_url} {call_data_yaml_file}

# Example 1: Adds the srkw-call-catalogue-files catalog with the call data file called 'call-catalog.yaml' via git SSH
python code/add_remote_catalog.py git@github.com:sfu-bigdata/srkw-call-catalogue-files.git call-catalog.yaml

# Example 2: Adds the srkw-call-catalogue-files catalog with the call data file called 'whale-call-data.yaml' via git HTTPS
python code/add_remote_catalog.py https://github.com/sfu-bigdata/srkw-call-catalogue-files.git whale-call-data.yaml
```
Note: If this is the first catalog to be added, it will default to being the root catalog and store the library.yaml file. 

## Removing Remote Catalog

To remove a remote catalog the `catalog name` as seen in index.yaml must be specified

``` bash
# Generic command for removing a remote catalog
python code/remove_remote_catalog.py {catalog_name_to_remove}

# Removes the remote catalog from the current viewer
python code/remove_remote_catalog.py srkw-call-catalogue-files 
```
Note: The root catalog cannot be removed and must be changed before removing the catalog

## Setting New Root Catalog

To set a new root catalog the `catalog name` of the new root catalog must be specified

``` bash
# Generic command for setting a new root catalog
python code/set_root_catalog.py {new_root_catalog_name}

# Sets the catalog srkw-call-catalogue-files as the new root catalog
python code/set_root_catalog.py srkw-call-catalogue-files
```

## Getting Root Catalog

To determine which of the remote catalogs is currently set as the root catalog

```bash
python code/get_root_catalog.py
```

## Refreshing Catalogs

To pull any of the remote changes to a catalog and refresh the local catalogs and site the name of the catalog or the --all flag must be specified

```bash
# Command for refreshing all remote catalogs that are added to the viewer
python code/refresh_remote_catalog.py --all

python code/refresh_remote_catalog.py {catalog_name}

# Refreshes the catalog called whale-catalogue
python code/refresh_remote_catalog.py whale-catalogue
```
