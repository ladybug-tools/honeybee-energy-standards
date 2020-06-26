# coding=utf-8
"""Extend honeybee-energy objects with the classmethods of this library."""

# import all of the objects that are being extended from honeybee-energy
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


# import all of the extension methods from this library
import standards_update.extension.material.opaque as material_opaque
import standards_update.extension.material.glazing as material_glazing
import standards_update.extension.material.gas as material_gas
import standards_update.extension.construction.opaque as construction_opaque
import standards_update.extension.construction.window as window_opaque
import standards_update.extension.constructionset as constructionset
import standards_update.extension.schedule.day as schedule_day
import standards_update.extension.schedule.ruleset as schedule_ruleset
import standards_update.extension.programtype as programtype


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
