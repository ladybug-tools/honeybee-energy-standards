"""Classmethod for honeybee-energy window construction."""
import honeybee_energy.lib.materials as mat_lib


def from_standards_dict(cls, data):
    """Create a WindowConstruction from an OpenStudio standards gem dictionary.

    Args:
        data: An OpenStudio standards dictionary of a window construction in the
            format below.

    .. code-block:: json

        {
        "name": "ASHRAE 189.1-2009 ExtWindow ClimateZone 4-5",
        "intended_surface_type": "ExteriorWindow",
        "materials": ["Theoretical Glass [207]"]
        }
    """
    materials = tuple(mat_lib.window_material_by_identifier(mat)
                      for mat in data['materials'])
    return cls(data['name'], materials)
