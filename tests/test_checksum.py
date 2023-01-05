"""Tests
"""

from intelhex import IntelHex
from pyHexDump.cmd_checksum import calc_checksum

def test_calc_checksum():
    """Test the checksum calculation algorithm with different
        polynomials, etc.

        Use http://www.sunshine2k.de/coding/javascript/crc/crc_js.html for verification.
    """
    binary_data = IntelHex()
    test_data = "12345678"
    crc = 0

    # Prepare binary data
    for idx, _ in enumerate(test_data):
        binary_data[idx] = ord(test_data[idx])

    test_case_list = [{
        "binary_data_endianess": "uint8",
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
        "binary_data_endianess": "uint8",
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
        "binary_data_endianess": "uint8",
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
        "binary_data_endianess": "uint8",
        "start_addr": 0,
        "end_addr": len(test_data),
        "polynomial": 0x07,
        "bit_width": 8,
        "seed": 0x00,
        "reverse_in": True, # Reflected
        "reverse_out": False,
        "final_xor": False,
        "expected": 0xf1
    }, {
        "binary_data_endianess": "uint8",
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
