# coding=utf-8
"""Change the honeybee-energy lib to load from the _standards_data folder."""
# import all of the objects that are being extended from honeybee-energy
import standards_update._lib.materials as material_lib
import standards_update._lib.constructions as construction_lib
import standards_update._lib.constructionsets as construction_set_lib
import standards_update._lib.schedules as schedule_lib
import standards_update._lib.programtypes as program_type_lib

from honeybee_energy.lib import materials
from honeybee_energy.lib import constructions
from honeybee_energy.lib import constructionsets
from honeybee_energy.lib import schedules
from honeybee_energy.lib import programtypes


# extend the 'object_by_identifier' methods within the honeybee_energy.lib
materials.opaque_material_by_identifier = \
    material_lib.opaque_material_by_identifier
materials.window_material_by_identifier = \
    material_lib.window_material_by_identifier
constructions.opaque_construction_by_identifier = \
    construction_lib.opaque_construction_by_identifier
constructions.window_construction_by_identifier = \
    construction_lib.window_construction_by_identifier
constructionsets.construction_set_by_identifier = \
    construction_set_lib.construction_set_by_identifier
schedules.schedule_by_identifier = \
    schedule_lib.schedule_by_identifier
programtypes.program_type_by_identifier = \
    program_type_lib.program_type_by_identifier


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