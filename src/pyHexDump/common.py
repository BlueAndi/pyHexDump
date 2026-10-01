"""This module provides common functions, used by different commands."""

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
import json
from typing import Any

from intelhex import IntelHex
from pyHexDump.constants import Ret
from pyHexDump.mem_access import IMemAccess

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def common_load_binary_file(file_name: str) -> tuple[Ret, IntelHex | None]:
    """Load a binary or Intel HEX file.

    Args:
        file_name: Path to the input file.

    Returns:
        A status code and the loaded data, or None when the file is missing.
    """
    ret_status = Ret.OK
    intel_hex_file = IntelHex()
    file_format = "bin"

    if file_name.endswith(".hex"):
        file_format = "hex"

    try:
        intel_hex_file.fromfile(file_name, format=file_format)
    except FileNotFoundError:
        ret_status = Ret.ERROR_INPUT_FILE_NOT_FOUND
        intel_hex_file = None

    return ret_status, intel_hex_file

def common_load_json_file(file_name: str) -> tuple[Ret, Any | None]:
    """Load a JSON file.

    Args:
        file_name: Path to the JSON file.

    Returns:
        A status code and the decoded JSON value, or None when the file is missing.
    """
    ret_status = Ret.OK
    config = None

    try:
        with open(file_name, encoding="utf-8") as file_descriptor:
            config = json.load(file_descriptor)
    except FileNotFoundError:
        ret_status = Ret.ERROR_CONFIG_FILE_NOT_FOUND

    return ret_status, config

def common_load_template_file(file_name: str) -> tuple[Ret, str | None]:
    """Load a text template file.

    Args:
        file_name: Path to the template file.

    Returns:
        A status code and template text, or None when the file is missing.
    """
    ret_status = Ret.OK
    template = None

    try:
        with open(file_name, encoding="utf-8") as file_descriptor:
            template = file_descriptor.read()
    except FileNotFoundError:
        ret_status = Ret.ERROR_TEMPLATE_FILE_NOT_FOUND

    return ret_status, template

def common_print_address(addr: int, addr_format: str = "{:04X}") -> None:
    """Print a memory address using the requested format.

    Args:
        addr: Address to print.
        addr_format: Format string applied to the address.

    Returns:
        None: The formatted address is written to stdout.
    """
    print(addr_format.format(addr), end="")

def common_print_value(value: int | float | list[int | float], value_format: str = "{:02X}") -> None:
    """Print one value or a list of values using the requested format.

    Args:
        value: Numeric value or list of numeric values to print.
        value_format: Format string applied to each value.

    Returns:
        None: The formatted value is written to stdout.
    """
    if isinstance(value, list):
        for idx, element in enumerate(value):
            if idx > 0:
                print(" ", end="")
            print(value_format.format(element), end="")
    else:
        print(value_format.format(value), end="")

def common_print_line(mem_access: IMemAccess, addr: int, count: int) -> None:
    """Print one line of memory values.

    Args:
        mem_access: Memory-access implementation used to read values.
        addr: Starting address of the line.
        count: Number of values to print.

    Returns:
        None: The formatted line is written to stdout.
    """
    common_print_address(addr)
    print(": ", end="")

    value_width = 2 * mem_access.get_size()
    value_format = "{:0" + str(value_width) + "X}"
    for idx in range(count):
        if idx > 0:
            print(" ", end="")

        offset = idx * mem_access.get_size()
        common_print_value(mem_access.get_value(addr + offset), value_format)

def common_dump_intel_hex(mem_access: IMemAccess, addr: int, count: int, next_line: int = 16) -> Ret:
    """Print memory values as a hexadecimal dump.

    Args:
        mem_access: Memory-access implementation used to read values.
        addr: Starting address of the dump.
        count: Number of values to print.
        next_line: Line width in bytes, or zero to print all values on one line.

    Returns:
        Ret: Success status after printing the dump.
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
        if index > 0:
            print("")

        offset = index * next_line
        common_print_line(mem_access, addr + offset, full_line_cnt)

    if last_line_element_cnt > 0:
        if full_lines_cnt > 0:
            print("")
            offset = full_lines_cnt * next_line

        common_print_line(mem_access, addr + offset, last_line_element_cnt)

    return Ret.OK

################################################################################
# Main

################################################################################
