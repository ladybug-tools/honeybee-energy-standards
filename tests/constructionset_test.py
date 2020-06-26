# coding=utf-8
from honeybee_energy.constructionset import ConstructionSet
import honeybee_energy.lib.constructionsets as constr_set_lib


def test_construction_set_lib():
    """Test that the honeybee-energy lib has been extended with new counstruction set data."""
    assert len(constr_set_lib.CONSTRUCTION_SETS) > 2  # should now have many more construction sets

    cset_from_lib = constr_set_lib.construction_set_by_identifier(constr_set_lib.CONSTRUCTION_SETS[0])
    assert isinstance(cset_from_lib, ConstructionSet)

    cset_from_lib = constr_set_lib.construction_set_by_identifier(constr_set_lib.CONSTRUCTION_SETS[2])
    assert isinstance(cset_from_lib, ConstructionSet)


def test_construction_set_by_identifier():
    """Test that all of the construction sets in the library can be loaded by identifier."""
    for c_set in constr_set_lib.CONSTRUCTION_SETS:
        cset_from_lib = constr_set_lib.construction_set_by_identifier(c_set)
        assert isinstance(cset_from_lib, ConstructionSet)
