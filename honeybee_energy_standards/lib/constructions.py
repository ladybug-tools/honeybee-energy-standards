"""Extend the honeybee_energy construction library."""
from honeybee_energy.construction.opaque import OpaqueConstruction
from honeybee_energy.construction.window import WindowConstruction
from honeybee_energy.lib.constructions import _idf_opaque_constructions, _idf_window_constructions

import os
import json


# load the standards gem data of construction to Python dictionaries.
_data_dir = os.path.join(os.path.dirname(__file__), '../data')

_opaque_dir = os.path.join(_data_dir, 'opaque_construction.json')
with open(_opaque_dir, 'r') as f:
    _opaque_constr_standards_dict = json.load(f)

_window_dir = os.path.join(_data_dir, 'window_construction.json')
with open(_window_dir, 'r') as f:
    _window_constr_standards_dict = json.load(f)


def opaque_construction_by_name(construction_name):
    """Get an opaque construction from the library given the construction name.

    Args:
        construction_name: A text string for the name of the construction.
    """
    try:  # see if the construction has already been loaded to a Python object
        return _idf_opaque_constructions[construction_name]
    except KeyError:  # construction likely needs to be loaded from standards data
        try:
            _constr_dict = _opaque_constr_standards_dict[construction_name]
        except KeyError:  # construction is nowhere to be found; raise an error
            raise ValueError(
                '"{}" was not found in the opaque energy construction library.'.format(
                    construction_name))

    # create the Python object from the standards gem dictionary
    _constr_obj = OpaqueConstruction.from_standards_dict(_constr_dict)
    _idf_opaque_constructions[construction_name] = _constr_obj  # load faster next time
    return _constr_obj


def window_construction_by_name(construction_name):
    """Get an window construction from the library given the construction name.

    Args:
        construction_name: A text string for the name of the construction.
    """
    try:  # see if the construction has already been loaded to a Python object
        return _idf_window_constructions[construction_name]
    except KeyError:  # construction likely needs to be loaded from standards data
        try:
            _constr_dict = _window_constr_standards_dict[construction_name]
        except KeyError:  # construction is nowhere to be found; raise an error
            raise ValueError(
                '"{}" was not found in the window energy construction library.'.format(
                    construction_name))

    # create the Python object from the standards gem dictionary
    _constr_obj = WindowConstruction.from_standards_dict(_constr_dict)
    _idf_window_constructions[construction_name] = _constr_obj  # load faster next time
    return _constr_obj
