# coding=utf-8
from honeybee_energy.construction.opaque import OpaqueConstruction
import honeybee_energy.lib.constructions as constr_lib

import pytest


def test_opaque_to_from_standards_dict():
    """Test the initialization of OpaqueConstruction objects from standards gem."""
    standards_dict = {
        "name": "Typical Insulated Exterior Mass Wall",
        "intended_surface_type": "ExteriorWall",
        "materials": [
            "1IN Stucco",
            "8IN CONCRETE HW RefBldg",
            "Typical Insulation",
            "1/2IN Gypsum"]}
    wall_constr = OpaqueConstruction.from_standards_dict(standards_dict)

    assert wall_constr.name == 'Typical Insulated Exterior Mass Wall'
    assert wall_constr.r_value == pytest.approx(0.29934598728, rel=1e-3)
    assert wall_constr.u_value == pytest.approx(3.3406160178, rel=1e-3)
    assert wall_constr.u_factor == pytest.approx(2.159364735, rel=1e-3)
    assert wall_constr.r_factor == pytest.approx(0.463099162, rel=1e-3)


def test_construction_lib():
    """Test that the honeybee-energy lib has been extended with new construction data."""
    assert len(constr_lib.OPAQUE_CONSTRUCTIONS) > 12  # should now have many more constructions

    constr_from_lib = constr_lib.opaque_construction_by_name(constr_lib.OPAQUE_CONSTRUCTIONS[0])
    assert isinstance(constr_from_lib, OpaqueConstruction)

    constr_from_lib = constr_lib.opaque_construction_by_name(constr_lib.OPAQUE_CONSTRUCTIONS[12])
    assert isinstance(constr_from_lib, OpaqueConstruction)


def test_opaque_material_by_name():
    """Test that all of the constructions in the library can be loaded by name."""
    for constr in constr_lib.OPAQUE_CONSTRUCTIONS:
        constr_from_lib = constr_lib.opaque_construction_by_name(constr)
        assert isinstance(constr_from_lib, OpaqueConstruction)
