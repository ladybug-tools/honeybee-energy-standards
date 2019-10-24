# coding=utf-8
"""Extend the honeybee_energy schedule library."""
from honeybee_energy.schedule.ruleset import ScheduleRuleset

from honeybee_energy.lib.schedules import _idf_schedules

import os
import json


# load the standards gem data of schedules to Python dictionaries.
_data_dir = os.path.join(os.path.dirname(__file__), '../data')

_schedule_dir = os.path.join(_data_dir, 'schedule.json')
with open(_schedule_dir, 'r') as f:
    _schedule_standards_dict = json.load(f)


def schedule_by_name(schedule_name):
    """Get a schedule from the library given its name.

    Args:
        schedule_name: A text string for the name of the schedule.
    """
    try:
        return _idf_schedules[schedule_name]
    except KeyError:
        try:
            _sched_dict = _schedule_standards_dict[schedule_name]
        except KeyError:
            raise ValueError('"{}" was not found in the schedule library.'.format(
                schedule_name))

    # create the Python object from the standards gem dictionary
    _sched_obj = ScheduleRuleset.from_standards_dict(_sched_dict)
    _idf_schedules[schedule_name] = _sched_obj  # load faster next time
    return _sched_obj
