# coding=utf-8
from honeybee_energy.material.glazing import EnergyWindowMaterialGlazing, \
    EnergyWindowMaterialSimpleGlazSys
from honeybee_energy.material.gas import EnergyWindowMaterialGas
import honeybee_energy.lib.materials as mat_lib

import pytest


def test_glazing_to_from_standards_dict():
    """Test the initialization of EnergyMaterial objects from standards gem."""
    standards_dict = {
        "name": "PYR B CLEAR 3MM",
        "material_type": "StandardGlazing",
        "thickness": 0.118110236220472,
        "conductivity": 6.24012461866438,
        "resistance": 0.160253209849202,
        "optical_data_type": "SpectralAverage",
        "solar_transmittance_at_normal_incidence": 0.74,
        "front_side_solar_reflectance_at_normal_incidence": 0.09,
        "back_side_solar_reflectance_at_normal_incidence": 0.1,
        "visible_transmittance_at_normal_incidence": 0.82,
        "front_side_visible_reflectance_at_normal_incidence": 0.11,
        "back_side_visible_reflectance_at_normal_incidence": 0.12,
        "infrared_transmittance_at_normal_incidence": 0.0,
        "front_side_infrared_hemispherical_emissivity": 0.84,
        "back_side_infrared_hemispherical_emissivity": 0.2,
        "dirt_correction_factor_for_solar_and_visible_transmittance": 1.0,
        "solar_diffusing": 0}
    mat_1 = EnergyWindowMaterialGlazing.from_standards_dict(standards_dict)

    assert mat_1.name == 'PYR B CLEAR 3MM'
    assert mat_1.thickness == pytest.approx(0.003, rel=1e-3)
    assert mat_1.conductivity == pytest.approx(0.9, rel=1e-2)


def test_simple_sys_to_from_standards_dict():
    """Test the initialization of EnergyMaterial objects from standards gem."""
    standards_dict = {
        "name": "U 0.52 SHGC 0.39 Simple Glazing",
        "material_type": "SimpleGlazing",
        "u_factor": 0.52,
        "solar_heat_gain_coefficient": 0.39,
        "visible_transmittance": 0.31}
    mat_1 = EnergyWindowMaterialSimpleGlazSys.from_standards_dict(standards_dict)

    assert mat_1.name == 'U 0.52 SHGC 0.39 Simple Glazing'
    assert mat_1.u_factor == pytest.approx(0.52 * 5.678, rel=1e-3)
    assert mat_1.shgc == pytest.approx(0.39, rel=1e-2)
    assert mat_1.vt == pytest.approx(0.31, rel=1e-2)


def test_gas_to_from_standards_dict():
    """Test initialization of EnergyWindowMaterialGas objects from standards gem."""
    standards_dict = {
        "name": "AIR 13MM",
        "material_type": "Gas",
        "thickness": 0.5,
        "gas_type": "Air"}
    mat_1 = EnergyWindowMaterialGas.from_standards_dict(standards_dict)

    assert mat_1.name == 'AIR 13MM'
    assert mat_1.thickness == pytest.approx(0.0127, rel=1e-2)
    assert mat_1.gas_type == 'Air'


def test_material_lib():
    """Test that the honeybee-energy lib has been extended with new material data."""
    possible_types = (EnergyWindowMaterialGlazing, EnergyWindowMaterialSimpleGlazSys,
                      EnergyWindowMaterialGas)

    assert len(mat_lib.WINDOW_MATERIALS) > 4  # should now have many more materials

    mat_from_lib = mat_lib.window_material_by_name(mat_lib.WINDOW_MATERIALS[0])
    assert isinstance(mat_from_lib, possible_types)

    mat_from_lib = mat_lib.window_material_by_name(mat_lib.WINDOW_MATERIALS[4])
    assert isinstance(mat_from_lib, possible_types)


def test_window_material_by_name():
    """Test that all of the materials in the library can be loaded by name."""
    possible_types = (EnergyWindowMaterialGlazing, EnergyWindowMaterialSimpleGlazSys,
                      EnergyWindowMaterialGas)

    for mat in mat_lib.WINDOW_MATERIALS:
        mat_from_lib = mat_lib.window_material_by_name(mat)
        assert isinstance(mat_from_lib, possible_types)
