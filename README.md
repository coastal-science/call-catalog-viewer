# call-catalog-viewer
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)

| [![Manual deploy](https://github.com/coastal-science/call-catalog-viewer/actions/workflows/manual_deploy.yml/badge.svg)](https://github.com/coastal-science/call-catalog-viewer/actions/workflows/manual_deploy.yml) | [![Manual deploy](https://github.com/coastal-science/call-catalog-viewer/actions/workflows/manual_deploy.yml/badge.svg)](https://github.com/coastal-science/call-catalog-viewer/actions/workflows/manual_deploy.yml) |
|-|-|

The call catalog viewer is an catalog authoring project developed to serve the orca [call catalog demo site](https://orca.research.sfu.ca/catalogue). The catalog viewer works in two parts, the (1) viewer (_this repo_) and (2) the [viewer files](https://github.com/sfu-bigdata/srkw-call-catalogue-files). The orca catalogue files is the digitized call catalogue originally developed by Dr. John K. B. Ford (DOI: "" 1989).

![Catalog viewer](documentation/Screenshot%20catalog.png)

In addition to digitizing the catalog of Orca calls, the call catalog viewer is developed as a catalog authoring platform to generate and display a static website for a catalog (or collection of catalogs). A catalog contains entries with media (sound, images, text) and generates a website with elementary features (navigation, filter, search, playback, lazy loading) as long as the underlying data model remains a hierarchical taxonomy (a collection of flat structures). 

The catalog and data model is described in human-readable and editable `yaml` [format](https://github.com/sfu-bigdata/srkw-call-catalogue-files/blob/main/call-catalog.yaml). The catalog data (entries, media) are maintained in a [git repository](https://github.com/sfu-bigdata/srkw-call-catalogue-files). Multiple catalogs can be combined into a _catalog-of-catalogs_.
![Catalog yaml](documentation/Screenshot%20catalog.yaml.png)

This project is helpful to generate, maintain and update a website that serves as a library (or catalog) of related media files, for example, 
- a library of bird calls (sound, image, text) in a genus combined into a catalog of genus calls in a family
- a gallery of car pictures of a vehicle model (_Mustang_), combined into a catalog by make (_Ford_).
- a departmental directory combined into a directory-of-directories in a university.


## Getting Started
TODO...
- How do I get started?
- Where can I get more help, if I need it?

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

### Contributors

The [human](humans.txt) members of our team are.

## [License](LICENSE.md)
MIT and [Open Government Licence - Canada 2.0](https://open.canada.ca/en/open-government-licence-canada)
