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
import pytest
from pyHexDump.cmd_checksum import _cmd_checksum, calc_checksum, cmd_register as cmd_checksum_register
from pyHexDump.constants import Ret
from pyHexDump.prg_arg_parser import PrgArgParser
from pyHexDump.bunch import dict_to_bunch

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def test_cmd_registration() -> None:
    """Test the command registration.
    """

    main_prg_arg_parser = PrgArgParser()
    cmd = cmd_checksum_register(main_prg_arg_parser.get_sub_parsers())

    assert cmd["name"] == "checksum"
    assert hasattr(cmd["execFunc"], "__call__") is True

def test_calc_checksum(capsys: pytest.CaptureFixture[str]) -> None:
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

def test_calc_checksum_rejects_unaligned_range() -> None:
    """A checksum range must contain whole elements of the selected type."""
    with pytest.raises(ValueError, match="aligned"):
        calc_checksum(None, "uint16le", 0, 3, 0x07, 8, 0, False, False, False)

def test_cmd_checksum_reports_unaligned_range(capsys: pytest.CaptureFixture[str]) -> None:
    """Invalid checksum ranges return the checksum error status."""
    status = _cmd_checksum(
        "tests/data/data.txt", "uint16le", 0, 3, 0x07, 8, 0, False, False, False
    )

    captured = capsys.readouterr()
    assert status == Ret.ERROR_CRC_CACLULATION
    assert "aligned to the data type size" in captured.out

################################################################################
# Main
################################################################################
