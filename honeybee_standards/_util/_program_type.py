# coding=utf-8
"""Clean the program type data."""
import os
import json


def clean_space_types(source_filename, dest_directory, vintage):
    """Process an OpenStudio Standards Space Type dictionary and write out a clean version.

    Specifically, this method performs 3 cleaning operations:
        * Discount odd space types that are not generally applicable but are intsead
            specific to a particular DoE reference building. (eg. 'Apartment_topfloor_NS')
        * Rename space types that use naming conventions that are not consistent with the
            other space types (eg. 'Courthouse - Conference' instead of 'Conference')
        * Reorganizing the 'Office' building type to be 3 separate types:
            'LargeOffice', 'MediumOffice', 'SmallOffice'.

    Args:
        source_filename: The full path to the space type JSON in the OpenStudio
            standards gem. If the standards gem repo has been downloaded to
            one's machine this file is likely in a location like the following:
                C:/Users/[USERNAME]/Documents/GitHub/openstudio-standards/lib/
                openstudio-standards/standards/ashrae_90_1/ashrae_90_1_2013/data/
                ashrae_90_1_2013.spc_typ.json
        dest_directory: The destination directory into which clean JSONs will be written.
            If you are trying to update the files within the honeybee_standards repo,
            you likely want to write to the following location:
                C:/Users/[USERNAME]/Documents/GitHub/honeybee-standards/honeybee_standards/
                data/program_type/
        vintage: Text for the vintage of the data to which the space types correspond to.
            Typically, this should be a shortened version of the full name of a standard.
            (eg. '2013' for 'Ashrae 90.1 2013')

    Returns:
        program_type_registry: Path to a JSON file containing the final included
            ProgramType names organized by building type. This is meant to be a
            human-readable file that documents all ProgramTypes that are available.
        program_type: Path to a JSON file containing the cleaned JSON with all relevant
            data. Each ProgramType has the clean, unique ProgramType name as a key and
            the value is the dictionary representation of all the ProgramType data.
    """
    # list all edits to be made from the original file
    _exclude_bldg = ('Office', 'Any')
    _exclude = ('Apartment_topfloor_NS',
                'Apartment_topfloor_WE',
                'Corridor_topfloor',
                'HospitalOfficeFlr5',
                'Hall_infil',
                'OutpatientFloor2Work',
                'Corridor4',
                'ElevatorCore4',
                'GuestRoom4Occ',
                'GuestRoom4Vac',
                'Stair4',
                'Storage4Front',
                'Storage4Rear',
                'Corridor2',
                'Retail2',
                '- undefined -',
                'Plenum')
    _replace = {'Courthouse - Break Room': 'Break Room',
                'Courthouse - Cell': 'Cell',
                'Courthouse - Conference': 'Conference',
                'Courthouse - Corridor': 'Corridor',
                'Courthouse - Courtroom': 'Courtroom',
                'Courthouse - Courtroom Waiting': 'Courtroom Waiting',
                'Courthouse - Elevator Lobby': 'Elevator Lobby',
                'Courthouse - Elevator Shaft': 'Elevator Shaft',
                'Courthouse - Entrance Lobby': 'Entrance Lobby',
                'Courthouse - Judges Chamber': 'Judges Chamber',
                'Courthouse - Jury Assembly': 'Jury Assembly',
                'Courthouse - Jury Deliberation': 'Jury Deliberation',
                'Courthouse - Library': 'Library',
                'Courthouse - Office': 'Office',
                'Courthouse - Parking': 'Parking',
                'Courthouse - Plenum': 'Plenum',
                'Courthouse - Restrooms': 'Restrooms',
                'Courthouse - Security Screening': 'Security Screening',
                'Courthouse - Service Shaft': 'Service Shaft',
                'Courthouse - Stairs': 'Stairs',
                'Courthouse - Storage': 'Storage',
                'Courthouse - Utility': 'Utility',
                'Strip mall - type 0A': 'Type 0A',
                'Strip mall - type 0B': 'Type 0B',
                'Strip mall - type 1': 'Type 1',
                'Strip mall - type 2': 'Type 2',
                'Strip mall - type 3': 'Type 3',
                'HospitalOfficeFlr1': 'HospitalOffice'}

    # initialize the clean dictionaries
    registry_dict = {'LargeOffice': [], 'SmallOffice': [], 'MediumOffice': []}
    program_type_dict = {}

    # extract data from the raw standards gem json file
    with open(source_filename, 'r') as f:
        data_store = json.load(f)

    for prog in data_store['space_types']:
        # get the building type and subdivide office into small, medium, and large
        bldg_type = prog['building_type']
        if bldg_type not in registry_dict and bldg_type not in _exclude_bldg:
            registry_dict[bldg_type] = []

        if prog['space_type'] in _exclude:
            # get rid of odd space types that are not generally applicable
            pass
        elif prog['space_type'] in _replace:
            # rename space types that use inconsistent naming conventions
            registry_dict[bldg_type].append(_replace[prog['space_type']])
            new_name, clean_data = clean_individual_type(
                vintage, bldg_type, _replace[prog['space_type']], prog)
            program_type_dict[new_name] = clean_data
        elif bldg_type == 'Office':
            # reorganize office space types by large, medium and small offices.
            if prog['space_type'].startswith('WholeBuilding'):
                continue
            elif prog['space_type'].startswith('SmallOffice'):
                prog_type = prog['space_type'].split(' - ')[-1]
                registry_dict['SmallOffice'].append(prog_type)
                new_name, clean_data = clean_individual_type(
                    vintage, 'SmallOffice', prog_type, prog)
                program_type_dict[new_name] = clean_data
            elif prog['space_type'].startswith('MediumOffice'):
                prog_type = prog['space_type'].split(' - ')[-1]
                registry_dict['MediumOffice'].append(prog_type)
                new_name, clean_data = clean_individual_type(
                    vintage, 'MediumOffice', prog_type, prog)
                program_type_dict[new_name] = clean_data
            else:
                registry_dict['LargeOffice'].append(prog['space_type'])
                new_name, clean_data = clean_individual_type(
                    vintage, 'LargeOffice', prog['space_type'], prog)
                program_type_dict[new_name] = clean_data
        else:
            # no need to change anything about the name
            registry_dict[bldg_type].append(prog['space_type'])
            new_name, clean_data = clean_individual_type(
                vintage, bldg_type, prog['space_type'], prog)
            program_type_dict[new_name] = clean_data

    # write the registry data
    program_type_registry = os.path.join(dest_directory, '{}_registry.json'.format(vintage))
    with open(program_type_registry, 'w') as fp:
        json.dump(registry_dict, fp, indent=2)

    # write the full data
    program_type = os.path.join(dest_directory, '{}_data.json'.format(vintage))
    with open(program_type, 'w') as fp:
        json.dump(program_type_dict, fp, indent=2)

    return program_type_registry, program_type


def clean_individual_type(vintage, building_type, space_type, data):
    """Clean the dictionary of an individual space type.

    Specifically, this method performs 2 cleaning operations:
    * Replacing the name of the dictionary with a unique name.
    * Removing all None values from the dictionary.

    Args:
        building_type: Text for the name of the building type.
        space_type: Text for the name of the space type.
        vintage: Text for the vintage of the data.
        data: JSON data for the space type.

    Return:
        unique_name: The new unique name for the ProgramType.
        clean_data: A clean dictionary.
    """
    unique_name = '{}::{}::{}'.format(vintage, building_type, space_type)
    clean_data = {'building_type': building_type,
                  'space_type': unique_name}
    for key in data:
        if data[key] is not None and key not in ('building_type', 'space_type'):
            clean_data[key] = data[key]
    return unique_name, clean_data
