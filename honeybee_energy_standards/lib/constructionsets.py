"""Extend the honeybee_energy constructionsets library."""
from honeybee_energy.constructionset import ConstructionSet
from honeybee_energy.lib.constructionsets import _json_construction_sets

import os
import json


# load the standards gem data of construction sets to Python dictionaries.
_data_dir = os.path.join(os.path.dirname(__file__), '../data')
_c_set_dir = os.path.join(_data_dir, 'construction_set')

_vintages = ('2013', '2010', '2007', '2004', '1980_2004', 'pre_1980')
_construction_set_standards_dict = {}
for vintage in _vintages:
    _c_set_vintage_dir = os.path.join(_c_set_dir, '{}_data.json'.format(vintage))
    with open(_c_set_vintage_dir, 'r') as f:
        _construction_set_standards_dict.update(json.load(f))


def construction_set_by_name(construction_set_name):
    """Get a construction_set from the library given its name.

    Args:
        construction_set_name: A text string for the name of the ConstructionSet.
    """
    try:  # see if the program type has already been loaded to a Python object
        return _json_construction_sets[construction_set_name]
    except KeyError:  # construction set likely needs to be loaded from standards data
        try:
            _c_set_dict = _construction_set_standards_dict[construction_set_name]
        except KeyError:  # program type is nowhere to be found; raise an error
            raise ValueError('"{}" was not found in the construction set library.'.format(
                construction_set_name))

    # create the Python object from the standards gem dictionary
    _c_set_obj = ConstructionSet.from_standards_dict(_c_set_dict)
    _json_construction_sets[construction_set_name] = _c_set_obj  # load faster next time
    return _c_set_obj
