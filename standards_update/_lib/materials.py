"""Extend the honeybee_energy material library."""
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass
from honeybee_energy.material.glazing import EnergyWindowMaterialGlazing, \
    EnergyWindowMaterialSimpleGlazSys
from honeybee_energy.material.gas import EnergyWindowMaterialGas
from honeybee_energy.lib.materials import _opaque_materials, _window_materials

import os
import json


# load the standards gem data of materials to Python dictionaries.
_data_dir = os.path.join(os.path.dirname(__file__), '../_standards_data')

try:
    _opaque_dir = os.path.join(_data_dir, 'opaque_material.json')
    with open(_opaque_dir, 'r') as f:
        _opaque_standards_dict = json.load(f)
except FileNotFoundError:
    _opaque_standards_dict = {}

try:
    _window_dir = os.path.join(_data_dir, 'window_material.json')
    with open(_window_dir, 'r') as f:
        _window_standards_dict = json.load(f)
except FileNotFoundError:
    _window_standards_dict = {}


def opaque_material_by_identifier(material_identifier):
    """Get an opaque material from the library given the material identifier.

    Args:
        material_identifier: A text string for the identifier of the material.
    """
    try:  # see if the material has already been loaded to a Python object
        return _opaque_materials[material_identifier]
    except KeyError:  # material likely needs to be loaded from standards data
        try:
            _mat_dict = _opaque_standards_dict[material_identifier]
        except KeyError:  # material is nowhere to be found; raise an error
            raise ValueError(
                '"{}" was not found in the opaque energy material library.'.format(
                    material_identifier))

    # create the Python object from the standards gem dictionary
    if _mat_dict['material_type'] == 'StandardOpaqueMaterial':
        _mat_obj = EnergyMaterial.from_standards_dict(_mat_dict)
    elif _mat_dict['material_type'] in ('MasslessOpaqueMaterial', 'AirGap'):
        _mat_obj = EnergyMaterialNoMass.from_standards_dict(_mat_dict)
    else:
        raise ValueError('Standards gem material type "{}" is not recognized.'.format(
            _mat_dict['material_type']))
    _mat_obj.lock()
    _opaque_materials[material_identifier] = _mat_obj  # next time, it will be loaded faster
    return _mat_obj


def window_material_by_identifier(material_identifier):
    """Get an window material from the library given the material identifier.

    Args:
        material_identifier: A text string for the identifier of the material.
    """
    try:  # see if the material has already been loaded to a Python object
        return _window_materials[material_identifier]
    except KeyError:  # material likely needs to be loaded from standards data
        try:
            _mat_dict = _window_standards_dict[material_identifier]
        except KeyError:  # material is nowhere to be found; raise an error
            raise ValueError(
                '"{}" was not found in the window energy material library.'.format(
                    material_identifier))

    # create the Python object from the standards gem dictionary
    if _mat_dict['material_type'] == 'StandardGlazing':
        _mat_obj = EnergyWindowMaterialGlazing.from_standards_dict(_mat_dict)
    elif _mat_dict['material_type'] == 'SimpleGlazing':
        _mat_obj = EnergyWindowMaterialSimpleGlazSys.from_standards_dict(_mat_dict)
    elif _mat_dict['material_type'] == 'Gas':
        _mat_obj = EnergyWindowMaterialGas.from_standards_dict(_mat_dict)
    else:
        raise ValueError('Standards gem material type "{}" is not recognized.'.format(
            _mat_dict['material_type']))
    _mat_obj.lock()
    _window_materials[material_identifier] = _mat_obj  # next time, it will be loaded faster
    return _mat_obj
