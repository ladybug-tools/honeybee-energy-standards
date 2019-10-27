# coding=utf-8
"""Classmethods for honeybee-energy ScheduleRuleset."""
from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.rule import ScheduleRule
import honeybee_energy.lib.scheduletypelimits as _type_lib

from ladybug.dt import Date


def from_standards_dict(cls, data):
    """Create a ScheduleRuleset from an OpenStudio standards gem dictionary.

    Args:
        data: A list of individual ScheduleDay dictionary descriptions from
            the standards gem that together define a complete ScheduleRuleset.
    """
    # map standards gem day types to integers
    _standards_gem_day_types = {
        'Sun': [1], 'Mon': [2], 'Tue': [3], 'Wed': [4], 'Thu': [5], 'Fri': [6],
        'Sat': [7], 'Hol': [8], 'Wknd': [1, 7], 'Wkdy': [2, 3, 4, 5, 6]}

    # empty variables to be replaced
    default_day = None
    summer_day = None
    winter_day = None
    schedule_rules = []

    # build the ScheduleDay objects and determine rules for when to apply them
    for day_sch_dict in data:
        schedule_day = ScheduleDay.from_standards_dict(day_sch_dict)
        day_types = day_sch_dict['day_types'].split('|')
        if 'Default' in day_types:
            default_day = schedule_day.duplicate()
            default_day.name = '{}_Default'.format(schedule_day.name)
            day_types.remove('Default')
        if 'SmrDsn' in day_sch_dict['day_types']:
            summer_day = schedule_day.duplicate()
            summer_day.name = '{}_SmrDsn'.format(schedule_day.name)
            day_types.remove('SmrDsn')
        if 'WntrDsn' in day_sch_dict['day_types']:
            winter_day = schedule_day.duplicate()
            winter_day.name = '{}_WntrDsn'.format(schedule_day.name)
            day_types.remove('WntrDsn')
        if len(day_types) != 0:  # there are rules for when to apply the schedule
            schedule_day.name = '{}_{}'.format(schedule_day.name, '|'.join(day_types))
            rule = ScheduleRule(schedule_day)
            for apply_day in day_types:
                apply_dows = _standards_gem_day_types[apply_day]
                for dow in apply_dows:
                    rule.apply_day_by_dow(dow)
            rule.start_date = _process_date_string(day_sch_dict['start_date'])
            rule.end_date = _process_date_string(day_sch_dict['end_date'])
            schedule_rules.append(rule)

    # attempt to determine a ScheduleTypeLimit from the units and category
    schedule_type = _type_from_standards_gem(
        day_sch_dict['units'], day_sch_dict['category'])

    # check that there is a default day
    if default_day is None:  # just try to pick one of the rules to be the default
        try:
            default_day = schedule_rules[0].schedule_day
            del schedule_rules[0]
        except IndexError:
            raise ValueError('No default_day_schedule or schedule rules were '
                             'found in the standards gem dictionary.')

    # return the schedule
    return cls(data[0]['name'], default_day, schedule_rules, schedule_type,
               summer_day, winter_day)


def _process_date_string(date_string):
    """Process DateTime strings from the OpenStudio standards gem format.

    Args:
        date_string: Examples: "2014-01-01T00:00:00+00:00", "01-01"
    """
    date_str = date_string.split('T')[0].split('-')
    return Date(int(date_str[-2]), int(date_str[-1]))


def _type_from_standards_gem(units, category):
    """Get ScheduleTypeLimit from 'units' and 'category' keys of standards gem."""
    fraction_categories = ('Lighting', 'Equipment', 'Infiltration',
                           'Occupancy', 'Elevator')
    on_off_categories = ('Operation', 'OA Air', 'Fan')
    if category in fraction_categories:
        return _type_lib.fractional
    if category in on_off_categories:
        return _type_lib.on_off
    if category == 'Activity':
        return _type_lib.activity_level
    if units == 'C':
        return _type_lib.temperature
    if units == 'W':
        return _type_lib.power
    if units == 'FRACTION':
        return _type_lib.fractional
    return None
