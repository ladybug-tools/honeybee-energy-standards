# coding=utf-8
from honeybee_energy.constructionset import ConstructionSet
import honeybee_energy.lib.constructionsets as constr_set_lib


def test_construction_set_from_standards_dict():
    """Test the from_standards_dict method."""
    constr_set_dict = \
        {
            "name": "2013::ClimateZone5::SteelFramed",
            "wall_set": {
                "exterior_construction": "Typical Insulated Steel Framed Exterior Wall-R19",
                "ground_construction": "Typical Insulated Basement Mass Wall-R8"
            },
            "floor_set": {
                "exterior_construction": "Typical Insulated Steel Framed Exterior Floor-R27",
                "ground_construction": "Typical Insulated Carpeted 8in Slab Floor-R5"
            },
            "roof_ceiling_set": {
                "exterior_construction": "Typical IEAD Roof-R32"
            },
            "aperture_set": {
                "window_construction": "U 0.48 SHGC 0.40 Dbl Ref-D Clr 6mm/13mm",
                "operable_construction": "U 0.48 SHGC 0.40 Dbl Ref-D Clr 6mm/13mm",
                "skylight_construction": "Window_U_0.50_SHGC_0.40_Skylight_Frame_Width_0.430_in"
            },
            "door_set": {
                "exterior_construction": "Typical Insulated Metal Door-R2",
                "overhead_construction": "Typical Overhead Door-R2",
                "exterior_glass_construction": "U 0.44 SHGC 0.26 Dbl Ref-B-H Clr 6mm/13mm Air"
            }
        }
    cz5_constr_set = ConstructionSet.from_standards_dict(constr_set_dict)

    assert cz5_constr_set.wall_set.exterior_construction.name == \
        'Typical Insulated Steel Framed Exterior Wall-R19'
    assert cz5_constr_set.wall_set.ground_construction.name == \
        'Typical Insulated Basement Mass Wall-R8'
    assert cz5_constr_set.floor_set.exterior_construction.name == \
        'Typical Insulated Steel Framed Exterior Floor-R27'
    assert cz5_constr_set.floor_set.ground_construction.name == \
        'Typical Insulated Carpeted 8in Slab Floor-R5'
    assert cz5_constr_set.roof_ceiling_set.exterior_construction.name == \
        'Typical IEAD Roof-R32'
    assert cz5_constr_set.door_set.exterior_construction.name == \
        'Typical Insulated Metal Door-R2'
    assert cz5_constr_set.door_set.overhead_construction.name == \
        'Typical Overhead Door-R2'

    assert cz5_constr_set.aperture_set.window_construction.name == \
        'U 0.48 SHGC 0.40 Dbl Ref-D Clr 6mm/13mm'
    assert cz5_constr_set.aperture_set.operable_construction.name == \
        'U 0.48 SHGC 0.40 Dbl Ref-D Clr 6mm/13mm'
    assert cz5_constr_set.aperture_set.skylight_construction.name == \
        'Window_U_0.50_SHGC_0.40_Skylight_Frame_Width_0.430_in'
    assert cz5_constr_set.door_set.exterior_glass_construction.name == \
        'U 0.44 SHGC 0.26 Dbl Ref-B-H Clr 6mm/13mm Air'


def test_construction_set_lib():
    """Test that the honeybee-energy lib has been extended with new counstruction set data."""
    assert len(constr_set_lib.CONSTRUCTION_SETS) > 2  # should now have many more construction sets

    cset_from_lib = constr_set_lib.construction_set_by_name(constr_set_lib.CONSTRUCTION_SETS[0])
    assert isinstance(cset_from_lib, ConstructionSet)

    cset_from_lib = constr_set_lib.construction_set_by_name(constr_set_lib.CONSTRUCTION_SETS[2])
    assert isinstance(cset_from_lib, ConstructionSet)


def test_construction_set_by_name():
    """Test that all of the construction sets in the library can be loaded by name."""
    for c_set in constr_set_lib.CONSTRUCTION_SETS:
        cset_from_lib = constr_set_lib.construction_set_by_name(c_set)
        assert isinstance(cset_from_lib, ConstructionSet)
