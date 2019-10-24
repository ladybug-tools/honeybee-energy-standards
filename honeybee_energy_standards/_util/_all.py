# coding=utf-8
"""Clean and re-export all ashrae 90.1 data from the standards gem."""
import os

from honeybee_energy_standards._util._program_type import clean_space_types
from honeybee_energy_standards._util._schedule import clean_schedules
from honeybee_energy_standards._util._construction_set import clean_construction_sets
from honeybee_energy_standards._util._construction import clean_constructions
from honeybee_energy_standards._util._material import clean_materials


def clean_all(ashrae_directory):
    """Clean and re-export all ashrae 90.1 data from the standards gem.

    Args:
        ashrae_directory: Directory to the ashrae 90.1 data in the standards gem.
            Typically this is:
                C:/Users/[USERNAME]/Documents/GitHub/openstudio-standards/lib/
                openstudio-standards/standards/ashrae_90_1/
    """
    current_dir = os.path.dirname(__file__)
    master_dir, util_mod = os.path.split(current_dir)
    dest_dir = os.path.join(master_dir, 'data')

    # clean the Schedules
    source_filename = os.path.join(ashrae_directory, 'data', 'ashrae_90_1.schedules.json')
    clean_schedules(source_filename, dest_dir)

    # clean the ProgramTypes
    source_filename_2013 = os.path.join(
        ashrae_directory, 'ashrae_90_1_2013', 'data', 'ashrae_90_1_2013.spc_typ.json')
    source_filename_2010 = os.path.join(
        ashrae_directory, 'ashrae_90_1_2010', 'data', 'ashrae_90_1_2010.spc_typ.json')
    source_filename_2007 = os.path.join(
        ashrae_directory, 'ashrae_90_1_2007', 'data', 'ashrae_90_1_2007.spc_typ.json')
    source_filename_2004 = os.path.join(
        ashrae_directory, 'ashrae_90_1_2004', 'data', 'ashrae_90_1_2004.spc_typ.json')
    source_filename_1980_2004 = os.path.join(
        ashrae_directory, 'doe_ref_1980_2004', 'data', 'doe_ref_1980_2004.spc_typ.json')
    source_filename_pre_1980 = os.path.join(
        ashrae_directory, 'doe_ref_pre_1980', 'data', 'doe_ref_pre_1980.spc_typ.json')

    dest_dir_prog = os.path.join(dest_dir, 'program_type')
    clean_space_types(source_filename_2013, dest_dir_prog, vintage='2013')
    clean_space_types(source_filename_2010, dest_dir_prog, vintage='2010')
    clean_space_types(source_filename_2007, dest_dir_prog, vintage='2007')
    clean_space_types(source_filename_2004, dest_dir_prog, vintage='2004')
    clean_space_types(source_filename_1980_2004, dest_dir_prog, vintage='1980_2004')
    clean_space_types(source_filename_pre_1980, dest_dir_prog, vintage='pre_1980')

    # clean the materials JSON
    source_filename = os.path.join(ashrae_directory, 'data', 'ashrae_90_1.materials.json')
    global_mats = clean_materials(source_filename, dest_dir)

    # clean the constructions JSON
    source_filename = os.path.join(ashrae_directory, 'data', 'ashrae_90_1.constructions.json')
    global_constrs = clean_constructions(source_filename, dest_dir)

    # clean the ConstructionSets
    source_filename_2013 = os.path.join(
        ashrae_directory, 'ashrae_90_1_2013', 'data',
        'ashrae_90_1_2013.construction_properties.json')
    source_filename_2010 = os.path.join(
        ashrae_directory, 'ashrae_90_1_2010', 'data',
        'ashrae_90_1_2010.construction_properties.json')
    source_filename_2007 = os.path.join(
        ashrae_directory, 'ashrae_90_1_2007', 'data',
        'ashrae_90_1_2007.construction_properties.json')
    source_filename_2004 = os.path.join(
        ashrae_directory, 'ashrae_90_1_2004', 'data',
        'ashrae_90_1_2004.construction_properties.json')
    source_filename_1980_2004 = os.path.join(
        ashrae_directory, 'doe_ref_1980_2004', 'data',
        'doe_ref_1980_2004.construction_properties.json')
    source_filename_pre_1980 = os.path.join(
        ashrae_directory, 'doe_ref_pre_1980', 'data',
        'doe_ref_pre_1980.construction_properties.json')

    dest_dir_c_set = os.path.join(dest_dir, 'construction_set')
    clean_construction_sets(source_filename_2013, dest_dir_c_set, '2013',
                            global_constrs[0], global_mats[0])
    clean_construction_sets(source_filename_2010, dest_dir_c_set, '2010',
                            global_constrs[0], global_mats[0])
    clean_construction_sets(source_filename_2007, dest_dir_c_set, '2007',
                            global_constrs[0], global_mats[0])

    clean_construction_sets(source_filename_2004, dest_dir_c_set, '2004',
                            global_constrs[0], global_mats[0])
    clean_construction_sets(source_filename_1980_2004, dest_dir_c_set, '1980_2004',
                            global_constrs[0], global_mats[0])
    clean_construction_sets(source_filename_pre_1980, dest_dir_c_set, 'pre_1980',
                            global_constrs[0], global_mats[0])
