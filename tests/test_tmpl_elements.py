"""Tests
"""

# MIT License
#
# Copyright (c) 2022 - 2026 Andreas Merkle (web@blue-andi.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

################################################################################
# Imports
################################################################################
import struct
from pyHexDump.tmpl_element import TmplElementInt, TmplElementIntList, \
    TmplElementFloat, TmplElementFloatList, TmplElementStr

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def test_tmpl_element() -> None:
    """Test the template element class with different representations.
    """
    # Test uint8
    test_value = 1
    tmpl_element = TmplElementInt("test", 0, test_value, 8)
    assert f"0x{test_value:02X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test uint16
    test_value = 45000
    tmpl_element = TmplElementInt("test", 0, test_value, 16)
    assert f"0x{test_value:04X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test uint32
    test_value = 80000
    tmpl_element = TmplElementInt("test", 0, test_value, 32)
    assert f"0x{test_value:08X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test uint64
    test_value = 12345789
    tmpl_element = TmplElementInt("test", 0, test_value, 64)
    assert f"0x{test_value:016X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test sint8
    test_value = -1
    value_raw = test_value & ((1 << 8) - 1)
    tmpl_element = TmplElementInt("test", 0, test_value, 8)
    assert f"0x{value_raw:02X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test sint16
    test_value = -10000
    value_raw = test_value & ((1 << 16) - 1)
    tmpl_element = TmplElementInt("test", 0, test_value, 16)
    assert f"0x{value_raw:04X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test sint32
    test_value = -500000
    value_raw = test_value & ((1 << 32) - 1)
    tmpl_element = TmplElementInt("test", 0, test_value, 32)
    assert f"0x{value_raw:08X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test sint64
    test_value = -12345789
    value_raw = test_value & ((1 << 64) - 1)
    tmpl_element = TmplElementInt("test", 0, test_value, 64)
    assert f"0x{value_raw:016X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test float32
    test_value = 1.2345
    value_raw = struct.unpack('<I', struct.pack('<f', test_value))[0]
    tmpl_element = TmplElementFloat("test", 0, test_value, 32)
    assert f"0x{value_raw:08X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test float64
    test_value = 1.2345
    value_raw = struct.unpack('<Q', struct.pack('<d', test_value))[0]
    tmpl_element = TmplElementFloat("test", 0, test_value, 64)
    assert f"0x{value_raw:016X}" == tmpl_element.hex()
    assert test_value == tmpl_element

def test_tmpl_element_with_array_part_1() -> None:
    """Test the template element class with different representations
        in case its an array.
    """

    # Test array of uint8
    test_values = [0, 1, 2, 3]
    tmpl_element = TmplElementIntList("test", 0, test_values, 8)

    hex_str = "["
    for idx, value in enumerate(test_values):
        if idx > 0:
            hex_str += ", "
        hex_str += f"0x{value:02X}"
    hex_str += "]"
    assert hex_str == tmpl_element.hex()

    for idx, value in enumerate(test_values):
        assert value == tmpl_element[idx]

    # Test uint16
    test_values = [0, 1, 2, 3]
    tmpl_element = TmplElementIntList("test", 0, test_values, 16)

    hex_str = "["
    for idx, value in enumerate(test_values):
        if idx > 0:
            hex_str += ", "
        hex_str += f"0x{value:04X}"
    hex_str += "]"
    assert hex_str == tmpl_element.hex()

    for idx, value in enumerate(test_values):
        assert value == tmpl_element[idx]

    # Test uint32
    test_values = [0, 1, 2, 3]
    tmpl_element = TmplElementIntList("test", 0, test_values, 32)

    hex_str = "["
    for idx, value in enumerate(test_values):
        if idx > 0:
            hex_str += ", "
        hex_str += f"0x{value:08X}"
    hex_str += "]"
    assert hex_str == tmpl_element.hex()

    for idx, value in enumerate(test_values):
        assert value == tmpl_element[idx]

    # Test uint64
    test_values = [0, 1, 2, 3]
    tmpl_element = TmplElementIntList("test", 0, test_values, 64)

    hex_str = "["
    for idx, value in enumerate(test_values):
        if idx > 0:
            hex_str += ", "
        hex_str += f"0x{value:016X}"
    hex_str += "]"
    assert hex_str == tmpl_element.hex()

    for idx, value in enumerate(test_values):
        assert value == tmpl_element[idx]

def test_tmpl_element_with_array_part_2() -> None:
    """Test the template element class with different representations
        in case its an array.
    """

    # Test sint8
    test_values = [0, -1, -2, -3]
    tmpl_element = TmplElementIntList("test", 0, test_values, 8)

    hex_str = "["
    for idx, value in enumerate(test_values):
        if idx > 0:
            hex_str += ", "
        value_raw = value & ((1 << 8) - 1)
        hex_str += f"0x{value_raw:02X}"
    hex_str += "]"
    assert hex_str == tmpl_element.hex()

    for idx, value in enumerate(test_values):
        assert value == tmpl_element[idx]

    # Test sint16
    test_values = [0, -1, -2, -3]
    tmpl_element = TmplElementIntList("test", 0, test_values, 16)

    hex_str = "["
    for idx, value in enumerate(test_values):
        if idx > 0:
            hex_str += ", "
        value_raw = value & ((1 << 16) - 1)
        hex_str += f"0x{value_raw:04X}"
    hex_str += "]"
    assert hex_str == tmpl_element.hex()

    for idx, value in enumerate(test_values):
        assert value == tmpl_element[idx]

    # Test sint32
    test_values = [0, -1, -2, -3]
    tmpl_element = TmplElementIntList("test", 0, test_values, 32)

    hex_str = "["
    for idx, value in enumerate(test_values):
        if idx > 0:
            hex_str += ", "
        value_raw = value & ((1 << 32) - 1)
        hex_str += f"0x{value_raw:08X}"
    hex_str += "]"
    assert hex_str == tmpl_element.hex()

    for idx, value in enumerate(test_values):
        assert value == tmpl_element[idx]

    # Test sint64
    test_values = [0, -1, -2, -3]
    tmpl_element = TmplElementIntList("test", 0, test_values, 64)

    hex_str = "["
    for idx, value in enumerate(test_values):
        if idx > 0:
            hex_str += ", "
        value_raw = value & ((1 << 64) - 1)
        hex_str += f"0x{value_raw:016X}"
    hex_str += "]"
    assert hex_str == tmpl_element.hex()

    for idx, value in enumerate(test_values):
        assert value == tmpl_element[idx]

def test_tmpl_element_with_array_part_3() -> None:
    """Test the template element class with different representations
        in case its an array.
    """

    # Test float32
    test_values = [0.123, 1.234, 12.345, 123.456]
    tmpl_element = TmplElementFloatList("test", 0, test_values, 32)

    hex_str = "["
    for idx, value in enumerate(test_values):
        if idx > 0:
            hex_str += ", "
        value_raw = struct.unpack('<I', struct.pack('<f', value))[0]
        hex_str += f"0x{value_raw:08X}"
    hex_str += "]"
    assert hex_str == tmpl_element.hex()

    for idx, value in enumerate(test_values):
        assert value == tmpl_element[idx]

    # Test float64
    test_values = [0.123, 1.234, 12.345, 123.456]
    tmpl_element = TmplElementFloatList("test", 0, test_values, 64)

    hex_str = "["
    for idx, value in enumerate(test_values):
        if idx > 0:
            hex_str += ", "
        value_raw = struct.unpack('<Q', struct.pack('<d', value))[0]
        hex_str += f"0x{value_raw:016X}"
    hex_str += "]"
    assert hex_str == tmpl_element.hex()

    for idx, value in enumerate(test_values):
        assert value == tmpl_element[idx]

    test_values = "abcd"
    tmpl_element = TmplElementStr("test", 0, test_values, 8)

    hex_str = "["
    for idx, value in enumerate(test_values):
        if idx > 0:
            hex_str += ", "
        value_raw = ord(test_values[idx])
        hex_str += f"0x{value_raw:02X}"
    hex_str += "]"
    assert hex_str == tmpl_element.hex()

    assert test_values == tmpl_element

################################################################################
# Main
################################################################################
