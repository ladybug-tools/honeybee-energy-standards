# coding=utf-8
"""Convert all standards gem JSONs to Honeybee JSONs."""
import honeybee_energy.lib.materials as mat_lib
import honeybee_energy.lib.constructions as constr_lib
import honeybee_energy.lib.constructionsets as constrset_lib
import honeybee_energy.lib.schedules as sch_lib
import honeybee_energy.lib.programtypes as program_lib

import os
import shutil
import json
import re


def local_data_dir():
    current_dir = os.path.dirname(__file__)
    return os.path.split(current_dir)[0]


def honeybee_construction_json(source_directory, constr_folder, lib_function, file_name):
    opa_mat_json = os.path.join(source_directory, file_name)
    hb_dict = {}
    with open(opa_mat_json, 'r') as json_file:
        mat_dict = json.load(json_file)
    for mat_name in mat_dict:
        try:
            hb_dict[mat_name] = lib_function(mat_name).to_dict(abridged=True)
        except Exception:
            hb_dict[mat_name] = lib_function(mat_name).to_dict()
    mat_path = os.path.join(constr_folder, file_name)
    with open(mat_path, 'w') as fp:
        json.dump(hb_dict, fp, indent=2)


def convert_to_hb_json(source_dir=None, dest_dir=None):
    """Convert OpenStudio standards JSON files into Honeybee JSON files.
    
    Args:
        source_dir: Directory to the cleaned OpenStudio Standards JSONs.
            Default will be the data folder in this package.
        dest_dir: Optional path to a destination directory. Default will be the
            data folder in this package.
    """
    # set default directories
    if source_dir is None:
        master_dir = local_data_dir()
        source_dir = os.path.join(master_dir, 'standards_data')
    if dest_dir is None:
        master_dir = local_data_dir()
        dest_dir = os.path.join(master_dir, 'data')
    
    # get all of the destination folders
    constr_dir = os.path.join(dest_dir, 'constructions')
    constrset_dir = os.path.join(dest_dir, 'constructionsets')
    sched_dir = os.path.join(dest_dir, 'schedules')
    ptype_dir = os.path.join(dest_dir, 'programtypes')
    
    # translate the materials and constructions to honeybee_json
    honeybee_construction_json(source_dir, constr_dir, mat_lib.opaque_material_by_name,
                               'opaque_material.json')
    honeybee_construction_json(source_dir, constr_dir, mat_lib.window_material_by_name,
                               'window_material.json')
    honeybee_construction_json(
        source_dir, constr_dir, constr_lib.opaque_construction_by_name,
        'opaque_construction.json')
    honeybee_construction_json(
        source_dir, constr_dir, constr_lib.window_construction_by_name,
        'window_construction.json')

    # translate the construction sets to honeybee_json
    src_constr_set_dir = os.path.join(source_dir, 'construction_set')
    for f in os.listdir(src_constr_set_dir):
        dest_file = os.path.join(constrset_dir, f)
        f_path = os.path.join(src_constr_set_dir, f)
        if os.path.isfile(f_path) and f_path.endswith('.json'):
            with open(f_path, 'r') as json_file:
                c_dict = json.load(json_file)
            hb_dict = {}
            for c_name in c_dict:
                hb_dict[c_name] = \
                    constrset_lib.construction_set_by_name(c_name).to_dict(abridged=True)
            with open(dest_file, 'w') as fp:
                json.dump(hb_dict, fp, indent=2)
    
    # translate schedules to honeybee json
    sched_json = os.path.join(source_dir, 'schedule.json')
    hb_sch_dict = {}
    with open(sched_json, 'r') as json_file:
        sch_dict = json.load(json_file)
    for sch_name in sch_dict:
        hb_sch_dict[sch_name] = sch_lib.schedule_by_name(sch_name).to_dict(abridged=True)
    # get a string representation and clean it further
    init_str = json.dumps(hb_sch_dict, indent=2)
    new_str = re.sub(r'\s*(\d*\.\d*),\s*', r'\1, ', init_str)
    right_bracket_str = re.sub(r'\s*(])', r'\1', new_str)
    left_bracket_str = re.sub(r'(\[)\s*', r'\1', right_bracket_str)
    final_str = re.sub(r'\[(.\d*),\s*(.\d*)\]', r'[\1, \2]', left_bracket_str)
    # write the data into a file
    sch_path = os.path.join(sched_dir, 'schedule.json')
    with open(sch_path, 'w') as fp:
        fp.write(final_str)
    
    # translate the program types to honeybee json
    src_ptype_dir = os.path.join(source_dir, 'program_type')
    for f in os.listdir(src_ptype_dir):
        f_path = os.path.join(src_ptype_dir, f)
        if os.path.isfile(f_path) and f_path.endswith('.json') \
                and not f_path.endswith('registry.json'):
            with open(f_path, 'r') as json_file:
                p_dict = json.load(json_file)
            hb_dict = {}
            for p_name in p_dict:
                hb_dict[p_name] = \
                    program_lib.program_type_by_name(p_name).to_dict(abridged=True)
            dest_file = os.path.join(ptype_dir, f)
            with open(dest_file, 'w') as fp:
                json.dump(hb_dict, fp, indent=2)
    
    # copy the program registry files over to the data folder
    for f in os.listdir(src_ptype_dir):
        f_path = os.path.join(src_ptype_dir, f)
        if os.path.isfile(f_path) and f_path.endswith('registry.json'):
            dest_file = os.path.join(ptype_dir, f)
            shutil.copy(f_path, dest_file)
