# coding=utf-8
from honeybee.room import Room
from honeybee.model import Model
from  honeybee.boundarycondition import boundary_conditions

from honeybee_energy.programtype import ProgramType
import honeybee_energy.lib.programtypes as prog_type_lib
from honeybee_energy.load.setpoint import Setpoint

from ladybug_geometry.geometry3d.pointvector import Vector3D

import pytest


def test_program_type_from_standards_dict():
    """Test the from_standards_dict methods."""
    program_dict = {
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
    office_program = ProgramType.from_standards_dict(program_dict)

    assert office_program.identifier == 'MediumOffice - OpenOffice'
    assert office_program.people.people_per_area == pytest.approx(0.05651, rel=1e-3)
    assert office_program.people.occupancy_schedule.identifier == 'OfficeMedium BLDG_OCC_SCH'
    assert office_program.people.activity_schedule.identifier == 'OfficeMedium ACTIVITY_SCH'
    assert office_program.lighting.watts_per_area == pytest.approx(10.548, rel=1e-3)
    assert office_program.lighting.schedule.identifier == 'OfficeMedium BLDG_LIGHT_SCH_2013'
    assert office_program.lighting.return_air_fraction == pytest.approx(0.0, rel=1e-3)
    assert office_program.lighting.radiant_fraction == pytest.approx(0.7, rel=1e-3)
    assert office_program.lighting.visible_fraction == pytest.approx(0.2, rel=1e-3)
    assert office_program.electric_equipment.watts_per_area == pytest.approx(10.3333, rel=1e-3)
    assert office_program.electric_equipment.schedule.identifier == 'OfficeMedium BLDG_EQUIP_SCH_2013'
    assert office_program.electric_equipment.latent_fraction == pytest.approx(0.0, rel=1e-3)
    assert office_program.electric_equipment.radiant_fraction == pytest.approx(0.5, rel=1e-3)
    assert office_program.electric_equipment.lost_fraction == pytest.approx(0.0, rel=1e-3)
    assert office_program.gas_equipment is None
    assert office_program.infiltration.flow_per_exterior_area == pytest.approx(0.000226568, rel=1e-3)
    assert office_program.infiltration.schedule.identifier == 'OfficeMedium INFIL_SCH_PNNL'
    assert office_program.ventilation.flow_per_person == pytest.approx(0.0023597, rel=1e-3)
    assert office_program.ventilation.flow_per_area == pytest.approx(0.0003048, rel=1e-3)
    assert office_program.ventilation.flow_per_zone == pytest.approx(0.0, rel=1e-3)
    assert office_program.ventilation.air_changes_per_hour == pytest.approx(0.0, rel=1e-3)
    assert office_program.setpoint.heating_schedule.identifier == 'OfficeMedium HTGSETP_SCH_YES_OPTIMUM'
    assert office_program.setpoint.heating_setpoint == pytest.approx(21.0, rel=1e-3)
    assert office_program.setpoint.heating_setback == pytest.approx(15.6, rel=1e-3)
    assert office_program.setpoint.cooling_schedule.identifier == 'OfficeMedium CLGSETP_SCH_YES_OPTIMUM'
    assert office_program.setpoint.cooling_setpoint == pytest.approx(24.0, rel=1e-3)
    assert office_program.setpoint.cooling_setback == pytest.approx(26.7, rel=1e-3)


def test_program_type_lib():
    """Test that the honeybee-energy lib has been extended with new program type data."""
    assert len(prog_type_lib.PROGRAM_TYPES) > 2  # should now have many more constructions

    prog_from_lib = prog_type_lib.program_type_by_identifier(prog_type_lib.PROGRAM_TYPES[0])
    assert isinstance(prog_from_lib, ProgramType)

    prog_from_lib = prog_type_lib.program_type_by_identifier(prog_type_lib.PROGRAM_TYPES[2])
    assert isinstance(prog_from_lib, ProgramType)


def test_program_type_by_identifier():
    """Test that all of the program types in the library can be loaded by identifier."""
    for prog in prog_type_lib.PROGRAM_TYPES:
        prog_from_lib = prog_type_lib.program_type_by_identifier(prog)
        assert isinstance(prog_from_lib, ProgramType)


def test_model_to_dict_with_program_type():
    """Test Model.to_dict() with standards ProgramTypes."""
    pat_room_program = prog_type_lib.program_type_by_identifier('2013::Hospital::ICU_PatRm')
    room = Room.from_box('Hospital_Patient_Room', 5, 10, 3)
    room.properties.energy.program_type = pat_room_program

    room.properties.energy.add_default_ideal_air()
    ideal_air = room.properties.energy.hvac.duplicate()
    ideal_air.economizer_type = 'DifferentialEnthalpy'
    ideal_air.sensible_heat_recovery = 0.81
    ideal_air.latent_heat_recovery = 0.68
    room.properties.energy.hvac = ideal_air

    pat_rm_setpoint = room.properties.energy.setpoint.duplicate()
    pat_rm_setpoint.identifier = 'Humidity Controlled PatRm Setpt'
    pat_rm_setpoint.heating_setpoint = 21
    pat_rm_setpoint.cooling_setpoint = 24
    pat_rm_setpoint.humidifying_setpoint = 30
    pat_rm_setpoint.dehumidifying_setpoint = 55
    room.properties.energy.setpoint = pat_rm_setpoint

    south_face = room[3]
    south_face.apertures_by_ratio(0.4, 0.01)
    south_face.apertures[0].overhang(0.5, indoor=False)
    south_face.move_shades(Vector3D(0, 0, -0.5))

    room[0].boundary_condition = boundary_conditions.adiabatic
    room[1].boundary_condition = boundary_conditions.adiabatic
    room[2].boundary_condition = boundary_conditions.adiabatic
    room[4].boundary_condition = boundary_conditions.adiabatic
    room[5].boundary_condition = boundary_conditions.adiabatic

    model = Model('Patient_Room_Test_Box', [room])
    model_dict = model.to_dict()

    assert model_dict['properties']['energy']['program_types'][0]['identifier'] == \
        '2013::Hospital::ICU_PatRm'
    assert model_dict['rooms'][0]['properties']['energy']['program_type'] == \
        '2013::Hospital::ICU_PatRm'
    assert 'setpoint' in model_dict['rooms'][0]['properties']['energy']
    assert model_dict['rooms'][0]['properties']['energy']['setpoint']['identifier'] == \
        'Humidity Controlled PatRm Setpt'
    assert 'hvac' in model_dict['rooms'][0]['properties']['energy']
