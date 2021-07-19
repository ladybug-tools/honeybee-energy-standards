"""Classmethod for honeybee-energy program type."""
from __future__ import division

import honeybee_energy.lib.schedules as sch_lib

from honeybee_energy.load.people import People
from honeybee_energy.load.lighting import Lighting
from honeybee_energy.load.equipment import ElectricEquipment, GasEquipment
from honeybee_energy.load.hotwater import ServiceHotWater
from honeybee_energy.load.infiltration import Infiltration
from honeybee_energy.load.ventilation import Ventilation
from honeybee_energy.load.setpoint import Setpoint


def from_standards_dict(cls, data):
    """Create a ProgramType from an OpenStudio standards gem dictionary.

    Args:
        data: An OpenStudio standards dictionary of a space type in the
            format below.

    .. code-block:: python

        {
        "template": "90.1-2013",
        "building_type": "Office",
        "space_type": "MediumOffice - OpenOffice",
        "lighting_standard": "ASHRAE 90.1-2013",
        "lighting_per_area": 0.98,
        "lighting_per_person": None,
        "additional_lighting_per_area": None,
        "lighting_fraction_to_return_air": 0.0,
        "lighting_fraction_radiant": 0.7,
        "lighting_fraction_visible": 0.2,
        "lighting_schedule": "OfficeMedium BLDG_LIGHT_SCH_2013",
        "ventilation_standard": "ASHRAE 62.1-2007",
        "ventilation_primary_space_type": "Office Buildings",
        "ventilation_secondary_space_type": "Office space",
        "ventilation_per_area": 0.06,
        "ventilation_per_person": 5.0,
        "ventilation_air_changes": None,
        "minimum_total_air_changes": None,
        "occupancy_per_area": 5.25,
        "occupancy_schedule": "OfficeMedium BLDG_OCC_SCH",
        "occupancy_activity_schedule": "OfficeMedium ACTIVITY_SCH",
        "infiltration_per_exterior_area": 0.0446,
        "infiltration_schedule": "OfficeMedium INFIL_SCH_PNNL",
        "gas_equipment_per_area": None,
        "gas_equipment_fraction_latent": None,
        "gas_equipment_fraction_radiant": None,
        "gas_equipment_fraction_lost": None,
        "gas_equipment_schedule": None,
        "electric_equipment_per_area": 0.96,
        "electric_equipment_fraction_latent": 0.0,
        "electric_equipment_fraction_radiant": 0.5,
        "electric_equipment_fraction_lost": 0.0,
        "electric_equipment_schedule": "OfficeMedium BLDG_EQUIP_SCH_2013",
        "heating_setpoint_schedule": "OfficeMedium HTGSETP_SCH_YES_OPTIMUM",
        "cooling_setpoint_schedule": "OfficeMedium CLGSETP_SCH_YES_OPTIMUM"
        }
    """
    pr_type_identifier = data['space_type']
    people = None
    lighting = None
    electric_equipment = None
    gas_equipment = None
    hot_water = None
    infiltration = None
    ventilation = None
    setpoint = None

    if 'occupancy_schedule' in data and data['occupancy_schedule'] is not None and \
            'occupancy_per_area' in data and data['occupancy_per_area'] != 0:
        occ_sched = sch_lib.schedule_by_identifier(data['occupancy_schedule'])
        act_sched = sch_lib.schedule_by_identifier(data['occupancy_activity_schedule'])
        occ_density = data['occupancy_per_area'] / 92.903
        people = People('{}_People'.format(pr_type_identifier), occ_density,
                        occ_sched, act_sched)

    if 'lighting_schedule' in data and data['lighting_schedule'] is not None:
        light_sched = sch_lib.schedule_by_identifier(data['lighting_schedule'])
        try:
            lpd = data['lighting_per_area'] * 10.7639
        except (TypeError, KeyError):
            lpd = 0  # there's a schedule but no actual load object
        try:
            raf = data['lighting_fraction_to_return_air']
        except KeyError:
            raf = 0
        try:
            lfr = data['lighting_fraction_radiant']
        except KeyError:
            lfr = 0.32
        try:
            lfv = data['lighting_fraction_visible']
        except KeyError:
            lfv = 0.25
        lighting = Lighting(
            '{}_Lighting'.format(pr_type_identifier), lpd, light_sched, raf, lfr, lfv)
        lighting.baseline_watts_per_area = lpd

    if 'electric_equipment_schedule' in data and \
            data['electric_equipment_schedule'] is not None:
        eequip_sched = sch_lib.schedule_by_identifier(data['electric_equipment_schedule'])
        try:
            eepd = data['electric_equipment_per_area'] * 10.7639
        except KeyError:
            eepd = 0  # there's a schedule but no actual load object
        electric_equipment = ElectricEquipment(
            '{}_Electric'.format(pr_type_identifier), eepd, eequip_sched,
            data['electric_equipment_fraction_radiant'],
            data['electric_equipment_fraction_latent'],
            data['electric_equipment_fraction_lost'])

    if 'gas_equipment_schedule' in data and \
            data['gas_equipment_schedule'] is not None:
        gequip_sched = sch_lib.schedule_by_identifier(data['gas_equipment_schedule'])
        try:
            gepd = data['gas_equipment_per_area'] * 3.15459
        except (TypeError, KeyError):
            gepd = 0  # there's a schedule but no actual load object
        gas_equipment = GasEquipment(
            '{}_Gas'.format(pr_type_identifier), gepd, gequip_sched,
            data['gas_equipment_fraction_radiant'],
            data['gas_equipment_fraction_latent'],
            data['gas_equipment_fraction_lost'])

    if 'service_water_heating_schedule' in data and \
            data['service_water_heating_schedule'] is not None:
        shw_sch = sch_lib.schedule_by_identifier(data['service_water_heating_schedule'])
        try:
            shw_load = data['service_water_heating_peak_flow_per_area'] * 40.7458
        except (TypeError, KeyError):
            shw_load = 0  # there's a schedule but no actual load object
        try:
            shw_temp = round(
                (data['service_water_heating_target_temperature'] - 32.) * 5. / 9.)
        except (TypeError, KeyError):
            shw_temp = 60
        try:
            fs = data['service_water_heating_fraction_sensible']
        except (TypeError, KeyError):
            fs = 0.2
        try:
            fl = data['service_water_heating_fraction_latent']
        except (TypeError, KeyError):
            fl = 0.05
        hot_water = ServiceHotWater(
            '{}_SHW'.format(pr_type_identifier), shw_load, shw_sch, shw_temp, fs, fl)

    if 'infiltration_schedule' in data and \
            data['infiltration_schedule'] is not None:
        inf_sched = sch_lib.schedule_by_identifier(data['infiltration_schedule'])
        try:
            inf = data['infiltration_per_exterior_area'] * 0.00508
        except KeyError:  # might be using infiltration_per_exterior_wall_area
            try:
                inf = data['infiltration_per_exterior_wall_area'] * 0.00508
            except KeyError:
                inf = 0  # there's a schedule but no actual load object
        infiltration = Infiltration(
            '{}_Infiltration'.format(pr_type_identifier), inf, inf_sched)

    if 'ventilation_standard' in data and \
            data['ventilation_standard'] is not None:
        person = data['ventilation_per_person'] * 0.000471947 if \
            'ventilation_per_person' in data and \
            data['ventilation_per_person'] is not None else 0
        area = data['ventilation_per_area'] * 0.00508 if \
            'ventilation_per_area' in data and \
            data['ventilation_per_area'] is not None else 0
        ach = data['ventilation_air_changes'] if \
            'ventilation_air_changes' in data and \
            data['ventilation_air_changes'] is not None else 0
        ventilation = Ventilation(
            '{}_Ventilation'.format(pr_type_identifier), person, area, 0, ach)

    if 'heating_setpoint_schedule' in data and \
            data['heating_setpoint_schedule'] is not None:
        heat_sched = sch_lib.schedule_by_identifier(data['heating_setpoint_schedule'])
        cool_sched = sch_lib.schedule_by_identifier(data['cooling_setpoint_schedule'])
        setpoint = Setpoint(
            '{}_Setpoint'.format(pr_type_identifier), heat_sched, cool_sched)

    return cls(data['space_type'], people, lighting, electric_equipment,
               gas_equipment, hot_water, infiltration, ventilation, setpoint)
