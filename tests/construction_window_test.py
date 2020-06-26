# coding=utf-8
from honeybee_energy.construction.window import WindowConstruction
import honeybee_energy.lib.constructions as constr_lib

import pytest


def test_construction_lib():
    """Test that the honeybee-energy lib has been extended with new construction data."""
    assert len(constr_lib.WINDOW_CONSTRUCTIONS) > 2  # should now have many more constructions

    constr_from_lib = constr_lib.window_construction_by_identifier(constr_lib.WINDOW_CONSTRUCTIONS[0])
    assert isinstance(constr_from_lib, WindowConstruction)

    constr_from_lib = constr_lib.window_construction_by_identifier(constr_lib.WINDOW_CONSTRUCTIONS[2])
    assert isinstance(constr_from_lib, WindowConstruction)


def test_opaque_material_by_identifier():
    """Test that all of the constructions in the library can be loaded by identifier."""
    for constr in constr_lib.WINDOW_CONSTRUCTIONS:
        constr_from_lib = constr_lib.window_construction_by_identifier(constr)
        assert isinstance(constr_from_lib, WindowConstruction)
