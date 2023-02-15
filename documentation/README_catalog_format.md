# Catalog formatting

Each `catalog` must adhere to the structure portrayed below

```yaml
id:
    - sample
    - call-type
display:
  - display-one:
    - pod
  - display-two:
    - clan
fields:
    - sample
    - call-type
    - image-file
    - wav-file
    - description-file
    # Any additional fields can be added, but the above are required.
    - pod
    - clan
    - matrilines
    - population
calls:
- sample: 0
  call-type: S01
  image-file: srkw-call-catalogue-files/media/S01-J,L.png
  wav-file: srkw-call-catalogue-files/media/S01-J,L.wav
  description-file: srkw-call-catalogue-files/call-type-description/call-type-S01.md
  # Additional fields included
  pod: J,L
  clan: J
  matrilines:
  population: SRKW
```
# `display` section

The `display` section outlines which data points to display for each of the calls in the catalog. It is required for the YAML to have these values, but they may be left blank. 
```yaml
display:
  - display-one: # both values will default to display 'sample' data for the call
  - display-two:
```

The only possible fields in this section are `display-one` and `display-two`. The values for each of these fields must also be present in the `fields` section of the YAML

![Sample display of call data](./single-view.png "Example of call data") 

In the above example the `display` section would look like

```yaml
display:
  - display-one:
    - pod
  - display-two:
    - clan
```
The entry in the `calls` section for this call would look like the following
```yaml
calls:
- sample: 0
  call-type: S01
  image-file: srkw-call-catalogue-files/media/S01-J,L.png
  wav-file: srkw-call-catalogue-files/media/S01-J,L.wav
  description-file: srkw-call-catalogue-files/call-type-description/call-type-S01.md
  pod: J,L # field being showcased in display-one
  clan: J # field being showcased in display-two
  matrilines:
  population: SRKW
```

# `fields` section

Each of the `fields` corresponds to a point of data that will be used in the catalog display. There are `5 required fields`, but additional fields can be added to filter calls. 

## Required `fields`
- sample
  - A unique identification number beginning at 0
- call-type
  - The unique name of the call
- image-file
  - Path to the image file
- wav-file
  - Path to the sound file
- description-file
  - Path to the markdown description file

Each of the above must be included in the `fields` section of the YAML file. Each of the fields and must also appear in each additional entry in the `calls` section


Valid `fields` section
```yaml
fields:
    - sample
    - call-type
    - image-file
    - wav-file
    - description-file
    - pod:
        - J,K
    - clan:
        - J,L
    - matrilines
    - population:
        - NRKW,SRKW,TRANSIENT

    # contains all required fields and additional 'pod', 'clan', 'matrilines', and'population' fields
```

Invalid `fields` section
```yaml
fields:
    - sample
    - image-file
    - wav-file
    - description-file
    - pod:
        - J,K
    - population:
        - NRKW,SRKW,TRANSIENT
    
    # Missing the 'call-type' required field
```

## Filtering `fields`

Each of the entries in `fields` can be used to filter the results displayed in the catalog. Which fields to filter on and the allowable values must be specified in the `fields` section.

To allow for filtering add the field entry as a key to a value of allowable values for the field.

```yaml
fields:
    - sample
    - call-type
    - image-file
    - wav-file
    - description-file
    - pod:
        - J,K,Unknown # Calls can be filtered by the pod values 'J','K', and 'Unknown'
    - clan:
        - J,L # Calls can be filtered on clan values 'J' and 'L'
    - matrilines
    - population:
        - NRKW,SRKW,TRANSIENT # Calls can be filtered on population values 'NRKW', 'SRKW', and 'TRANSIENT'
```
Each entry that is specified will create an additional dropdown menu to filter on in the catalogue.

# `calls` section

Each entry in the class section represents a call to display in the catalogue

## Required `calls`

All of the entries must contain all of the fields specified in the `fields` section of the catalogue file. 

Valid `calls` section
```yaml
fields:
    - sample
    - call-type
    - image-file
    - wav-file
    - description-file
    - pod:
        - J,K
    - clan:
        - J,L
    - matrilines
    - population:
        - NRKW,SRKW,TRANSIENT
calls:
  - sample: 0
    call-type: S01
    image-file: srkw-call-catalogue-files/media/S01-J,L.png
    wav-file: srkw-call-catalogue-files/media/S01-J,L.wav
    pod: J,L
    clan: J
    description-file: srkw-call-catalogue-files/call-type-description/call-type-S01.md
    matrilines:
    population: SRKW

  # Each of the entries in 'fields' is in the 'calls' entry
```

Invalid `calls` entry
```yaml
fields:
    - sample
    - call-type
    - image-file
    - wav-file
    - description-file
    - pod:
        - J,K
    - clan:
        - J,L
    - matrilines
    - population:
        - NRKW,SRKW,TRANSIENT
calls:
  - sample: 0
    call-type: S01
    image-file: srkw-call-catalogue-files/media/S01-J,L.png
    wav-file: srkw-call-catalogue-files/media/S01-J,L.wav
    pod: J,L
    clan: J
    description-file: srkw-call-catalogue-files/call-type-description/call-type-S01.md
    matrilines:
    # missing population field

  # Invalid entry. It must contain all of the fields in 'fields' section
```

Values in the `calls` section may be left blank, however this will result in the field data of `Unknown` for that call. If values are left as `Unknown` ensure that it is added as one of the filters in the `fields` section if it is a filterable field. 

Valid entry with blank fields
```yaml
fields:
    - sample
    - call-type
    - image-file
    - wav-file
    - description-file
    - pod:
        - J,K
    - clan:
        - J,L
    - matrilines
    - population:
        - NRKW,SRKW,TRANSIENT
calls:
  - sample: 0
    call-type: S01
    image-file: srkw-call-catalogue-files/media/S01-J,L.png
    wav-file: srkw-call-catalogue-files/media/S01-J,L.wav
    pod: # value will default to 'Unknown'
    clan: J
    description-file: srkw-call-catalogue-files/call-type-description/call-type-S01.md
    matrilines:
    population: # value will default to 'Unknown'

  # May leave blank fields, but they must still be present
```