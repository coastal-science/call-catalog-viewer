# How It Works

Using Git and Git Tags, versions of a catalog can be created and revisited at any time. This is can be a useful feature for chronological releases, i.e. 'June-2022' release, or before any other significant changes. See below for how to get started creating versions and updating them in the viewer

# Creating a Version

Creating a version involves creating a git tag and the optional step of pushing the tag to the remote catalog to make it a part of the repository.

## Creating a Git Tag

Once a state has been reached that you wish to create a version of (new calls added, new time period, etc.), then a git tag must be created. 

To create a git tag make sure all of your changes have been made and committed and execute the command below.

```bash
# Replace version_name with the version name you wish to create. Do not include spaces
# Replace message with the tag message you wish to create. 
git tag -a {version_name} -m {message}
```

Now the tag has been created locally and can be used with the viewer. However, if has not been pushed to the remote catalog so will not be available for others or on other versions of the same catalog. If you wish to add to the remote then continue into the next section, else you may skip to 'Catalog Versions in the Viewer' section.

## (Optional) Pushing Version to Remote Catalog 

Pushing a version to the remote catalog allows for it to become part of the catalog history and available in all instances of the catalog, not just the single instance where it was created. To update the remote catalog to contain the new version, execute the below command.

Pushing a version to remote catalog
```bash
# Replace 'version_name' with the version name specified in the creation of the tag
# If forgotton, all versions can be listed by using executing 'git tag'
git push {version_name}
```

# Catalog Version in the Viewer

Now that a catalog verison has been created, it can now be revisited in the catalog viewer, showcasing the state of the catalog at the time of the version creation. If the version must be retrieved from the remote (the version was created in a different instances of the catalog and pushed to the remote), then executing the below command will make it available. If it was created on the same version, disregard the next command and continue to the 'Catalog Version Options' section. 

Retrieving tag pushed to remote catalog
```bash
# Replacing catalog_name with the catalog that has the new version
# For more information on refreshing remote catalogs look at documentation/README_remote_catalogs.md
python code/refresh_remote_catalog.py {catalog_name}
```

## Catalog Version Options

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



