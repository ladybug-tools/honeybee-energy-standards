"""Classmethod for honeybee-energy construction set."""
from __future__ import division

import honeybee_energy.lib.constructions as con_lib


def from_standards_dict(cls, data):
    """Create a ConstructionSet from an OpenStudio standards gem dictionary.

    Args:
        data: An OpenStudio standards dictionary of a construction type in the
            format below.

    .. code-block:: python

        {
        "name": "2013::ClimateZone5::SteelFramed",
        "wall_set": {
            "exterior_construction": "Typical Insulated Steel Framed Exterior Wall-R19",
            "ground_construction": "Typical Insulated Basement Mass Wall-R8"
        },
        "floor_set": {
            "exterior_construction": "Typical Insulated Steel Framed Exterior Floor-R27",
            "ground_construction": "Typical Insulated Carpeted 8in Slab Floor-R5"
        },
        "roof_ceiling_set": {
            "exterior_construction": "Typical IEAD Roof-R32"
        },
        "aperture_set": {
            "window_construction": "U 0.48 SHGC 0.40 Dbl Ref-D Clr 6mm/13mm",
            "operable_construction": "U 0.48 SHGC 0.40 Dbl Ref-D Clr 6mm/13mm",
            "skylight_construction": "Window_U_0.50_SHGC_0.40_Skylight_Frame_Width_0.430_in"
        },
        "door_set": {
            "exterior_construction": "Typical Insulated Metal Door-R2",
            "overhead_construction": "Typical Overhead Door-R2",
            "exterior_glass_construction": "U 0.44 SHGC 0.26 Dbl Ref-B-H Clr 6mm/13mm Air"
        }
    """
    # initialize a blank construction set
    construction_set = cls(data['name'])

    # assign all of the opaque constructions
    construction_set.wall_set.exterior_construction = \
        con_lib.opaque_construction_by_identifier(data['wall_set']['exterior_construction'])
    construction_set.wall_set.ground_construction = \
        con_lib.opaque_construction_by_identifier(data['wall_set']['ground_construction'])
    construction_set.floor_set.exterior_construction = \
        con_lib.opaque_construction_by_identifier(data['floor_set']['exterior_construction'])
    construction_set.floor_set.ground_construction = \
        con_lib.opaque_construction_by_identifier(data['floor_set']['ground_construction'])
    construction_set.roof_ceiling_set.exterior_construction = \
        con_lib.opaque_construction_by_identifier(data['roof_ceiling_set']['exterior_construction'])
    construction_set.door_set.exterior_construction = \
        con_lib.opaque_construction_by_identifier(data['door_set']['exterior_construction'])
    construction_set.door_set.overhead_construction = \
        con_lib.opaque_construction_by_identifier(data['door_set']['overhead_construction'])

    # assign all of the window constructions
    construction_set.aperture_set.window_construction = \
        con_lib.window_construction_by_identifier(data['aperture_set']['window_construction'])
    construction_set.aperture_set.operable_construction = \
        con_lib.window_construction_by_identifier(data['aperture_set']['operable_construction'])
    construction_set.aperture_set.skylight_construction = \
        con_lib.window_construction_by_identifier(data['aperture_set']['skylight_construction'])
    construction_set.door_set.exterior_glass_construction = \
        con_lib.window_construction_by_identifier(data['door_set']['exterior_glass_construction'])

    return construction_set
