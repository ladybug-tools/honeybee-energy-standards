"""Classmethods for honeybee-energy opaque materials."""


@classmethod
def from_standards_dict(cls, data):
    """Create a EnergyMaterial from an OpenStudio standards gem dictionary.

    Args:
        data: An OpenStudio standards dictionary of a opaque material in the
            format below.

        .. code-block:: python

            {
            "name": "G01 13mm gypsum board",
            "material_type": "StandardOpaqueMaterial",
            "roughness": "Smooth",
            "thickness": 0.5,
            "conductivity": 1.10957,
            "density": 49.9424,
            "specific_heat": 0.260516252,
            "thermal_absorptance": 0.9,
            "solar_absorptance": 0.7,
            "visible_absorptance": 0.5
            }
    """
    assert data['material_type'] == 'StandardOpaqueMaterial', \
        'Expected StandardOpaqueMaterial. Got {}.'.format(data['material_type'])
    thickness = 0.0254 * data['thickness']  # convert from inches
    conductivity = data['conductivity'] / 6.9381117  # convert from Btu*in/hr*ft2*F
    density = data['density'] * 16.0185  # convert from lb/ft3
    specific_heat = data['specific_heat'] / 0.000239  # convert from Btu/lb*F

    optional_keys = ('roughness', 'thermal_absorptance', 'solar_absorptance',
                     'visible_absorptance')
    optional_vals = ('MediumRough', 0.9, 0.7, 0.7)
    for key, val in zip(optional_keys, optional_vals):
        if key not in data or data[key] is None:
            data[key] = val

    return cls(data['name'], thickness, conductivity,
               density, specific_heat, data['roughness'],
               data['thermal_absorptance'], data['solar_absorptance'],
               data['visible_absorptance'])


@classmethod
def no_mass_from_standards_dict(cls, data):
    """Create a EnergyMaterialNoMass from an OpenStudio standards gem dictionary.

    Args:
        data: {
            "name": "CP02 CARPET PAD",
            "material_type": "MasslessOpaqueMaterial",
            "roughness": "Smooth",
            "resistance": 0.160253201,
            "thermal_absorptance": 0.9,
            "solar_absorptance": 0.8,
            "visible_absorptance": 0.8}
    """
    assert data['material_type'] in ('MasslessOpaqueMaterial', 'AirGap'), \
        'Expected MasslessOpaqueMaterial. Got {}.'.format(data['material_type'])
    optional_keys = ('roughness', 'thermal_absorptance', 'solar_absorptance',
                     'visible_absorptance')
    optional_vals = ('MediumRough', 0.9, 0.7, 0.7)
    for key, val in zip(optional_keys, optional_vals):
        if key not in data or data[key] is None:
            data[key] = val
    r_value = data['resistance'] / 5.678263337  # convert from hr*ft2*F/Btu
    return cls(data['name'], r_value, data['roughness'],
               data['thermal_absorptance'], data['solar_absorptance'],
               data['visible_absorptance'])
