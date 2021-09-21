# coding=utf-8
from honeybee_energy.material.glazing import EnergyWindowMaterialGlazing, \
    EnergyWindowMaterialSimpleGlazSys
from honeybee_energy.material.gas import EnergyWindowMaterialGas, \
    EnergyWindowMaterialGasMixture
import honeybee_energy.lib.materials as mat_lib

import pytest


def test_material_lib():
    """Test that the honeybee-energy lib has been extended with new material data."""
    possible_types = (EnergyWindowMaterialGlazing, EnergyWindowMaterialSimpleGlazSys,
                      EnergyWindowMaterialGas, EnergyWindowMaterialGasMixture)

    assert len(mat_lib.WINDOW_MATERIALS) > 4  # should now have many more materials

    mat_from_lib = mat_lib.window_material_by_identifier(mat_lib.WINDOW_MATERIALS[0])
    assert isinstance(mat_from_lib, possible_types)

    mat_from_lib = mat_lib.window_material_by_identifier(mat_lib.WINDOW_MATERIALS[4])
    assert isinstance(mat_from_lib, possible_types)


def test_window_material_by_identifier():
    """Test that all of the materials in the library can be loaded by identifier."""
    possible_types = (EnergyWindowMaterialGlazing, EnergyWindowMaterialSimpleGlazSys,
                      EnergyWindowMaterialGas, EnergyWindowMaterialGasMixture)

    for mat in mat_lib.WINDOW_MATERIALS:
        mat_from_lib = mat_lib.window_material_by_identifier(mat)
        assert isinstance(mat_from_lib, possible_types)
