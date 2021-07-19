"""Extend the honeybee_energy programtypes library."""
from honeybee_energy.programtype import ProgramType
from honeybee_energy.lib.programtypes import _program_types

import os
import json


# load the standards gem data of program types to Python dictionaries.
_data_dir = os.path.join(os.path.dirname(__file__), '../_standards_data')
_prog_dir = os.path.join(_data_dir, 'program_type')

_vintages = ('2019', '2016', '2013', '2010', '2007', '2004', '1980_2004', 'pre_1980')
_program_type_standards_dict = {}
for vintage in _vintages:
    _prog_vintage_dir = os.path.join(_prog_dir, '{}_data.json'.format(vintage))
    try:
        with open(_prog_vintage_dir, 'r') as f:
            _program_type_standards_dict.update(json.load(f))
    except FileNotFoundError:
        pass


def program_type_by_identifier(program_type_identifier):
    """Get a program_type from the library given its identifier.

    Args:
        program_type_identifier: A text string for the identifier of the ProgramType.
    """
    try:  # see if the program type has already been loaded to a Python object
        return _program_types[program_type_identifier]
    except KeyError:  # program type likely needs to be loaded from standards data
        try:
            _prog_dict = _program_type_standards_dict[program_type_identifier]
        except KeyError:  # program type is nowhere to be found; raise an error
            raise ValueError('"{}" was not found in the program type library.'.format(
                program_type_identifier))

    # create the Python object from the standards gem dictionary
    _prog_obj = ProgramType.from_standards_dict(_prog_dict)
    _prog_obj.lock()
    _program_types[program_type_identifier] = _prog_obj  # load faster next time
    return _prog_obj
