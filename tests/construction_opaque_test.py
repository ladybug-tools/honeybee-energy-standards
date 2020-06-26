# coding=utf-8
from honeybee_energy.construction.opaque import OpaqueConstruction
from honeybee_energy.construction.air import AirBoundaryConstruction
import honeybee_energy.lib.constructions as constr_lib

import pytest


def test_construction_lib():
    """Test that the honeybee-energy lib has been extended with new construction data."""
    assert len(constr_lib.OPAQUE_CONSTRUCTIONS) > 12  # should now have many more constructions

    constr_from_lib = constr_lib.opaque_construction_by_identifier(
        constr_lib.OPAQUE_CONSTRUCTIONS[0])
    assert isinstance(constr_from_lib, OpaqueConstruction)

    constr_from_lib = constr_lib.opaque_construction_by_identifier(
        constr_lib.OPAQUE_CONSTRUCTIONS[12])
    assert isinstance(constr_from_lib, OpaqueConstruction)


def test_opaque_material_by_identifier():
    """Test that all of the constructions in the library can be loaded by identifier."""
    for constr in constr_lib.OPAQUE_CONSTRUCTIONS:
        constr_from_lib = constr_lib.opaque_construction_by_identifier(constr)
        assert isinstance(constr_from_lib, (OpaqueConstruction, AirBoundaryConstruction))
