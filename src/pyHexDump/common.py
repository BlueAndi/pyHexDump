"""This module provides common functions, used by different commands."""

# MIT License
#
# Copyright (c) 2022 - 2023 Andreas Merkle (web@blue-andi.de)
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
        with open(file_name, encoding="utf-8") as file_descriptor:
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
        with open(file_name, encoding="utf-8") as file_descriptor:
            template = file_descriptor.read()
    except FileNotFoundError:
        ret_status = Ret.ERROR_TEMPLATE_FILE_NOT_FOUND

    return ret_status, template

def common_print_address(addr, addr_format="{:04X}"):
    """Print the memory address in the given format.

    Args:
        addr (int): Memory address
        addr_format (str, optional): The output format. Defaults to "{:04X}".
    """
    print(addr_format.format(addr), end="")

def common_print_value(value, value_format="{:02X}"):
    """Print the value in the given format.

    Args:
        value (int, list): A single value or a list of values.
        value_format (str, optional): The output format. Defaults to "{:02X}".
    """
    # Array of values?
    if isinstance(value, list):
        # Print the array with a space between
        for idx, element in enumerate(value):
            if idx > 0:
                print(" ", end="")
            print(value_format.format(element), end="")
    else:
        # Print the single value
        print(value_format.format(value), end="")

def common_print_line(mem_access, addr, count):
    """Print a single line in the format:
        <address>: <data>

    Args:
        intel_hex_file (intelhex): The intel hex object.
        mem_access (MemAccess): The memory access API.
        addr (int): The memory start address.
        count (int): The number of elements to show.
    """
    common_print_address(addr)
    print(": ", end="")

    value_width = 2 * mem_access.get_size()
    value_format = "{:0" + str(value_width) + "X}"
    for idx in range(count):
        # Print space between each value
        if idx > 0:
            print(" ", end="")

        offset = idx * mem_access.get_size()
        common_print_value(mem_access.get_value(addr + offset), value_format)

def common_dump_intel_hex(mem_access, addr, count, next_line=16):
    """Dump some data, starting with the address in the format "<addr>: <data>".
        The address and the data is printed in hex.

    Args:
        mem_access (MemAccess): Memory access API
        addr (int): Address
        count (int): Number of elements
        next_line (int): A newline will be printed after this number of bytes.

    Returns:
        Ret: If successful, it will return Ret.OK otherwise a error code.
    """

    if next_line == 0:
        next_line = mem_access.get_size() * count

    full_line_cnt = next_line // mem_access.get_size()
    full_lines_cnt = 0
    last_line_element_cnt = 0

    if full_line_cnt > 0:
        full_lines_cnt = count // full_line_cnt
        last_line_element_cnt = count % full_line_cnt

    offset = 0
    for index in range(full_lines_cnt):
        # Print newline not for the first line but for all following lines
        if index > 0:
            print("")

        offset = index * next_line
        common_print_line(mem_access, addr + offset, full_line_cnt)

    if last_line_element_cnt > 0:
        # Print newline only if this is not the first line (no full lines available)
        if full_lines_cnt > 0:
            print("")

        common_print_line(mem_access, addr + offset, last_line_element_cnt)

    return Ret.OK

################################################################################
# Main
################################################################################
