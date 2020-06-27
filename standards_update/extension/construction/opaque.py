"""Classmethod for honeybee-energy opaque construction."""
import honeybee_energy.lib.materials as mat_lib


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
    materials = tuple(mat_lib.opaque_material_by_identifier(mat)
                      for mat in data['materials'])
    return cls(data['name'], materials)
