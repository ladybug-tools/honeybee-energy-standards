# coding=utf-8
"""Extend honeybee-energy objects with the classmethods of this library."""
import os
import json

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

import honeybee_energy.lib.programtypes as hb_programtypes


# import all of the extension methods from this library
import honeybee_energy_standards.extension.material.opaque as material_opaque
import honeybee_energy_standards.extension.material.glazing as material_glazing
import honeybee_energy_standards.extension.material.gas as material_gas
import honeybee_energy_standards.extension.construction.opaque as construction_opaque
import honeybee_energy_standards.extension.construction.window as window_opaque
import honeybee_energy_standards.extension.constructionset as constructionset
import honeybee_energy_standards.extension.schedule.day as schedule_day
import honeybee_energy_standards.extension.schedule.ruleset as schedule_ruleset
import honeybee_energy_standards.extension.programtype as programtype


# add classmethods to create honeybee-energy objects from standards gem dictionaries
EnergyMaterial.from_standards_dict = \
    classmethod(material_opaque.from_standards_dict)
EnergyMaterialNoMass.from_standards_dict = \
    classmethod(material_opaque.no_mass_from_standards_dict)
EnergyWindowMaterialGlazing.from_standards_dict = \
    classmethod(material_glazing.from_standards_dict)
EnergyWindowMaterialSimpleGlazSys.from_standards_dict = \
    classmethod(material_glazing.simple_from_standards_dict)
EnergyWindowMaterialGas.from_standards_dict = \
    classmethod(material_gas.from_standards_dict)
OpaqueConstruction.from_standards_dict = \
    classmethod(construction_opaque.from_standards_dict)
WindowConstruction.from_standards_dict = \
    classmethod(window_opaque.from_standards_dict)
ConstructionSet.from_standards_dict = \
    classmethod(constructionset.from_standards_dict)
ScheduleDay.from_standards_dict = \
    classmethod(schedule_day.from_standards_dict)
ScheduleRuleset.from_standards_dict = \
    classmethod(schedule_ruleset.from_standards_dict)
ProgramType.from_standards_dict = \
    classmethod(programtype.from_standards_dict)


# add a variable to the program type library to help easily look up ProgramTypes
STANDARDS_REGISTRY = {}
_vintages = ('2013', '2010', '2007', '2004', '1980_2004', 'pre_1980')
_prog_dir = os.path.join(os.path.dirname(__file__), 'data', 'programtypes_registry')
for vintage in _vintages:
    _prog_vintage_dir = os.path.join(_prog_dir, '{}_registry.json'.format(vintage))
    try:
        with open(_prog_vintage_dir, 'r') as f:
            STANDARDS_REGISTRY[vintage] = json.load(f)
    except FileNotFoundError:
        pass
setattr(hb_programtypes, 'STANDARDS_REGISTRY', STANDARDS_REGISTRY)
