# coding=utf-8
from honeybee.room import Room
from honeybee.model import Model
from  honeybee.boundarycondition import boundary_conditions

from honeybee_energy.programtype import ProgramType
import honeybee_energy.lib.programtypes as prog_type_lib
from honeybee_energy.load.setpoint import Setpoint

from ladybug_geometry.geometry3d.pointvector import Vector3D

import pytest
import json


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



def test_building_mix():
    """Test that the building_mix ratios."""
    bld_mix_file = './honeybee_energy_standards/building_mix.json'
    with open(bld_mix_file) as inf:
        bld_mix_dict = json.load(inf)

    for building in bld_mix_dict.values():
        for program in building:
            prog_from_lib = prog_type_lib.program_type_by_identifier(program)
            assert isinstance(prog_from_lib, ProgramType)
        total_fracts = sum(f for f in building.values())
        assert total_fracts == pytest.approx(1, rel=1e-3)
