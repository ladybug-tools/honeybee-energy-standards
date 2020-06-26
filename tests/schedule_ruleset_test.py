# coding=utf-8
from honeybee_energy.schedule.ruleset import ScheduleRuleset
import honeybee_energy.lib.scheduletypelimits as schedule_types
import honeybee_energy.lib.schedules as sched_lib

import json


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
