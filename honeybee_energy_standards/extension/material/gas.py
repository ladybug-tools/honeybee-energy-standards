"""Classmethods for honeybee-energy gas materials."""


def from_standards_dict(cls, data):
    """Create EnergyWindowMaterialGas from OpenStudio standards dictionary.

    Args:
        data: An OpenStudio standards dictionary of a gas material in the
            format below.

    .. code-block:: python

        {
        "name": 'Gap_1_W_0_0018',
        "material_type": "Gas",
        "thickness": 0.070866,
        "gas_type": "Air"
        }
    """
    assert data['material_type'] == 'Gas', \
        'Expected Gas. Got {}.'.format(data['material_type'])
    thickness = 0.0254 * data['thickness']  # convert from inches
    return cls(data['name'], thickness, data['gas_type'])
