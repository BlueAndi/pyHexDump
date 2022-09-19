"""Command to show a hex dump."""

# MIT License
#
# Copyright (c) 2022 Andreas Merkle (web@blue-andi.de)
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
from pyHexDump.constants import Ret
from pyHexDump.common import common_load_binary_file, common_dump_intel_hex
from pyHexDump.mem_access import mem_access_get_api_by_data_type

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def cmd_dump(binary_file, addr, count, data_type):
    """Dump binary file to the console at the given address. It will contain a
        number of elements (count) depended on the data type (data_type).

    Args:
        binary_file (str): File name of the binary file
        addr (int): Address where to start the dump
        count (int): Number of elements which to dump
        data_type (str): Data type of a element (u8, u16le, u16be, u32le, u32be)

    Returns:
        Ret: If successful it will return OK, otherwise a corresponding error code.
    """
    ret_status, intel_hex = common_load_binary_file(binary_file)

    if ret_status == Ret.OK:
        mem_access = mem_access_get_api_by_data_type(data_type)
        ret_status = common_dump_intel_hex(intel_hex, mem_access, addr, count)
        print("")

    return ret_status

################################################################################
# Main
################################################################################
