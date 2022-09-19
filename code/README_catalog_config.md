# Catalog configuration

A `catalog-viewer` can host parallel catalogs. To add or remove catalogs to a viewer (`cd /var/www/html/catalog-viewer/`) use the commands:

```bash
$ python code/add_catalog.py ...
$ python code/remove_catalog.py ...
$ python code/catalog_config.py {add,remove} ...
```

Further details and examples are documented in their `--help` and docstring.

|Equivalent | |
|---|---|
| `python code/catalog_config.py add ...` | `python code/add_catalog.py ...` |
| `python code/catalog_config.py remove ...` | `python code/remove_catalog.py ...` |

## `add` a catalog

The required arguments to `add` a catalog are 
- \<`name`\> of the new catalog, 
- \<`source-folder`\> where media files are, a symbolic link to this target is created within `catalogs` (aka `LIBRARY` and `LIBRARY-INDEX.yaml`)
- \<`index`\> a yaml file within _\<source-folder\>_ that contains the listing of catalog entries.

Add the srkw-call-catalogue with:
```bash
python code/catalog_config.py add <name> <source-folder> <index.yaml>
```
e.g.
```
python code/catalog_config.py add srkw-call-catalogue-files ./srkw-call-catalogue-files call-catalog.yaml
```

## `remove` a catalog

`remove` requires the \<`name`\> of the catalog from `index.yaml`. 

Remove the srkw-call-catalogue with:
```bash
python code/catalog_config.py remove <name>
```
e.g.
```
python code/catalog_config.py remove srkw-call-catalogue-files
```

# How and Why?

Repositories of parallel catalogs are housed in the  viewer's `LIBRARY` (by default located in the `viewer/catalogs` folder). Symbolic links connect to the data folders and the addition/removal is reflected in the `LIBRARY-INDEX` (by default `viewer/catalogs/index.yaml`)

The minimum configuration to load any catalog result in the following folder structure:
```bash
/var/www/html/catalog-viewer/
├── catalog
│   ├── index.yaml
│   ├── <catalog-name-A>.json # produced by `read_files.py` parser and used by frontend
│   ├── <catalog-name-A> -> /var/www/html/<catalog-name-A> # symbolic link
```
and `index.yaml` containing a listing of available catalogs (after 3 `add`s)
```yaml
catalogs:
    - catalog-A-name
    - catalog-B-name
    - catalog-c-name
```

> To override the default locations us the cmd flags `--LIBRARY <folder>` and `--LIBRARY-INDEX <index>.yaml` with new locations

## Starting from scratch, add a new catalog.

Prerequisites: 
- git clones of the `catalog-viewer` repo and `*-catalogue-files` repo
- repos `*-catalogue-files` have identical folder structures
- `catalog-viewer` must contain `catalog/index.yaml`


Starting with an empty list of catalogs `index.yaml`:
```yaml
catalogs:
    - 
```
and the following folder structure:
```bash
/var/www/html/catalog-viewer/
├── catalog
│   └── index.yaml
├── home.html
├── ...
└── index.html
```

```bash
/var/www/html/
├── catalog-viewer
    ├── catalog
    │   ├── index.yaml
    ├── home.html
    └── ...
    └── index.html
├── srkw-call-catalogue-files
        ├── call-catalog.yaml
        ├── ...
        └── media   # containing jpg, wav, etc
```

```
cd /var/www/html/catalog-viewer/
```

Then, to `add` a catalog use the command 

```bash
$ python code/add_catalog.py srkw-call-catalogue-files ./srkw-call-catalogue-files call-catalog.yaml
```

`index.yaml` updates like so

```yaml
catalogs:
    - srkw-call-catalogue-files
    - nrkw-call-catalogue-files         # independent calls `add_catalog.py`
    - transient-call-catalogue-files    # independent calls `add_catalog.py`
```

And the directories update symbolic links accordingly

```bash
/var/www/html/
├── catalog-viewer
    ├── catalog
    │   ├── index.yaml
    │   ├── srkw-call-catalogue-files.json  # produced by `read_files.py` parser
    │   ├── srkw-call-catalogue-files -> /var/www/html/srkw-call-catalogue-files    # symbolic link
    │   │   ├── call-catalog.yaml
    │   │   ├── ...
    │   │   └── media   # containing jpg, wav, etc
    ├── home.html
    └── index.html
├── srkw-call-catalogue-files
        ├── call-catalog.yaml
        ├── ...
        └── media   # containing jpg, wav, etc
```

To `remove` a catalog use the command `$ python code/remove_catalog.py srkw-call-catalogue-files`

<!-- ## Generic Sample

The folder structure after `add`ing 3 catalogs (pacific-whales, atlantic-sharks, antarctic-dolphins)
```bash
python code/catalog_config.py add pacific-whales ./pacific-whales listing.yaml

python code/catalog_config.py add atlantic-sharks ./atlantic-sharks call-catalog.yaml

python code/catalog_config.py add antarctic-dolphins ./antarctic-dolphins data.yaml
```
 looks like:

```bash
/var/www/html/catalog-viewer/
├── catalog
│   ├── index.yaml
│   ├── pacific-whales.json # produced by `read_files.py` parser
│   ├── pacific-whales -> /var/www/html/pacific-whales # symbolic link
│   │   ├── call-catalog.yaml
│   │   ├── ...
│   ├── atlantic-sharks.json
│   ├── atlantic-sharks -> /var/www/html/atlantic-sharks
│   │   ├── call-catalog.yaml
│   │   ├── ...
│   ├── antarctic-dolphins.json
│   ├── antarctic-dolphins -> /var/www/html/antarctic-dolphins
│   │   ├── call-catalog.yaml
│   │   ├── ...
```
And `index.yaml` contains a listing of available catalogs
```yaml
catalogs:
    - pacific-whales
    - atlantic-sharks
    - antarctic-dolphins
``` -->
