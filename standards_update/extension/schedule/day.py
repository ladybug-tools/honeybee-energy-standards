# coding=utf-8
"""Classmethods for honeybee-energy ScheduleDay."""


def from_standards_dict(cls, data):
    """Create a ScheduleDay from an OpenStudio standards gem dictionary.

    Args:
        data: Standards gem dictionary of a ScheduleDay following the format below.

    .. code-block:: python

        {
        "name": "Large Office Bldg Occ",
        "category": "Occupancy",
        "units": null,
        "day_types": "Default",
        "start_date": "2014-01-01T00:00:00+00:00",
        "end_date": "2014-12-31T00:00:00+00:00",
        "type": "Hourly",
        "notes": "From DOE Reference Buildings ",
        "values": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.95, 0.95, 0.95,
                   0.95, 0.5, 0.95, 0.95, 0.95, 0.95, 0.7, 0.4, 0.4, 0.1,
                   0.1, 0.05, 0.05]
        }
    """
    if len(data['values']) == 24:
        return cls.from_values_at_timestep(data['name'], data['values'])
    elif len(data['values']) == 1:
        return cls(data['name'], data['values'])  # single value in the schedule
    else:
        raise ValueError('Schedule "{}" has an illegal number of values: {}. '
                         'Must be 1 or 24.'.format(data['name'], len(data['values'])))
