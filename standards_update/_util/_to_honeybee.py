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


def honeybee_construction_json(
        source_directory, constr_folder, lib_function, file_name, extra_objs=None):
    opa_mat_json = os.path.join(source_directory, file_name)
    hb_dict = {}
    with open(opa_mat_json, 'r') as json_file:
        mat_dict = json.load(json_file)
    for mat_id in mat_dict:
        try:
            hb_dict[mat_id] = lib_function(mat_id).to_dict(abridged=True)
        except Exception:
            hb_dict[mat_id] = lib_function(mat_id).to_dict()
    if extra_objs is not None:
        for e_obj in extra_objs:
            with open(e_obj, 'r') as f:
                hb_dict.update(json.load(f))
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
        source_dir = os.path.join(master_dir, '_standards_data')
    if dest_dir is None:
        master_dir = local_data_dir()
        dest_dir = os.path.join(master_dir, 'data')

    # get all of the destination folders
    constr_dir = os.path.join(dest_dir, 'constructions')
    constrset_dir = os.path.join(dest_dir, 'constructionsets')
    sched_dir = os.path.join(dest_dir, 'schedules')
    ptype_dir = os.path.join(dest_dir, 'programtypes')
    ptype_reg_dir = os.path.join(dest_dir, 'programtypes_registry')

    # translate the materials and constructions to honeybee_json
    extra_folder = os.path.join(os.path.split(os.path.dirname(__file__))[0], '_extra')
    honeybee_construction_json(
        source_dir, constr_dir, mat_lib.opaque_material_by_identifier,
        'opaque_material.json', [os.path.join(extra_folder, 'ground_materials.json')])
    honeybee_construction_json(
        source_dir, constr_dir, mat_lib.window_material_by_identifier,
        'window_material.json')
    honeybee_construction_json(
        source_dir, constr_dir, constr_lib.opaque_construction_by_identifier,
        'opaque_construction.json', [os.path.join(extra_folder, 'ground_constructions.json')])
    honeybee_construction_json(
        source_dir, constr_dir, constr_lib.window_construction_by_identifier,
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
            for c_id in c_dict:
                base_dict = \
                    constrset_lib.construction_set_by_identifier(c_id).to_dict(abridged=True)
                del_keys = []
                for key in base_dict:
                    if base_dict[key] is None:
                        del_keys.append(key)
                    elif isinstance(base_dict[key], dict):
                        sub_del_keys = []
                        for s_key in base_dict[key]:
                            if base_dict[key][s_key] is None:
                                sub_del_keys.append(s_key)
                        for s_key in sub_del_keys:
                            del base_dict[key][s_key]
                for key in del_keys:
                    del base_dict[key]
                hb_dict[c_id] = base_dict
            with open(dest_file, 'w') as fp:
                json.dump(hb_dict, fp, indent=2)

    # translate schedules to honeybee json
    sched_json = os.path.join(source_dir, 'schedule.json')
    hb_sch_dict = {}
    with open(sched_json, 'r') as json_file:
        sch_dict = json.load(json_file)
    for sch_id in sch_dict:
        hb_sch_dict[sch_id] = sch_lib.schedule_by_identifier(sch_id).to_dict(abridged=True)
    # get a string representation and clean it further
    init_str = json.dumps(hb_sch_dict, indent=2)
    new_str = re.sub(r'\s*(\d*\.\d*),\s*', r'\1, ', init_str)
    right_bracket_str = re.sub(r'\s*(])', r'\1', new_str)
    left_bracket_str = re.sub(r'(\[)\s*', r'\1', right_bracket_str)
    newer_str = re.sub(r'\[(.\d*),\s*(.\d*)\],\s*', r'[\1, \2], ', left_bracket_str)
    final_str = re.sub(r'\[(.\d*),\s*(.\d*)\]', r'[\1, \2]', newer_str)
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
            for p_id in p_dict:
                hb_dict[p_id] = \
                    program_lib.program_type_by_identifier(p_id).to_dict(abridged=True)
            dest_file = os.path.join(ptype_dir, f)
            with open(dest_file, 'w') as fp:
                json.dump(hb_dict, fp, indent=2)

    # copy the program registry files over to the data folder
    for f in os.listdir(src_ptype_dir):
        f_path = os.path.join(src_ptype_dir, f)
        if os.path.isfile(f_path) and f_path.endswith('registry.json'):
            dest_file = os.path.join(ptype_reg_dir, f)
            shutil.copy(f_path, dest_file)

    print('Successfully translated OpenStudio JSONs to Honeybee.')


def remove_hb_jsons(dest_dir=None):
    """Remove all Honeybee JSON data from this package.

    Args:
        dest_dir: Optional path to a destination directory. Default will be the
            data folder in this package.
    """
    if dest_dir is None:
        master_dir = local_data_dir()
        dest_dir = os.path.join(master_dir, 'data')

    con_dir = os.path.join(dest_dir, 'constructions')
    for file_name in os.listdir(con_dir):
        json_file = os.path.join(con_dir, file_name)
        if file_name.endswith('.json') and os.path.isfile(json_file):
            os.remove(json_file)

    con_set_dir = os.path.join(dest_dir, 'constructionsets')
    for file_name in os.listdir(con_set_dir):
        json_file = os.path.join(con_set_dir, file_name)
        if file_name.endswith('.json') and os.path.isfile(json_file):
            os.remove(json_file)

    sch_dir = os.path.join(dest_dir, 'schedules')
    for file_name in os.listdir(sch_dir):
        json_file = os.path.join(sch_dir, file_name)
        if file_name.endswith('.json') and os.path.isfile(json_file):
            os.remove(json_file)

    ptype_dir = os.path.join(dest_dir, 'programtypes')
    for file_name in os.listdir(ptype_dir):
        json_file = os.path.join(ptype_dir, file_name)
        if file_name.endswith('.json') and os.path.isfile(json_file):
            os.remove(json_file)

    ptype_reg_dir = os.path.join(dest_dir, 'programtypes_registry')
    for file_name in os.listdir(ptype_reg_dir):
        json_file = os.path.join(ptype_reg_dir, file_name)
        if file_name.endswith('.json') and os.path.isfile(json_file):
            os.remove(json_file)
