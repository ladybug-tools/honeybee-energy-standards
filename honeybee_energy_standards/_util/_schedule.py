# coding=utf-8
"""Clean the schedule data."""
import re
import os
import json
from datetime import datetime


def clean_schedules(source_filename, dest_directory):
    """Process the OpenStudio Standards Schedule dictionary and write out a clean version.

    Specifically, this method performs 3 cleaning operations:
        * Output resulting dictionary in a format with the name of the ScheduleRuleset
            as the key and a list of the relevant ScheduleDay dictionaries as values.
        * Remove meaningless Hour:Minute:Second from the dates over which to apply
            individual schedule rules and remove the year as well.
        * Fix schedule values lists that do not have the correct number of values (this
            should be either 1 or 24 but some appear to have 2).
        * Remove all 'DummySmrDsn' and 'DummrySmrDsn' rules (I think the second one might
            be a typo but there's one in the gem now).
        * Fix the 'WtrDsn' typo (it should be 'WntrDsn' like all of the other schedules).
        * Un-indent lists of schedule day values, which results in better readability and
            a significantly smaller file size.

    Args:
        source_filename: The full path to the schedule JSON in the OpenStudio
            standards gem. If the standards gem repo has been downloaded to one's
            machine this file is likely in a location like the following:
                C:/Users/[USERNAME]/Documents/GitHub/openstudio-standards/lib/
                openstudio-standards/standards/ashrae_90_1/data/ashrae_90_1.schedules.json
        dest_directory: The destination directory into which clean JSONs will be written.
            If you are trying to update the files within the honeybee_standards repo,
            you likely want to write to the following location:
                C:/Users/[USERNAME]/Documents/GitHub/honeybee-standards/honeybee_standards/data/

    Returns:
        dest_file_path: The file path to the clean JSON.
    """
    # list of all the day types to remove
    _remove_day_types = ('DummySmrDsn', 'DummrySmrDsn')

    # initialize the clean dictionary
    sch_dict = {}

    # extract data from the raw standards gem json file
    with open(source_filename, 'r') as f:
        data_store = json.load(f)

    # group the data by parent ScheduleRuleset
    for sch in data_store['schedules']:
        sch_name = sch['name']
        if sch_name in sch_dict:
            sch_dict[sch_name].append(sch)
        else:
            sch_dict[sch_name] = [sch]

    # clean the datetime strings to only have the month and day
    for full_sched in sch_dict.values():
        for sched_rule in full_sched:
            sched_rule['start_date'] = clean_dt(sched_rule['start_date'])
            sched_rule['end_date'] = clean_dt(sched_rule['end_date'])

    # clean the datetime strings to only have the month and day
    for full_sched in sch_dict.values():
        for sched_rule in full_sched:
            val_len = len(sched_rule['values'])
            if val_len == 1 or val_len == 24:
                pass
            else:
                print('Schedule "{}" has an incorrect number of values'.format(
                    sched_rule['name']))
                sched_rule['values'] = [sched_rule['values'][0]]

    # Remove the day types that are not supported and fix the 'WtrDsn' typo
    for full_sched in sch_dict.values():
        del_indices = []
        for i, sched_rule in enumerate(full_sched):
            if sched_rule['day_types'] in _remove_day_types:
                del_indices.append(i)
            sched_rule['day_types'] = sched_rule['day_types'].replace('WtrDsn', 'WntrDsn')
        for i in del_indices:
            del full_sched[i]

    # get a string representation and clean it further
    init_str = json.dumps(sch_dict, indent=2)
    new_str = re.sub(r'\s*(\d*\.\d*),\s*', r'\1, ', init_str)
    right_bracket_str = re.sub(r'\s*(])', r'\1', new_str)
    clean_str = re.sub(r'(\[)\s*', r'\1', right_bracket_str)

    # write the data into a file
    dest_file_path = os.path.join(dest_directory, 'schedule.json')
    with open(dest_file_path, 'w') as fp:
        fp.write(clean_str)

    return dest_file_path


def remove_unused_schedules(clean_schedule_json=None, clean_program_type_jsons=None):
    """Remove any unused schedule from a clean schedule JSON.

    Args:
        clean_schedule_json: File path to a clean schedule JSON. If None, this
            method will search for the file in the 'data' folder of this library.
        clean_program_type_jsons: List of file paths to clean program_type JSONS.
            If None this method will search for the file in the 'data/program_type'
            folder of this library.
    """
    # gather the relevant files
    if clean_schedule_json is None:
        likely_dir_1 = os.path.join(os.path.dirname(__file__), '../data')
        clean_schedule_json = os.path.join(likely_dir_1, 'schedule.json')
    if clean_program_type_jsons is None:
        likely_dir_2 = os.path.join(os.path.dirname(__file__), '../data/program_type')
        clean_program_type_jsons = [os.path.join(likely_dir_2, jsf)
                                    for jsf in os.listdir(likely_dir_2) if 'data' in jsf]

    # add some of the extra useful schedules
    all_schedules = set()
    also_include = ('Always Off', 'Always On')
    for name in also_include:
        all_schedules.add(name)

    # gather all schedules used by the program types
    for vintage in clean_program_type_jsons:
        with open(vintage, 'r') as f:
            data_store = json.load(f)
        for prog_type in data_store.values():
            for prop in prog_type.keys():
                if 'schedule' in prop:
                    all_schedules.add(prog_type[prop])

    # extract data from the scedules json file
    with open(clean_schedule_json, 'r') as f:
        sched_data_store = json.load(f)

    # loop through gathered schedules and make sure they get into the new schedule json
    new_sch_dict = {}
    for sch_name in all_schedules:
        new_sch_dict[sch_name] = sched_data_store[sch_name]

    # get a string representation and clean it further
    init_str = json.dumps(new_sch_dict, indent=2)
    new_str = re.sub(r'\s*(\d*\.\d*),\s*', r'\1, ', init_str)
    right_bracket_str = re.sub(r'\s*(])', r'\1', new_str)
    left_bracket_str = re.sub(r'(\[)\s*', r'\1', right_bracket_str)

    # write the data into a file
    with open(clean_schedule_json, 'w') as fp:
        fp.write(left_bracket_str)


def clean_dt(os_dt):
    """Clean a datetime string from OpenStudio to only reflect month and day."""
    dt = datetime.strptime(os_dt, '%Y-%m-%dT00:00:00+00:00')
    return dt.strftime('%m-%d')
