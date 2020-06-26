# coding=utf-8
"""Extend the honeybee_energy schedule library."""
from honeybee_energy.schedule.ruleset import ScheduleRuleset

from honeybee_energy.lib.schedules import _schedules

import os
import json


# load the standards gem data of schedules to Python dictionaries.
_data_dir = os.path.join(os.path.dirname(__file__), '../_standards_data')

try:
    _schedule_dir = os.path.join(_data_dir, 'schedule.json')
    with open(_schedule_dir, 'r') as f:
        _schedule_standards_dict = json.load(f)
except FileNotFoundError:
    _schedule_standards_dict = {}


def schedule_by_identifier(schedule_identifier):
    """Get a schedule from the library given its identifier.

    Args:
        schedule_identifier: A text string for the identifier of the schedule.
    """
    try:
        return _schedules[schedule_identifier]
    except KeyError:
        try:
            _sched_dict = _schedule_standards_dict[schedule_identifier]
        except KeyError:
            raise ValueError('"{}" was not found in the schedule library.'.format(
                schedule_identifier))

    # create the Python object from the standards gem dictionary
    _sched_obj = ScheduleRuleset.from_standards_dict(_sched_dict)
    _sched_obj.lock()
    _schedules[schedule_identifier] = _sched_obj  # load faster next time
    return _sched_obj
