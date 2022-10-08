"""Tests
"""

from intelhex import IntelHex
from pyHexDump.constants import Ret
from pyHexDump.mem_access import mem_access_get_api_by_data_type
from pyHexDump.common import common_dump_intel_hex
from pyHexDump.cmd_checksum import calc_checksum

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

    ret_status = common_dump_intel_hex(binary_data, mem_access_api, 0, len(test_data))

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 31 32 33 34 35 36 37 38"

    # unsigned 16-bit LE dump
    mem_access_api = mem_access_get_api_by_data_type("u16le")

    ret_status = common_dump_intel_hex(binary_data, mem_access_api, 0, len(test_data) // 2)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 3231 3433 3635 3837"

    # unsigned 16-bit BE dump
    mem_access_api = mem_access_get_api_by_data_type("u16be")

    ret_status = common_dump_intel_hex(binary_data, mem_access_api, 0, len(test_data) // 2)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 3132 3334 3536 3738"

    # unsigned 32-bit LE dump
    mem_access_api = mem_access_get_api_by_data_type("u32le")

    ret_status = common_dump_intel_hex(binary_data, mem_access_api, 0, len(test_data) // 4)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 34333231 38373635"

    # unsigned 32-bit BE dump
    mem_access_api = mem_access_get_api_by_data_type("u32be")

    ret_status = common_dump_intel_hex(binary_data, mem_access_api, 0, len(test_data) // 4)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 31323334 35363738"

    # unsigned 8-bit dump - next line after half number of bytes
    mem_access_api = mem_access_get_api_by_data_type("u8")

    ret_status = common_dump_intel_hex(binary_data, mem_access_api, 0, \
                                        len(test_data), len(test_data) // 2)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 31 32 33 34\n0004: 35 36 37 38"

def test_calc_checksum():
    """Test the checksum calculation algorthm with different
        polynomials, etc.
    """
    binary_data = IntelHex()
    test_data = "12345678"
    ret_status = Ret.ERROR
    crc = 0

    # Prepare binary data
    for idx, _ in enumerate(test_data):
        binary_data[idx] = ord(test_data[idx])

    test_case_list = [{
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
        ret_status, crc = calc_checksum(binary_data, test_case["start_addr"], \
            test_case["end_addr"], test_case["polynomial"], test_case["bit_width"], \
            test_case["seed"], test_case["reverse_in"], test_case["reverse_out"], \
            test_case["final_xor"])

        print(test_case)
        assert ret_status == Ret.OK

        # String compare to see the hex value in the assertion output
        assert hex(crc) == hex(test_case["expected"])
