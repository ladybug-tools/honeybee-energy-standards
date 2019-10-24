# coding=utf-8
from honeybee_energy.construction.window import WindowConstruction
import honeybee_energy.lib.constructions as constr_lib

import pytest


def test_window_to_from_standards_dict():
    """Test the initialization of OpaqueConstruction objects from standards gem."""
    standards_dict = {
        "name": "U 0.19 SHGC 0.20 Trp LoE Film (55) Bronze 6mm/13mm Air",
        "intended_surface_type": "ExteriorWindow",
        "materials": [
            "BRONZE 6MM",
            "AIR 13MM",
            "COATED POLY-55",
            "AIR 13MM",
            "CLEAR 3MM"]}
    glaz_constr = WindowConstruction.from_standards_dict(standards_dict)

    assert glaz_constr.name == 'U 0.19 SHGC 0.20 Trp LoE Film (55) Bronze 6mm/13mm Air'
    assert glaz_constr.r_value == pytest.approx(0.645449, rel=1e-2)
    assert glaz_constr.u_value == pytest.approx(1.549307, rel=1e-2)
    assert glaz_constr.u_factor == pytest.approx(1.2237779, rel=1e-2)
    assert glaz_constr.r_factor == pytest.approx(0.817141, rel=1e-2)


def test_construction_lib():
    """Test that the honeybee-energy lib has been extended with new construction data."""
    assert len(constr_lib.WINDOW_CONSTRUCTIONS) > 2  # should now have many more constructions

    constr_from_lib = constr_lib.window_construction_by_name(constr_lib.WINDOW_CONSTRUCTIONS[0])
    assert isinstance(constr_from_lib, WindowConstruction)

    constr_from_lib = constr_lib.window_construction_by_name(constr_lib.WINDOW_CONSTRUCTIONS[2])
    assert isinstance(constr_from_lib, WindowConstruction)


def test_opaque_material_by_name():
    """Test that all of the constructions in the library can be loaded by name."""
    for constr in constr_lib.WINDOW_CONSTRUCTIONS:
        constr_from_lib = constr_lib.window_construction_by_name(constr)
        assert isinstance(constr_from_lib, WindowConstruction)
