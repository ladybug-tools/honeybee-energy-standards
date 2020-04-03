# coding=utf-8
from honeybee_energy.schedule.ruleset import ScheduleRuleset
import honeybee_energy.lib.scheduletypelimits as schedule_types
import honeybee_energy.lib.schedules as sched_lib

import json


def test_schedule_from_standards_dict():
    """Test the ScheduleRuleset from_standards_dict method."""
    filename = './tests/standards/OpenStudio_Standards_schedule.json'
    if filename:
        with open(filename, 'r') as f:
            data_store = json.load(f)
    office_sch = ScheduleRuleset.from_standards_dict(data_store['Large Office Bldg Occ'])

    assert office_sch.identifier == "Large Office Bldg Occ"
    assert office_sch.default_day_schedule.identifier == "Large Office Bldg Occ_Default"
    assert len(office_sch.default_day_schedule) == 10
    assert len(office_sch.schedule_rules) == 2
    assert office_sch.summer_designday_schedule.identifier == 'Large Office Bldg Occ_SmrDsn'
    assert len(office_sch.summer_designday_schedule) == 3
    assert office_sch.winter_designday_schedule.identifier == 'Large Office Bldg Occ_WntrDsn'
    assert len(office_sch.winter_designday_schedule) == 1
    assert office_sch.schedule_type_limit == schedule_types.fractional


def test_schedule_lib():
    """Test that the honeybee-energy lib has been extended with new schedule data."""
    assert len(sched_lib.SCHEDULES) > 8  # should now have many more schedules

    sched_from_lib = sched_lib.schedule_by_identifier(sched_lib.SCHEDULES[0])
    assert isinstance(sched_from_lib, ScheduleRuleset)

    sched_from_lib = sched_lib.schedule_by_identifier(sched_lib.SCHEDULES[8])
    assert isinstance(sched_from_lib, ScheduleRuleset)


def test_schedule_by_identifier():
    """Test that all of the schedules in the library can be loaded by identifier."""
    for sched in sched_lib.SCHEDULES:
        sched_from_lib = sched_lib.schedule_by_identifier(sched)
        assert isinstance(sched_from_lib, ScheduleRuleset)
