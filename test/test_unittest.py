"""Tests
"""

import struct
from intelhex import IntelHex
from pyHexDump.constants import Ret
from pyHexDump.mem_access import mem_access_get_api_by_data_type
from pyHexDump.common import common_dump_intel_hex
from pyHexDump.cmd_checksum import calc_checksum
from pyHexDump.macros import get_macro_dict, set_binary_data
from pyHexDump.cmd_print import TmplElement

def test_dump(capsys):
    """Test the dump of binary data.
    """
    binary_data = IntelHex()
    test_data = "12345678"

    # Prepare binary data
    for idx, _ in enumerate(test_data):
        binary_data[idx] = ord(test_data[idx])

    # unsigned 8-bit dump
    mem_access_api = mem_access_get_api_by_data_type("u8")
    mem_access_api.set_binary_data(binary_data)

    ret_status = common_dump_intel_hex(mem_access_api, 0, len(test_data))

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 31 32 33 34 35 36 37 38"

    # unsigned 16-bit LE dump
    mem_access_api = mem_access_get_api_by_data_type("u16le")
    mem_access_api.set_binary_data(binary_data)

    ret_status = common_dump_intel_hex(mem_access_api, 0, len(test_data) // 2)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 3231 3433 3635 3837"

    # unsigned 16-bit BE dump
    mem_access_api = mem_access_get_api_by_data_type("u16be")
    mem_access_api.set_binary_data(binary_data)

    ret_status = common_dump_intel_hex(mem_access_api, 0, len(test_data) // 2)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 3132 3334 3536 3738"

    # unsigned 32-bit LE dump
    mem_access_api = mem_access_get_api_by_data_type("u32le")
    mem_access_api.set_binary_data(binary_data)

    ret_status = common_dump_intel_hex(mem_access_api, 0, len(test_data) // 4)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 34333231 38373635"

    # unsigned 32-bit BE dump
    mem_access_api = mem_access_get_api_by_data_type("u32be")
    mem_access_api.set_binary_data(binary_data)

    ret_status = common_dump_intel_hex(mem_access_api, 0, len(test_data) // 4)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 31323334 35363738"

    # unsigned 8-bit dump - next line after half number of bytes
    mem_access_api = mem_access_get_api_by_data_type("u8")
    mem_access_api.set_binary_data(binary_data)

    ret_status = common_dump_intel_hex(mem_access_api, 0, len(test_data), len(test_data) // 2)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 31 32 33 34\n0004: 35 36 37 38"

def test_calc_checksum():
    """Test the checksum calculation algorthm with different
        polynomials, etc.
    """
    binary_data = IntelHex()
    test_data = "12345678"
    crc = 0

    # Prepare binary data
    for idx, _ in enumerate(test_data):
        binary_data[idx] = ord(test_data[idx])

    test_case_list = [{
        "binary_data_endianess": "u8",
        "start_addr": 0,
        "end_addr": len(test_data),
        "polynomial": 0x07,
        "bit_width": 8,
        "seed": 0x00,
        "reverse_in": False,
        "reverse_out": False,
        "final_xor": False,
        "expected": 0xC7
    }, {
        "binary_data_endianess": "u8",
        "start_addr": 0,
        "end_addr": len(test_data),
        "polynomial": 0x07,
        "bit_width": 8,
        "seed": 0x00,
        "reverse_in": False,
        "reverse_out": True, # Reflected
        "final_xor": False,
        "expected": 0xE3
    }, {
        "binary_data_endianess": "u8",
        "start_addr": 0,
        "end_addr": len(test_data),
        "polynomial": 0x07,
        "bit_width": 8,
        "seed": 0x00,
        "reverse_in": False,
        "reverse_out": False,
        "final_xor": True, # Inverted
        "expected": 0x38
    }, {
        "binary_data_endianess": "u8",
        "start_addr": 0,
        "end_addr": len(test_data),
        "polynomial": 0x04C11DB7,
        "bit_width": 32,
        "seed": 0xFFFFFFFF,
        "reverse_in": False,
        "reverse_out": False,
        "final_xor": True,
        "expected": 0xB61C3D04
    }]

    for test_case in test_case_list:
        # pylint: disable-next=too-many-function-args
        crc = calc_checksum(binary_data, test_case["binary_data_endianess"], \
                            test_case["start_addr"], \
                            test_case["end_addr"], \
                            test_case["polynomial"], \
                            test_case["bit_width"], \
                            test_case["seed"], \
                            test_case["reverse_in"], \
                            test_case["reverse_out"], \
                            test_case["final_xor"])

        # String compare to see the hex value in the assertion output
        assert hex(crc) == hex(test_case["expected"])

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

    # u8 access
    value = macro_dict["m_read_u8"](0)
    assert test_data[0] == value

    # u16le access
    value = macro_dict["m_read_u16le"](0)
    expected = 0
    for idx in range(2):
        expected |= test_data[idx] << (idx * 8)
    assert hex(expected) == hex(value)

    # u16be access
    value = macro_dict["m_read_u16be"](0)
    expected = 0
    for idx in range(2):
        expected |= test_data[idx] << (8 - idx * 8)
    assert hex(expected) == hex(value)

    # u32le access
    value = macro_dict["m_read_u32le"](0)
    expected = 0
    for idx in range(4):
        expected |= test_data[idx] << (idx * 8)
    assert hex(expected) == hex(value)

    # u32be access
    value = macro_dict["m_read_u32be"](0)
    expected = 0
    for idx in range(4):
        expected |= test_data[idx] << (24 - idx * 8)
    assert hex(expected) == hex(value)

    # u64le access
    value = macro_dict["m_read_u64le"](0)
    expected = 0
    for idx in range(8):
        expected |= test_data[idx] << (idx * 8)
    assert hex(expected) == hex(value)

    # u64be access
    value = macro_dict["m_read_u64be"](0)
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

    # s8 access
    test_value = -128
    bit_width = 8
    value_raw = test_value & (2**bit_width - 1)
    binary_data[0] = value_raw
    value = macro_dict["m_read_s8"](0)
    assert test_value == value

    # s16le access
    test_value = -512
    bit_width = 16
    value_raw = test_value & (2**bit_width - 1)
    binary_data[0] = (value_raw >> 0) & 0xff
    binary_data[1] = (value_raw >> 8) & 0xff
    value = macro_dict["m_read_s16le"](0)
    assert test_value == value

    # s16be access
    test_value = -513
    bit_width = 16
    value_raw = test_value & (2**bit_width - 1)
    binary_data[0] = (value_raw >> 8) & 0xff
    binary_data[1] = (value_raw >> 0) & 0xff
    value = macro_dict["m_read_s16be"](0)
    assert test_value == value

    # s32le access
    test_value = -80001
    bit_width = 32
    value_raw = test_value & (2**bit_width - 1)
    binary_data[0] = (value_raw >>  0) & 0xff
    binary_data[1] = (value_raw >>  8) & 0xff
    binary_data[2] = (value_raw >> 16) & 0xff
    binary_data[3] = (value_raw >> 24) & 0xff
    value = macro_dict["m_read_s32le"](0)
    assert test_value == value

    # s32be access
    test_value = -80002
    bit_width = 32
    value_raw = test_value & (2**bit_width - 1)
    binary_data[0] = (value_raw >> 24) & 0xff
    binary_data[1] = (value_raw >> 16) & 0xff
    binary_data[2] = (value_raw >>  8) & 0xff
    binary_data[3] = (value_raw >>  0) & 0xff
    value = macro_dict["m_read_s32be"](0)
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

def test_tmpl_element():
    """Test the template element class with different representations.
    """
    # Test uint8
    test_value = 1
    tmpl_element = TmplElement(0, test_value, 8)
    assert f"0x{test_value:02X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test uint16
    test_value = 45000
    tmpl_element = TmplElement(0, test_value, 16)
    assert f"0x{test_value:04X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test uint32
    test_value = 80000
    tmpl_element = TmplElement(0, test_value, 32)
    assert f"0x{test_value:08X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test uint64
    test_value = 12345789
    tmpl_element = TmplElement(0, test_value, 64)
    assert f"0x{test_value:016X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test sint8
    test_value = -1
    value_raw = test_value & ((1 << 8) - 1)
    tmpl_element = TmplElement(0, test_value, 8)
    assert f"0x{value_raw:02X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test sint16
    test_value = -10000
    value_raw = test_value & ((1 << 16) - 1)
    tmpl_element = TmplElement(0, test_value, 16)
    assert f"0x{value_raw:04X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test sint32
    test_value = -500000
    value_raw = test_value & ((1 << 32) - 1)
    tmpl_element = TmplElement(0, test_value, 32)
    assert f"0x{value_raw:08X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test sint64
    test_value = -12345789
    value_raw = test_value & ((1 << 64) - 1)
    tmpl_element = TmplElement(0, test_value, 64)
    assert f"0x{value_raw:016X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test float32
    test_value = 1.2345
    value_raw = struct.unpack('<I', struct.pack('<f', test_value))[0]
    tmpl_element = TmplElement(0, test_value, 32)
    assert f"0x{value_raw:08X}" == tmpl_element.hex()
    assert test_value == tmpl_element

    # Test float64
    test_value = 1.2345
    value_raw = struct.unpack('<Q', struct.pack('<d', test_value))[0]
    tmpl_element = TmplElement(0, test_value, 64)
    assert f"0x{value_raw:016X}" == tmpl_element.hex()
    assert test_value == tmpl_element

def test_tmpl_element_with_array_part_1():
    """Test the template element class with different representations
        in case its an array.
    """

    # Test array of uint8
    test_values = [0, 1, 2, 3]
    tmpl_element = TmplElement(0, test_values, 8)

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
    tmpl_element = TmplElement(0, test_values, 16)

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
    tmpl_element = TmplElement(0, test_values, 32)

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
    tmpl_element = TmplElement(0, test_values, 64)

    hex_str = "["
    for idx, value in enumerate(test_values):
        if idx > 0:
            hex_str += ", "
        hex_str += f"0x{value:016X}"
    hex_str += "]"
    assert hex_str == tmpl_element.hex()

    for idx, value in enumerate(test_values):
        assert value == tmpl_element[idx]

def test_tmpl_element_with_array_part_2():
    """Test the template element class with different representations
        in case its an array.
    """

    # Test sint8
    test_values = [0, -1, -2, -3]
    tmpl_element = TmplElement(0, test_values, 8)

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
    tmpl_element = TmplElement(0, test_values, 16)

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
    tmpl_element = TmplElement(0, test_values, 32)

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
    tmpl_element = TmplElement(0, test_values, 64)

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

def test_tmpl_element_with_array_part_3():
    """Test the template element class with different representations
        in case its an array.
    """

    # Test float32
    test_values = [0.123, 1.234, 12.345, 123.456]
    tmpl_element = TmplElement(0, test_values, 32)

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
    tmpl_element = TmplElement(0, test_values, 64)

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
