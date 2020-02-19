# coding=utf-8
"""Change the honeybee-energy lib to load from the _standards_data folder."""
# import all of the objects that are being extended from honyebee-energy
import honeybee_energy_standards._lib.materials as material_lib
import honeybee_energy_standards._lib.constructions as construction_lib
import honeybee_energy_standards._lib.constructionsets as construction_set_lib
import honeybee_energy_standards._lib.schedules as schedule_lib
import honeybee_energy_standards._lib.programtypes as program_type_lib

from honeybee_energy.lib import materials
from honeybee_energy.lib import constructions
from honeybee_energy.lib import constructionsets
from honeybee_energy.lib import schedules
from honeybee_energy.lib import programtypes


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