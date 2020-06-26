# coding=utf-8
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass
import honeybee_energy.lib.materials as mat_lib

import pytest


def test_material_lib():
    """Test that the honeybee-energy lib has been extended with new material data."""
    possible_types = (EnergyMaterial, EnergyMaterialNoMass)

    assert len(mat_lib.OPAQUE_MATERIALS) > 13  # should now have many more materials

    mat_from_lib = mat_lib.opaque_material_by_identifier(mat_lib.OPAQUE_MATERIALS[0])
    assert isinstance(mat_from_lib, possible_types)

    mat_from_lib = mat_lib.opaque_material_by_identifier(mat_lib.OPAQUE_MATERIALS[13])
    assert isinstance(mat_from_lib, possible_types)


def test_opaque_material_by_identifier():
    """Test that all of the materials in the library can be loaded by identifier."""
    possible_types = (EnergyMaterial, EnergyMaterialNoMass)

    for mat in mat_lib.OPAQUE_MATERIALS:
        mat_from_lib = mat_lib.opaque_material_by_identifier(mat)
        assert isinstance(mat_from_lib, possible_types)
