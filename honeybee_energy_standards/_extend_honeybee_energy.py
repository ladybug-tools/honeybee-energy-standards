# coding=utf-8
"""Extend honeybee-energy objects and lib with the classmethods and data of this library."""
# import all of the objects that are being extended from honyebee-energy
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass
from honeybee_energy.material.glazing import EnergyWindowMaterialGlazing, \
    EnergyWindowMaterialSimpleGlazSys
from honeybee_energy.material.gas import EnergyWindowMaterialGas
from honeybee_energy.construction.opaque import OpaqueConstruction
from honeybee_energy.construction.window import WindowConstruction
from honeybee_energy.constructionset import ConstructionSet
from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.programtype import ProgramType

from honeybee_energy.lib import materials
from honeybee_energy.lib import constructions
from honeybee_energy.lib import constructionsets
from honeybee_energy.lib import schedules
from honeybee_energy.lib import programtypes


# import all of the extension methods from this library
import honeybee_energy_standards.material.opaque as material_opaque
import honeybee_energy_standards.material.glazing as material_glazing
import honeybee_energy_standards.material.gas as material_gas
import honeybee_energy_standards.construction.opaque as construction_opaque
import honeybee_energy_standards.construction.window as window_opaque
import honeybee_energy_standards.constructionset as constructionset
import honeybee_energy_standards.schedule.day as schedule_day
import honeybee_energy_standards.schedule.ruleset as schedule_ruleset
import honeybee_energy_standards.programtype as programtype

import honeybee_energy_standards.lib.materials as material_lib
import honeybee_energy_standards.lib.constructions as construction_lib
import honeybee_energy_standards.lib.constructionsets as construction_set_lib
import honeybee_energy_standards.lib.schedules as schedule_lib
import honeybee_energy_standards.lib.programtypes as program_type_lib


# add classmethods to create honeybee-energy objects from standards gem dictionaries
EnergyMaterial.from_standards_dict = material_opaque.from_standards_dict
EnergyMaterialNoMass.from_standards_dict = material_opaque.no_mass_from_standards_dict
EnergyWindowMaterialGlazing.from_standards_dict = material_glazing.from_standards_dict
EnergyWindowMaterialSimpleGlazSys.from_standards_dict = material_glazing.simple_from_standards_dict
EnergyWindowMaterialGas.from_standards_dict = material_gas.from_standards_dict
OpaqueConstruction.from_standards_dict = construction_opaque.from_standards_dict
WindowConstruction.from_standards_dict = window_opaque.from_standards_dict
ConstructionSet.from_standards_dict = constructionset.from_standards_dict
ScheduleDay.from_standards_dict = schedule_day.from_standards_dict
ScheduleRuleset.from_standards_dict = schedule_ruleset.from_standards_dict
ProgramType.from_standards_dict = programtype.from_standards_dict


# extend the 'object_by_name' methods within the honeybee_energy.lib
materials.opaque_material_by_name = material_lib.opaque_material_by_name
materials.window_material_by_name = material_lib.window_material_by_name
constructions.opaque_construction_by_name = construction_lib.opaque_construction_by_name
constructions.window_construction_by_name = construction_lib.window_construction_by_name
constructionsets.construction_set_by_name = construction_set_lib.construction_set_by_name
schedules.schedule_by_name = schedule_lib.schedule_by_name
programtypes.program_type_by_name = program_type_lib.program_type_by_name


# overwrite the list of all available objects within honeybee_energy.lib
materials.OPAQUE_MATERIALS = materials.OPAQUE_MATERIALS + \
    tuple(material_lib._opaque_standards_dict.keys())
materials.WINDOW_MATERIALS = materials.WINDOW_MATERIALS + \
    tuple(material_lib._window_standards_dict.keys())
constructions.OPAQUE_CONSTRUCTIONS = constructions.OPAQUE_CONSTRUCTIONS + \
    tuple(construction_lib._opaque_constr_standards_dict.keys())
constructions.WINDOW_CONSTRUCTIONS = constructions.WINDOW_CONSTRUCTIONS + \
    tuple(construction_lib._window_constr_standards_dict.keys())
constructionsets.CONSTRUCTION_SETS = constructionsets.CONSTRUCTION_SETS + \
    tuple(construction_set_lib._construction_set_standards_dict.keys())
schedules.SCHEDULES = schedules.SCHEDULES + \
    tuple(schedule_lib._schedule_standards_dict.keys())
programtypes.PROGRAM_TYPES = programtypes.PROGRAM_TYPES + \
    tuple(program_type_lib._program_type_standards_dict.keys())
