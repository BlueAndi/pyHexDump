"""Tests
"""

from intelhex import IntelHex
from pyHexDump.constants import Ret
from pyHexDump.mem_access import mem_access_get_api_by_data_type
from pyHexDump.common import common_dump_intel_hex

def test_dump(capsys):
    """Test the dump of binary data.
    """
    binary_data = IntelHex()
    test_data = "12345678"

    # Prepare binary data
    for idx, _ in enumerate(test_data):
        binary_data[idx] = ord(test_data[idx])

    # unsigned 8-bit dump
    mem_access_api = mem_access_get_api_by_data_type("uint8")
    mem_access_api.set_binary_data(binary_data)

    ret_status = common_dump_intel_hex(mem_access_api, 0, len(test_data))

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 31 32 33 34 35 36 37 38"

    # unsigned 16-bit LE dump
    mem_access_api = mem_access_get_api_by_data_type("uint16le")
    mem_access_api.set_binary_data(binary_data)

    ret_status = common_dump_intel_hex(mem_access_api, 0, len(test_data) // 2)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 3231 3433 3635 3837"

    # unsigned 16-bit BE dump
    mem_access_api = mem_access_get_api_by_data_type("uint16be")
    mem_access_api.set_binary_data(binary_data)

    ret_status = common_dump_intel_hex(mem_access_api, 0, len(test_data) // 2)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 3132 3334 3536 3738"

    # unsigned 32-bit LE dump
    mem_access_api = mem_access_get_api_by_data_type("uint32le")
    mem_access_api.set_binary_data(binary_data)

    ret_status = common_dump_intel_hex(mem_access_api, 0, len(test_data) // 4)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 34333231 38373635"

    # unsigned 32-bit BE dump
    mem_access_api = mem_access_get_api_by_data_type("uint32be")
    mem_access_api.set_binary_data(binary_data)

    ret_status = common_dump_intel_hex(mem_access_api, 0, len(test_data) // 4)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 31323334 35363738"

    # unsigned 8-bit dump - next line after half number of bytes
    mem_access_api = mem_access_get_api_by_data_type("uint8")
    mem_access_api.set_binary_data(binary_data)

    ret_status = common_dump_intel_hex(mem_access_api, 0, len(test_data), len(test_data) // 2)

    captured = capsys.readouterr()

    assert ret_status == Ret.OK
    assert captured.out == "0000: 31 32 33 34\n0004: 35 36 37 38"
