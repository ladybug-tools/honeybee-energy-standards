"""Classmethod for honeybee-energy opaque construction."""
from ..lib.materials import opaque_material_by_name


@classmethod
def from_standards_dict(cls, data):
    """Create an OpaqueConstruction from an OpenStudio standards gem dictionary.

    Args:
        data: An OpenStudio standards dictionary of an opaque construction in the
            format below.

        .. code-block:: json

            {
            "name": "Typical Insulated Exterior Mass Wall",
            "intended_surface_type": "ExteriorWall",
            "standards_construction_type": "Mass",
            "insulation_layer": "Typical Insulation",
            "materials": [
                "1IN Stucco",
                "8IN CONCRETE HW RefBldg",
                "Typical Insulation",
                "1/2IN Gypsum"]
            }
    """
    materials = tuple(opaque_material_by_name(mat) for mat in data['materials'])
    return cls(data['name'], materials)
