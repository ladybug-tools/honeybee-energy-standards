# coding=utf-8
from honeybee_energy.schedule.day import ScheduleDay


def test_schedule_day_from_standards_dict():
    """Test the ScheduleDay from_standards_dict method."""
    test_dict_1 = {
        "name": "Large Office Bldg Light",
        "category": "Lighting",
        "units": None,
        "day_types": "Sun",
        "start_date": "2014-01-01T00:00:00+00:00",
        "end_date": "2014-12-31T00:00:00+00:00",
        "type": "Constant",
        "notes": "From DOE Reference Buildings ",
        "values": [0.0]}
    test_dict_2 = {
        "name": "Large Office Bldg Occ",
        "category": "Occupancy",
        "units": None,
        "day_types": "Default",
        "start_date": "2014-01-01T00:00:00+00:00",
        "end_date": "2014-12-31T00:00:00+00:00",
        "type": "Hourly",
        "notes": "From DOE Reference Buildings ",
        "values": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.95, 0.95, 0.95, 0.95, 0.5,
                   0.95, 0.95, 0.95, 0.95, 0.7, 0.4, 0.4, 0.1, 0.1, 0.05, 0.05]}
    schedule_1 = ScheduleDay.from_standards_dict(test_dict_1)
    schedule_2 = ScheduleDay.from_standards_dict(test_dict_2)

    assert schedule_1.name == "Large Office Bldg Light"
    assert schedule_1.is_constant
    assert schedule_1[0] == 0

    assert schedule_2.name == "Large Office Bldg Occ"
    assert not schedule_2.is_constant
    assert len(schedule_2) == 10
    assert schedule_2.values == (0, 0.1, 0.2, 0.95, 0.5, 0.95, 0.7, 0.4, 0.1, 0.05)
