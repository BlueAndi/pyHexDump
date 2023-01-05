"""Test
"""

from pyHexDump.bunch import dict_to_bunch

def test_bunch():
    """Test bunch
    """
    test_dict = {
        "a": {
            "b": {
                "c": 55
            }
        }
    }

    result = dict_to_bunch(test_dict)

    assert result.a.b.c == 55 #pylint: disable=no-member
