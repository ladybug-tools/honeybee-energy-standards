# coding=utf-8
"""Clean the construction set data."""
from __future__ import division

import math
import os
import json


def clean_construction_sets(source_filename, dest_directory, vintage,
                            construction_filename, material_filename):
    """Clean the OpenStudio Standards Construction Properties dictionary.

    Specifically, this method performs the following major cleaning operations:
    * Classify the individual construction properties into complete ConstructionSets
        oranized by Climate Zone and Construction Type. These include:
            * climate zones: (1, 2, 3, 4, 5, 6, 7, 8)
            * construction types: ('SteelFramed', 'WoodFramed', 'Mass', 'MetalBuilding')
        This entails the following default assumptions:
            * When multiple constructions exist for a given construction type, this
                method will default to the NonResidential building type and ignore
                the Residential and Semiheated building types.
            * SteelFramed and Mass buildings use the 'IEAD' roof type.
            * WoodFramed buildings use the 'Attic and Other' roof type.
            * Metal Building uses it's own roof type.
            * For all windows and glass doors, the 'Metal framing (all other)'
                type is used for all construction types except 'WoodFramed', where
                'Nonmetal framing (all)' is used instead. If multiple construction options
                exist, the one corresponding to 40% glazing is used.
            * The 'Swinging' door type is used for all vertical opaque doors and The
                'NonSwinging' door tpye is used for all overhead doors.
            * All skylights use the 'Glass with Curb' type over 'Plastic with Curb'
                or 'Without Curb'.
            * When multiple variations of a given climate zone number exist for a given
                zone (ie. 3A, 3B, 3C) prefernce will be given to A.
    * Output resulting dictionary in a format with the name of the ConstructionSet
        as the key and the dictionary of the constructions as the values.

    Args:
        source_filename: The full path to the construction properties JSON in the
            OpenStudio standards gem. If the standards gem repo has been downloaded
            to one's machine this file is likely in a location like the following:
                C:/Users/[USERNAME]/Documents/GitHub/openstudio-standards/lib/
                openstudio-standards/standards/ashrae_90_1/ashrae_90_1_2013/data/
                ashrae_90_1_2013.construction_properties.json
        dest_directory: The destination directory into which clean JSONs will be written.
            If you are trying to update the files within the honeybee_standards repo,
            you likely want to write to the following location:
                C:/Users/[USERNAME]/Documents/GitHub/honeybee-standards/honeybee_standards/
                data/construction_set
        vintage: Text for the vintage of the data to which the space types correspond to.
            Typically, this should be a shortened version of the full name of a standard.
            (eg. '2013' for 'Ashrae 90.1 2013')
        construction_filename: File path to the cleaned opaque construction JSON. This
            will be edited and re-exported with constructions matching the insulation
            values of the various climate zones.
        material_filename: File path to the cleaned opaque material JSON. This
            will be used to determin target resistances

    Returns:
        dest_file_path: The file path to the clean JSON.
    """
    # initialize the clean dictionary
    constr_set_dict = {}

    # set the criteria of construction sets to build
    climate_zones = (1, 2, 3, 4, 5, 6, 7, 8)
    construction_types = ('SteelFramed', 'WoodFramed', 'Mass', 'Metal Building')

    # extract data from the raw standards gem json file
    with open(source_filename, 'r') as f:
        data_store = json.load(f)

    # load existing clean constructions and materials data
    with open(construction_filename, 'r') as f:
        clean_constr_dict = json.load(f)
    with open(material_filename, 'r') as f:
        clean_mat_dict = json.load(f)

    # loop through climate zones and construction types to build up all sets
    for c_zone in climate_zones:
        for constr_type in construction_types:
            # initialize an empty base construction set
            cz_name = 'ClimateZone{}'.format(c_zone)
            set_name = '{}::{}::{}'.format(vintage, cz_name, constr_type)
            base_dict = {'name': set_name,
                         'wall_set': {},
                         'floor_set': {},
                         'roof_ceiling_set': {},
                         'aperture_set': {},
                         'door_set': {}
                         }

            # get the exterior wall construction
            wall_constr = extract_construction(data_store, c_zone, 'ExteriorWall', constr_type)
            wall_constr = adjust_typical_insulation(wall_constr, clean_constr_dict, clean_mat_dict)
            base_dict['wall_set']['exterior_construction'] = wall_constr

            # get the ground wall construction (note Mass is the only option available)
            wall_constr = extract_construction(data_store, c_zone, 'GroundContactWall', 'Mass')
            wall_constr = adjust_typical_insulation(wall_constr, clean_constr_dict, clean_mat_dict)
            base_dict['wall_set']['ground_construction'] = wall_constr

            # get the exterior roof construction
            if constr_type == 'Metal Building':
                roof_type = constr_type
            else:
                roof_type = 'IEAD' if constr_type in ('SteelFramed', 'Mass') else 'Attic and Other'
            roof_constr = extract_construction(data_store, c_zone, 'ExteriorRoof', roof_type)
            roof_constr = adjust_typical_insulation(roof_constr, clean_constr_dict, clean_mat_dict)
            base_dict['roof_ceiling_set']['exterior_construction'] = roof_constr

            # get the exposed floor construction
            floor_type = 'SteelFramed' if constr_type == 'Metal Building' else constr_type
            floor_constr = extract_construction(data_store, c_zone, 'ExteriorFloor', floor_type)
            floor_constr = adjust_typical_insulation(floor_constr, clean_constr_dict, clean_mat_dict)
            base_dict['floor_set']['exterior_construction'] = floor_constr

            # get the underground floor construction
            floor_constr = extract_construction(data_store, c_zone, 'GroundContactFloor', 'Unheated')
            if floor_constr['construction'] == 'Smallhotel 2010 Slab Floor':
                floor_constr = extract_construction(data_store, c_zone, 'GroundContactFloor',
                                                    'Heated', 'Semiheated')
            floor_constr = adjust_typical_insulation(floor_constr, clean_constr_dict, clean_mat_dict)
            base_dict['floor_set']['ground_construction'] = floor_constr

            # get the exterior window construction
            win_type = 'Nonmetal framing (all)' if constr_type == 'WoodFramed' else \
                'Metal framing (all other)'
            win_constr = extract_construction(data_store, c_zone, 'ExteriorWindow', win_type)
            base_dict['aperture_set']['window_construction'] = win_constr['construction']
            base_dict['aperture_set']['operable_construction'] = win_constr['construction']

            # get the skylight construction
            win_constr = extract_construction(data_store, c_zone, 'Skylight', 'Glass with Curb')
            base_dict['aperture_set']['skylight_construction'] = win_constr['construction']

            # get the exterior opaque door constructions
            door_constr = extract_construction(data_store, c_zone, 'ExteriorDoor', 'Swinging')
            door_constr = adjust_typical_insulation(door_constr, clean_constr_dict, clean_mat_dict)
            base_dict['door_set']['exterior_construction'] = door_constr
            door_constr = extract_construction(data_store, c_zone, 'ExteriorDoor', 'NonSwinging')
            door_constr = adjust_typical_insulation(door_constr, clean_constr_dict, clean_mat_dict)
            base_dict['door_set']['overhead_construction'] = door_constr

            # get the exterior glass door constructions
            door_constr = extract_construction(data_store, c_zone, 'GlassDoor',
                                               'Metal framing (entrance door)')
            base_dict['door_set']['exterior_glass_construction'] = door_constr['construction']

            # add the construction set to the final dictionary
            constr_set_dict[set_name] = base_dict

    # write the complete set of constructions
    dest_file_path = os.path.join(dest_directory, '{}_data.json'.format(vintage))
    with open(dest_file_path, 'w') as fp:
        json.dump(constr_set_dict, fp, indent=2)

    # write the updated dictionary of constructions
    with open(construction_filename, 'w') as fp:
        json.dump(clean_constr_dict, fp, indent=2)

    return dest_file_path


def extract_construction(data_store, c_zone, srf_type, constr_type,
                         bldg_category='Nonresidential'):
    """Get the name of a construction from the whole data_store based on criteria.

    Args:
        data_store: The full JSON dictionary of construction properties.
        c_zone: A number between 0 and 8 for the climate zone.
        srf_type: The type of surface being requested (ie. 'ExteriorWall',
            'ExteriorWindow', etc.)
        constr_type: The type of building construction. Choose from:
            ('SteelFramed', 'WoodFramed', 'Mass', 'MetalBuilding')
        bldg_category: The building category. Choose from:
            ('Nonresidential', 'Residential', 'Semiheated')
    """
    clim_zone = 'ClimateZone {}'.format(c_zone)
    # try to find the construction following the building_category
    for cnst_dict in data_store['construction_properties']:
        if cnst_dict['construction'] and 'Adiabatic' not in cnst_dict['construction'] and \
                cnst_dict['climate_zone_set'] == clim_zone and \
                cnst_dict['intended_surface_type'] == srf_type and \
                cnst_dict['standards_construction_type'] == constr_type and \
                cnst_dict['building_category'] == bldg_category:
            return cnst_dict
    # if no construction was found in the building category, just find any construction
    for cnst_dict in data_store['construction_properties']:
        if cnst_dict['construction'] and 'Adiabatic' not in cnst_dict['construction'] and \
                cnst_dict['climate_zone_set'] == clim_zone and \
                cnst_dict['intended_surface_type'] == srf_type and \
                cnst_dict['standards_construction_type'] == constr_type:
            return cnst_dict
    # no construction was found try adding an A to the climate zone
    if 'A' in str(c_zone):
        raise(TypeError('No Construction found meeting these criteria: {}, {}, {}'.format(
            c_zone, srf_type, constr_type)))
    else:
        cz = '{}A'.format(c_zone)
        return extract_construction(data_store, cz, srf_type, constr_type, bldg_category)


def adjust_typical_insulation(base_constr_dict, constuction_dict, material_dict):
    """Adjust insulation in the the global constuction_dict using a construction property dictionary.

    Args:
        base_constr_dict: A dictionary from the raw OpenStudio standards construction
            properties dictionary.
        constuction_dict: Complete dictionary from the clean construction JSON. This
            method will add a new construction to this dictionary that meets the
            'assembly_maximum_u_value' in the base_constr_dict and uses the 'construction'
            in the base_constr_dict to start.
        material_dict: Complete dictionary from the clean material JSON.
    """
    # get the target R-value
    compliant_u_val = base_constr_dict['assembly_maximum_u_value']
    if compliant_u_val is not None:
        if compliant_u_val == 0:
            return base_constr_dict['construction']
        compliant_r_val = 1 / compliant_u_val
    elif base_constr_dict['assembly_maximum_f_factor'] is not None:  # ground floor slab
        compliant_f_val = base_constr_dict['assembly_maximum_f_factor']
        if compliant_f_val >= 0.73:  # ASHRAE 90.1 Table A6.3.1
            return base_constr_dict['construction']
        compliant_r_val = 5 if compliant_f_val >= 0.46 else 10  # ASHRAE 90.1 Table A6.3.1
    elif base_constr_dict['assembly_maximum_c_factor'] is not None:  # underground wall
        compliant_c_val = base_constr_dict['assembly_maximum_c_factor']
        if compliant_c_val >= 1.14:  # ASHRAE 90.1 Table A4.2.1
            return base_constr_dict['construction']
        # ASHRAE 90.1 Table A4.2.1
        r_vals = (5, 7.5, 10, 12.5, 15, 17.5, 20)
        c_facs = (0.17, 0.119, 0.092, 0.075, 0.063, 0.054, 0.048)
        for r, c in zip(r_vals, c_facs):
            if c <= compliant_c_val:
                compliant_r_val = r
                break
    else:
        # no insulation criteria available. return original construction
        return base_constr_dict['construction']

    # get the starting construction to work from and calculate its R-value
    orig_constr_name = base_constr_dict['construction']
    start_constr = constuction_dict[orig_constr_name]
    base_r = sum(material_dict[mat]['resistance'] for mat in start_constr['materials'])

    # calculate the R-value needed by the insulation
    target_r = int(math.ceil(compliant_r_val - base_r))
    if target_r == 0:
        return base_constr_dict['construction']
    new_constr_name = '{}-R{}'.format(orig_constr_name, math.ceil(compliant_r_val))

    # add the new construction to the global constuction_dict if necessary
    if new_constr_name not in constuction_dict:
        new_constr = start_constr.copy()
        new_constr['name'] = new_constr_name
        insul_name = 'Typical Insulation-R{}'.format(target_r)
        assert 'Typical Insulation' in new_constr['materials'], \
            'Typical Insulation must be in a construction in order to adjust it.'
        new_constr['materials'] = [mat if mat != 'Typical Insulation' else insul_name
                                   for mat in new_constr['materials']]
        constuction_dict[new_constr_name] = new_constr

    return new_constr_name
