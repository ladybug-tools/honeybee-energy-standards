"""Classmethods for honeybee-energy glazing materials."""


@classmethod
def from_standards_dict(cls, data):
    """Create EnergyWindowMaterialGlazing from OpenStudio standards gem dictionary.

    Args:
        data: An OpenStudio standards dictionary of a glazing material in the
            format below.

        .. code-block:: python

            {
            "name": 'Blue 6mm',
            "material_type": "StandardGlazing",
            "thickness": 0.2362204,
            "solar_transmittance": 0.45,
            "solar_reflectance": 0.36,
            "visible_transmittance": 0.714,
            "visible_reflectance": 0.207,
            "infrared_transmittance": 0,
            "emissivity": 0.84,
            "emissivity_back": 0.0466,
            "conductivity": 6.24012
            }
    """
    assert data['material_type'] == 'StandardGlazing', \
        'Expected StandardGlazing. Got {}.'.format(data['material_type'])
    assert data['optical_data_type'] == 'SpectralAverage', \
        'Expected SpectralAverage. Got {}.'.format(data['optical_data_type'])
    thickness = 0.0254 * data['thickness']  # convert from inches
    conductivity = data['conductivity'] / 6.9381117  # convert from Btu*in/hr*ft2*F
    solar_diff = False if data['solar_diffusing'] == 0 else True
    new_mat = cls(data['name'], thickness,
                  data['solar_transmittance_at_normal_incidence'],
                  data['front_side_solar_reflectance_at_normal_incidence'],
                  data['visible_transmittance_at_normal_incidence'],
                  data['front_side_visible_reflectance_at_normal_incidence'],
                  data['infrared_transmittance_at_normal_incidence'],
                  data['front_side_infrared_hemispherical_emissivity'],
                  data['back_side_infrared_hemispherical_emissivity'],
                  conductivity)
    new_mat.solar_reflectance_back = \
        data['back_side_solar_reflectance_at_normal_incidence']
    new_mat.visible_reflectance_back = \
        data['back_side_visible_reflectance_at_normal_incidence']
    new_mat.dirt_correction = \
        data['dirt_correction_factor_for_solar_and_visible_transmittance']
    new_mat.solar_diffusing = solar_diff
    return new_mat


@classmethod
def simple_from_standards_dict(cls, data):
    """Create EnergyWindowMaterialSimpleGlazSys from OpenStudio standards dictionary.

    Args:
        data: {
            "name": 'Fixed Window',
            "material_type": "SimpleGlazing",
            "u_factor": 0.45,
            "solar_heat_gain_coefficient": 0.45,
            "visible_transmittance": 0.35}
    """
    assert data['material_type'] == 'SimpleGlazing', \
        'Expected SimpleGlazing. Got {}.'.format(data['material_type'])
    u_factor = data['u_factor'] * 5.678  # convert from Btu/hr*ft2*F
    return cls(data['name'], u_factor, data['solar_heat_gain_coefficient'],
               data['visible_transmittance'])
