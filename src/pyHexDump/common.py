"""This module provides common functions, used by different commands."""

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
import json

from intelhex import IntelHex
from pyHexDump.constants import Ret

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def common_load_binary_file(file_name):
    """Load binary file which to dump.

        If any error happen, it will return the error code and None instead of
        the file content.

    Args:
        file_name (str): File name of the binary file

    Returns:
        Ret, IntelHex: Status information and file content
    """
    ret_status = Ret.OK
    intel_hex_file = IntelHex()
    file_format = "bin"

    # Intel hex file? All others are handled as binary.
    if file_name.endswith(".hex"):
        file_format = "hex"

    try:
        intel_hex_file.fromfile(file_name, format=file_format)
    except FileNotFoundError:
        ret_status = Ret.ERROR_INPUT_FILE_NOT_FOUND
        intel_hex_file = None

    return ret_status, intel_hex_file

def common_load_json_file(file_name):
    """Load JSON file to dictionary.

        If any error happen, it will return the error code and None instead of
        the dictionary.

    Args:
        file_name (str): File name of the JSON file

    Returns:
        Ret, dict: Status information and dictionary
    """
    ret_status = Ret.OK
    config = None

    try:
        with open(file_name) as file_descriptor:
            config = json.load(file_descriptor)
    except FileNotFoundError:
        ret_status = Ret.ERROR_CONFIG_FILE_NOT_FOUND

    return ret_status, config

def common_load_template_file(file_name):
    """Load template file to dictionary.

        If any error happen, it will return the error code and None instead of
        the dictionary.

    Args:
        file_name (str): File name of the template file

    Returns:
        Ret, dict: Status information and dictionary
    """
    ret_status = Ret.OK
    template = None

    try:
        with open(file_name) as file_descriptor:
            template = file_descriptor.read()
    except FileNotFoundError:
        ret_status = Ret.ERROR_TEMPLATE_FILE_NOT_FOUND

    return ret_status, template

def common_dump_intel_hex(intel_hex, mem_access, addr, count, next_line=16):
    """Dump some data, starting with the address in the format "<addr>: <data>".
        The address and the data is printed in hex.

    Args:
        intel_hex (intelhex): Binary file
        mem_access (MemAccess): Memory access API
        addr (int): Address
        count (int): Number of elements
        next_line (int): A newline will be printed after this number of bytes.

    Returns:
        Ret: If successful, it will return Ret.OK otherwise a error code.
    """

    offset = 0 # byte
    for index in range(count):

        if (next_line == 0) and (index == 0):
            print("{:04x}: ".format(addr + offset), end="")

        elif (next_line > 0) and ((offset % next_line) == 0):
            if index > 0:
                print("")

            print("{:04x}: ".format(addr + offset), end="")

        elif index > 0:

            print(" ", end="")

        value = mem_access.get_value(intel_hex, addr + offset)

        print("{:0{num}x}".format(value, num=2 * mem_access.get_size()), end="")

        offset += mem_access.get_size()

    return Ret.OK

################################################################################
# Main
################################################################################
