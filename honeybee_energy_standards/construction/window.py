"""Classmethod for honeybee-energy window construction."""
from ..lib.materials import window_material_by_name


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
    materials = tuple(window_material_by_name(mat) for mat in data['materials'])
    return cls(data['name'], materials)
