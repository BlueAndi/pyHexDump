"""Tests
"""

from pyHexDump.cmd_checksum import cmd_register as cmd_checksum_register
from pyHexDump.prg_arg_parser import PrgArgParser
from pyHexDump.bunch import dict_to_bunch

def test_cmd_registration():
    """Test the command registration.
    """

    main_prg_arg_parser = PrgArgParser()
    cmd = cmd_checksum_register(main_prg_arg_parser.get_sub_parsers())

    assert cmd["name"] == "checksum"
    assert hasattr(cmd["execFunc"], "__call__") is True

def test_calc_checksum(capsys):
    """Test the checksum calculation algorithm with different
        polynomials, etc.

        Use http://www.sunshine2k.de/coding/javascript/crc/crc_js.html for verification.
    """
    main_prg_arg_parser = PrgArgParser()
    cmd = cmd_checksum_register(main_prg_arg_parser.get_sub_parsers())

    test_case_list = [{
        "binary_data_endianess": "uint8",
        "start_addr": 0,
        "end_addr": 8,
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
        "end_addr": 8,
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
        "end_addr": 8,
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
        "end_addr": 8,
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
        "end_addr": 8,
        "polynomial": 0x04C11DB7,
        "bit_width": 32,
        "seed": 0xFFFFFFFF,
        "reverse_in": False,
        "reverse_out": False,
        "final_xor": True,
        "expected": 0xB61C3D04
    }]

    for test_case in test_case_list:
        args = {
            "binaryFile": [ "tests/data/data.txt" ],
            "binaryDataEndianess": test_case["binary_data_endianess"],
            "saddr": test_case["start_addr"],
            "eaddr": test_case["end_addr"],
            "polynomial": test_case["polynomial"],
            "bitWidth": test_case["bit_width"],
            "seed": test_case["seed"],
            "reverseIn": test_case["reverse_in"],
            "reverseOut": test_case["reverse_out"],
            "finalXOR": test_case["final_xor"]
        }

        cmd["execFunc"](dict_to_bunch(args))

        captured = capsys.readouterr()

        # String compare to see the hex value in the assertion output
        assert f'{test_case["expected"]:02X}' == captured.out
