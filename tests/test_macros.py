"""Tests
"""

import struct
from intelhex import IntelHex
from pyHexDump.macros import get_macro_dict, set_binary_data

def test_macros_read_unsigned_integers():
    """Test macros to read unsigned integer values.
    """
    binary_data = IntelHex()
    test_data = []

    # Test data values shall be [0;8[
    for idx in range(8):
        test_data.append(idx)

    # Prepare binary data
    for idx, _ in enumerate(test_data):
        binary_data[idx] = test_data[idx]

    macro_dict = get_macro_dict()
    set_binary_data(binary_data)

    # uint8 access
    value = macro_dict["m_read_uint8"](0)
    assert test_data[0] == value

    # uint16le access
    value = macro_dict["m_read_uint16le"](0)
    expected = 0
    for idx in range(2):
        expected |= test_data[idx] << (idx * 8)
    assert hex(expected) == hex(value)

    # uint16be access
    value = macro_dict["m_read_uint16be"](0)
    expected = 0
    for idx in range(2):
        expected |= test_data[idx] << (8 - idx * 8)
    assert hex(expected) == hex(value)

    # uint32le access
    value = macro_dict["m_read_uint32le"](0)
    expected = 0
    for idx in range(4):
        expected |= test_data[idx] << (idx * 8)
    assert hex(expected) == hex(value)

    # uint32be access
    value = macro_dict["m_read_uint32be"](0)
    expected = 0
    for idx in range(4):
        expected |= test_data[idx] << (24 - idx * 8)
    assert hex(expected) == hex(value)

    # uint64le access
    value = macro_dict["m_read_uint64le"](0)
    expected = 0
    for idx in range(8):
        expected |= test_data[idx] << (idx * 8)
    assert hex(expected) == hex(value)

    # uint64be access
    value = macro_dict["m_read_uint64be"](0)
    expected = 0
    for idx in range(8):
        expected |= test_data[idx] << (56 - idx * 8)
    assert hex(expected) == hex(value)

def test_macros_read_signed_integers():
    """Test macros to read signed integer values.
    """
    binary_data = IntelHex()

    macro_dict = get_macro_dict()
    set_binary_data(binary_data)

    # int8 access
    test_value = -128
    bit_width = 8
    value_raw = test_value & (2**bit_width - 1)
    binary_data[0] = value_raw
    value = macro_dict["m_read_int8"](0)
    assert test_value == value

    # int16le access
    test_value = -512
    bit_width = 16
    value_raw = test_value & (2**bit_width - 1)
    binary_data[0] = (value_raw >> 0) & 0xff
    binary_data[1] = (value_raw >> 8) & 0xff
    value = macro_dict["m_read_int16le"](0)
    assert test_value == value

    # int16be access
    test_value = -513
    bit_width = 16
    value_raw = test_value & (2**bit_width - 1)
    binary_data[0] = (value_raw >> 8) & 0xff
    binary_data[1] = (value_raw >> 0) & 0xff
    value = macro_dict["m_read_int16be"](0)
    assert test_value == value

    # int32le access
    test_value = -80001
    bit_width = 32
    value_raw = test_value & (2**bit_width - 1)
    binary_data[0] = (value_raw >>  0) & 0xff
    binary_data[1] = (value_raw >>  8) & 0xff
    binary_data[2] = (value_raw >> 16) & 0xff
    binary_data[3] = (value_raw >> 24) & 0xff
    value = macro_dict["m_read_int32le"](0)
    assert test_value == value

    # int32be access
    test_value = -80002
    bit_width = 32
    value_raw = test_value & (2**bit_width - 1)
    binary_data[0] = (value_raw >> 24) & 0xff
    binary_data[1] = (value_raw >> 16) & 0xff
    binary_data[2] = (value_raw >>  8) & 0xff
    binary_data[3] = (value_raw >>  0) & 0xff
    value = macro_dict["m_read_int32be"](0)
    assert test_value == value

def test_macros_read_float32():
    """Test macros to read 32-bit floating values.
    """
    binary_data = IntelHex()

    macro_dict = get_macro_dict()
    set_binary_data(binary_data)

    # float32le access
    test_value = 1.2345
    value_raw = struct.unpack('<I', struct.pack('<f', test_value))[0]
    binary_data[0] = (value_raw >>  0) & 0xff
    binary_data[1] = (value_raw >>  8) & 0xff
    binary_data[2] = (value_raw >> 16) & 0xff
    binary_data[3] = (value_raw >> 24) & 0xff
    value = macro_dict["m_read_float32le"](0)
    epsilon = 0.000001
    assert (test_value + epsilon) > value
    assert (test_value - epsilon) < value

    # float32be access
    test_value = 1.2345
    value_raw = struct.unpack('<I', struct.pack('<f', test_value))[0]
    binary_data[0] = (value_raw >> 24) & 0xff
    binary_data[1] = (value_raw >> 16) & 0xff
    binary_data[2] = (value_raw >>  8) & 0xff
    binary_data[3] = (value_raw >>  0) & 0xff
    value = macro_dict["m_read_float32be"](0)
    epsilon = 0.000001
    assert (test_value + epsilon) > value
    assert (test_value - epsilon) < value

def test_macros_read_float64():
    """Test macros to read 64-bit floating values.
    """
    binary_data = IntelHex()

    macro_dict = get_macro_dict()
    set_binary_data(binary_data)

    # float64le access
    test_value = 1.6789
    value_raw = struct.unpack('<Q', struct.pack('<d', test_value))[0]
    binary_data[0] = (value_raw >>  0) & 0xff
    binary_data[1] = (value_raw >>  8) & 0xff
    binary_data[2] = (value_raw >> 16) & 0xff
    binary_data[3] = (value_raw >> 24) & 0xff
    binary_data[4] = (value_raw >> 32) & 0xff
    binary_data[5] = (value_raw >> 40) & 0xff
    binary_data[6] = (value_raw >> 48) & 0xff
    binary_data[7] = (value_raw >> 56) & 0xff
    value = macro_dict["m_read_float64le"](0)
    epsilon = 0.000001
    assert (test_value + epsilon) > value
    assert (test_value - epsilon) < value

    # float64be access
    test_value = 1.6789
    value_raw = struct.unpack('<Q', struct.pack('<d', test_value))[0]
    binary_data[0] = (value_raw >> 56) & 0xff
    binary_data[1] = (value_raw >> 48) & 0xff
    binary_data[2] = (value_raw >> 40) & 0xff
    binary_data[3] = (value_raw >> 32) & 0xff
    binary_data[4] = (value_raw >> 24) & 0xff
    binary_data[5] = (value_raw >> 16) & 0xff
    binary_data[6] = (value_raw >>  8) & 0xff
    binary_data[7] = (value_raw >>  0) & 0xff
    value = macro_dict["m_read_float64be"](0)
    epsilon = 0.000001
    assert (test_value + epsilon) > value
    assert (test_value - epsilon) < value

def test_macros_swap():
    """Test macros for data swapping
    """
    macro_dict = get_macro_dict()

    # Swap bytes
    value = 0x1234
    expected = 0x3412
    value = macro_dict["m_swap_bytes_u16"](value)
    assert hex(expected) == hex(value)

    # Swap bytes
    value = 0x12345678
    expected = 0x78563412
    value = macro_dict["m_swap_bytes_u32"](value)
    assert hex(expected) == hex(value)

    # Swap words
    value = 0x12345678
    expected = 0x56781234
    value = macro_dict["m_swap_words_u32"](value)
    assert hex(expected) == hex(value)

def test_macro_string():
    """Test macro for reading a string.
    """
    binary_data = IntelHex()

    macro_dict = get_macro_dict()
    set_binary_data(binary_data)

    test_string = "Hello World!"
    test_string_len = len(test_string)

    for idx in range(test_string_len):
        binary_data[idx] = ord(test_string[idx])
    binary_data[test_string_len] = 0

    value = macro_dict["m_read_string"](0)

    assert test_string == value
