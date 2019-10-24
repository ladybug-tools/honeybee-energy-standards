# coding=utf-8
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass
import honeybee_energy.lib.materials as mat_lib

import pytest


def test_material_to_from_standards_dict():
    """Test the initialization of EnergyMaterial objects from standards gem."""
    standards_dict = {
        "name": "Extruded Polystyrene - XPS - 6 in. R30.00",
        "material_type": "StandardOpaqueMaterial",
        "roughness": "MediumSmooth",
        "thickness": 6.0,
        "conductivity": 0.20,
        "resistance": 29.9999994,
        "density": 1.3,
        "specific_heat": 0.35,
        "thermal_absorptance": None,
        "solar_absorptance": None,
        "visible_absorptance": None}
    mat_1 = EnergyMaterial.from_standards_dict(standards_dict)

    assert mat_1.name == 'Extruded Polystyrene - XPS - 6 in. R30.00'
    assert mat_1.thickness == pytest.approx(0.1524, rel=1e-3)
    assert mat_1.conductivity == pytest.approx(0.028826, rel=1e-3)
    assert mat_1.density == pytest.approx(20.82, rel=1e-3)
    assert mat_1.specific_heat == pytest.approx(1464.435, rel=1e-3)
    assert mat_1.roughness == 'MediumSmooth'
    assert mat_1.resistivity == pytest.approx(1 / 0.028826, rel=1e-3)


def test_material_nomass_to_from_standards_dict():
    """Test the initialization of EnergyMaterialNoMass objects from standards gem."""
    standards_dict = {
        "name": "MAT-SHEATH",
        "material_type": "MasslessOpaqueMaterial",
        "roughness": None,
        "thickness": None,
        "conductivity": 6.24012461866438,
        "resistance": 0.160253209849203,
        "density": 0.0436995724033012,
        "specific_heat": 0.000167192127639247,
        "thermal_absorptance": 0.9,
        "solar_absorptance": 0.7,
        "visible_absorptance": 0.7}
    mat_1 = EnergyMaterialNoMass.from_standards_dict(standards_dict)

    assert mat_1.name == 'MAT-SHEATH'
    assert mat_1.roughness == 'MediumRough'
    assert mat_1.r_value == pytest.approx(0.1602532098 / 5.678, rel=1e-2)
    assert mat_1.thermal_absorptance == 0.9
    assert mat_1.solar_absorptance == 0.7
    assert mat_1.visible_absorptance == 0.7


def test_material_lib():
    """Test that the honeybee-energy lib has been extended with new material data."""
    possible_types = (EnergyMaterial, EnergyMaterialNoMass)

    assert len(mat_lib.OPAQUE_MATERIALS) > 13  # should now have many more materials

    mat_from_lib = mat_lib.opaque_material_by_name(mat_lib.OPAQUE_MATERIALS[0])
    assert isinstance(mat_from_lib, possible_types)

    mat_from_lib = mat_lib.opaque_material_by_name(mat_lib.OPAQUE_MATERIALS[13])
    assert isinstance(mat_from_lib, possible_types)


def test_opaque_material_by_name():
    """Test that all of the materials in the library can be loaded by name."""
    possible_types = (EnergyMaterial, EnergyMaterialNoMass)

    for mat in mat_lib.OPAQUE_MATERIALS:
        mat_from_lib = mat_lib.opaque_material_by_name(mat)
        assert isinstance(mat_from_lib, possible_types)
