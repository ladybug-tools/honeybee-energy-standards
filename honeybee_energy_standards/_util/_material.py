# coding=utf-8
"""Clean the material data."""
import os
import json


def clean_materials(source_filename, dest_directory):
    """Process the OpenStudio Standards Material dictionary and write out a clean version.

    Specifically, this method performs the following cleaning operations:
        * Output resulting dictionary in a format with the name of the Material
            as the key and the dictionary of the material properties as the values.
        * Remove all material properties with None values. This reduces the file size
            to roughly a quarter of what it is normally.
        * Remove all materials from 'CEC Title24' since they are not used by any of the
            constructions or construction sets of ASHRAE 90.1.
        * Remove the 5 skylight frame materials, which do not have enough data to create
            complete energy materials.
        * Add a series of Typical Insulation materials with increasing R-value, which
            will be used to create code compliant constructions in the _construction_set
            module.

    Args:
        source_filename: The full path to the material JSON in the OpenStudio
            standards gem. If the standards gem repo has been downloaded to one's
            machine this file is likely in a location like the following:
                C:/Users/[USERNAME]/Documents/GitHub/openstudio-standards/lib/
                openstudio-standards/standards/ashrae_90_1/data/ashrae_90_1.materials.json
        dest_directory: The destination directory into which clean JSONs will be written.
            If you are trying to update the files within the honeybee_standards repo,
            you likely want to write to the following location:
                C:/Users/[USERNAME]/Documents/GitHub/honeybee-standards/honeybee_standards/data/

    Returns:
        opaque_dest_file_path: The file path to the clean JSON with opaque materials.
        window_dest_file_path: The file path to the clean JSON with window materials.
    """
    # types of materials (to help organize opaque materials from window ones)
    opaque_types = ('StandardOpaqueMaterial', 'MasslessOpaqueMaterial', 'AirGap')
    window_types = ('SimpleGlazing', 'Gas', 'StandardGlazing')

    # initialize the clean dictionaries
    opaque_mat_dict = {}
    window_mat_dict = {}

    # extract data from the raw standards gem json file
    with open(source_filename, 'r') as f:
        data_store = json.load(f)

    # clean the data
    for mat in data_store['materials']:
        clean_mat = {}
        if mat['notes'] is None and not mat['name'].startswith('Skylight_Frame_Width'):
            for key, value in mat.items():
                if value is not None:
                    clean_mat[key] = value
            if mat['material_type'] in opaque_types:
                opaque_mat_dict[mat['name']] = clean_mat
            elif mat['material_type'] in window_types:
                window_mat_dict[mat['name']] = clean_mat

    # add typical insulation materials with different resistances to the dictionary
    add_typical_insulation(opaque_mat_dict)

    # write the data into a file
    opaque_dest_file_path = os.path.join(dest_directory, 'opaque_material.json')
    with open(opaque_dest_file_path, 'w') as fp:
        json.dump(opaque_mat_dict, fp, indent=2)
    window_dest_file_path = os.path.join(dest_directory, 'window_material.json')
    with open(window_dest_file_path, 'w') as fp:
        json.dump(window_mat_dict, fp, indent=2)

    return opaque_dest_file_path, window_dest_file_path


def add_typical_insulation(opaque_mat_dict):
    """Add versions of the typical insulation material that have compliant R-values.

    This is necessary because the standards gem switched to automatically adjusting the
    thickness of any construction's insulation layer in a Ruby script rather than simply
    having a list of compliant constructions like they used to. Accordngly, this method
    generates a series of insulation materials at an increasing thickness, which yield
    whole-number R-values. These will be used in the _construction_set module to write
    out a series of constructions that meet the target R-value of various codes.
    """
    typical_insulation = opaque_mat_dict['Typical Insulation']
    assert typical_insulation['material_type'] == 'MasslessOpaqueMaterial', \
        'Typical insulation must be a MasslessOpaqueMaterial.'
    del typical_insulation['conductivity']
    del typical_insulation['density']
    del typical_insulation['specific_heat']

    for r_val in range(1, 61):
        new_dict_name = '{}-R{}'.format(typical_insulation['name'], r_val)
        new_dict = typical_insulation.copy()
        del new_dict['thermal_absorptance']
        del new_dict['solar_absorptance']
        del new_dict['visible_absorptance']
        new_dict['name'] = new_dict_name
        new_dict['resistance'] = r_val
        opaque_mat_dict[new_dict_name] = new_dict
