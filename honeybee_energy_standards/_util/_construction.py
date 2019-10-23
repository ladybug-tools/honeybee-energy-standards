# coding=utf-8
"""Clean the construction data."""
import os
import json


def clean_constructions(source_filename, dest_directory):
    """Process the OpenStudio Standards Construction dictionary and write a clean version.

    Specifically, this method performs the following cleaning operations:
        * Output resulting dictionary in a format with the name of the Construction
            as the key and the dictionary of the construction properties as the values.
        * Remove keys from the construction that are not used by honeybee including:
            'insulation_layer', 'standards_construction_type', 'skylight_framing'.
        * Discount odd constructions that are not generally applicable but are intsead
            specific to a DoE reference building. (eg. 'LargeHotel Interior Ceiling')
        * Remove the few constructions that do not have supporting materials in the
            nearby material.json. Note that this removal will not be performed if there
            is no neightboring material.json next to where the constructions.json will
            be output.

    Args:
        source_filename: The full path to the construction JSON in the OpenStudio
            standards gem. If the standards gem repo has been downloaded to one's
            machine this file is likely in a location like the following:
                C:/Users/[USERNAME]/Documents/GitHub/openstudio-standards/lib/
                openstudio-standards/standards/ashrae_90_1/data/ashrae_90_1.constructions.json
        dest_directory: The destination directory into which clean JSONs will be written.
            If you are trying to update the files within the honeybee_standards repo,
            you likely want to write to the following location:
                C:/Users/[USERNAME]/Documents/GitHub/honeybee-standards/honeybee_standards/data/

    Returns:
        opaque_dest_file_path: The file path to the clean JSON with opaque materials.
        window_dest_file_path: The file path to the clean JSON with window materials.
    """
    # list all edits to be made from the original file
    _remove_keys = ('insulation_layer', 'standards_construction_type', 'skylight_framing')
    _remove_constrs = ('Ground FloorGround_Floor_R11_T2013',
                       'Ground FloorGround_Floor_R17_T2013',
                       'Ground FloorGround_Floor_R22_T2013',
                       'int_slab_ceiling_smallhotel',
                       'int_slab_floor_smallhotel',
                       'int_wall_smallhotel',
                       'LargeHotel Interior Ceiling',
                       'LargeHotel Interior Floor',
                       'LargeHotel Interior Wall',
                       'Metal framed wallsW_m1_R15',
                       'Metal framed wallsW_m2_R19',
                       'Metal framed wallsW_m3_R21',
                       'Metal framed wallsW_T24_2013_R13.99',
                       'Metal framed wallsW1_R8.60',
                       'Metal framed wallsW2_R11.13',
                       'Metal framed wallsW3_R11.36',
                       'Metal framed wallsW4_R12.62',
                       'Metal roofR_R30',
                       'Metal roofR_R38',
                       'Metal roofR_T24_2013_24.86',
                       'Metal roofR1_R14.20',
                       'Metal roofR2_R12.90',
                       'Metal roofR3_R17.74',
                       'Metal roofR4_R20.28',
                       'NACM_Drop Ceiling',
                       'NACM_Interior Floor',
                       'NACM_Interior Wall',
                       'Plenum Acoustical Tile',
                       'Smallhotel 2010 Slab Floor')

    # list of window surface types, which differentiate Window constructions from Opaque
    _window_types = ('ExteriorWindow', 'InteriorWindow', 'GlassDoor', 'Skylight', None)

    # initialize the clean dictionary
    opaque_constr_dict = {}
    window_constr_dict = {}

    # extract data from the raw standards gem json file
    with open(source_filename, 'r') as f:
        data_store = json.load(f)

    # clean the data
    for constr in data_store['constructions']:
        if constr['name'] not in _remove_constrs:
            clean_constr = {}
            for key, value in constr.items():
                if key not in _remove_keys:
                    clean_constr[key] = value
            if constr['intended_surface_type'] in _window_types:
                window_constr_dict[constr['name']] = clean_constr
            else:
                opaque_constr_dict[constr['name']] = clean_constr

    # remove any constructions that do not have supporting materials
    opaque_mat_fp = os.path.join(dest_directory, 'opaque_material.json')
    remove_constructions_without_materials(opaque_mat_fp, opaque_constr_dict)
    window_mat_fp = os.path.join(dest_directory, 'window_material.json')
    remove_constructions_without_materials(window_mat_fp, window_constr_dict)

    # write the data into a file
    opaque_dest_file_path = os.path.join(dest_directory, 'opaque_construction.json')
    with open(opaque_dest_file_path, 'w') as fp:
        json.dump(opaque_constr_dict, fp, indent=2)
    window_dest_file_path = os.path.join(dest_directory, 'window_construction.json')
    with open(window_dest_file_path, 'w') as fp:
        json.dump(window_constr_dict, fp, indent=2)

    return opaque_dest_file_path, window_dest_file_path


def remove_constructions_without_materials(mat_fp, constr_dict):
    """Remove any constructions that lack corresponding materials in the material files.

    Note that this method is not meant to correct the raw standards gem data
    but is rather intended to account for any edits that other cleaning functions have
    made to the materials (like removing the 'CEC Title24' materials).

    Args:
        mat_fp: Path to the material file.
        constr_dict: Construction dictionary to check.
    """
    if not os.path.isfile(mat_fp):
        return

    with open(mat_fp, 'r') as f:
        clean_mat_dict = json.load(f)
    mats = clean_mat_dict.keys()
    constrs_to_remove = []
    for c_name, constr in constr_dict.items():
        for mat in constr['materials']:
            if mat not in mats:
                constrs_to_remove.append(c_name)
                break
    for c_name in constrs_to_remove:
        del constr_dict[c_name]
