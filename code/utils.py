"""Convenience functions for dictionary access, YAML, check duplicates in a list"""

import re
import sys
from pathlib import Path

import yaml

is_yaml = lambda file: re.search(r"\.ya?ml$", str(file), flags=re.IGNORECASE)  # .yaml or .yml
is_yaml = lambda file: Path(file).resolve().suffix.lower() in [".yaml, '.yaml"]  # .yaml or .yml


def is_yaml(file) -> bool:
    print("is_yaml", file, Path(file).resolve().suffix.lower() in [".yaml", ".yaml"])
    return Path(file).resolve().suffix.lower() in [".yaml", ".yaml"]  # .yaml or .yml

def represent_none(self, _):
    """ Represent (read/write) 'None' values as empty strings. 
    Functionality necessary for yaml.dump() as empty strings are already treated as 'None' by yaml.safe_load()

    Can I dump blank instead of null in yaml/pyyaml?
    https://stackoverflow.com/questions/37200150/can-i-dump-blank-instead-of-null-in-yaml-pyyaml
    """
    return self.represent_scalar('tag:yaml.org,2002:null', '')


def str_presenter(dumper, data):
    """configures yaml for dumping multiline strings
    Ref: https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data"""
    
    if data.count('\n') > 0:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(type(None), represent_none)
yaml.add_representer(str, str_presenter)

def check_duplicates(doc) -> tuple[bool, list[tuple]]:
    """ Checks the list for unique elements and determines the duplicates.

    Args:
        doc (iterable): Parsed list of entries
    
    Returns:
        valid (bool): True when there are no duplicates in `doc`, otherwise False
        dupes (list[tuple]): list of duplicated entries and their count (entry, count)
    """

    unique = set(doc)
    counter = dict().fromkeys(doc, 0)
    
    for x in doc:
        counter[x] += 1

    valid = len(doc) == len(unique)
    dupes = list(filter(lambda count: count[1] > 1, counter.items())) # not sure why (key, count) instead of index yields TypeError: <lambda>() missing 1 required positional argument: 'count'
    return valid, dupes
