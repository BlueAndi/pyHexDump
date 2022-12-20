"""This module contains functions used for generating the report."""

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
from pyHexDump.mem_access import mem_access_get_api_by_data_type
from pyHexDump.cmd_checksum import calc_checksum

################################################################################
# Variables
################################################################################

BINARY_DATA = None

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def _compare_values(set_value, actual_value, value_format="{:02X}"):
    """Compares the set_value and the actual_value.

        Args:
            set_value(int): Set value
            actual_value(int): Actual value
            value_format (str, optional): The output format. Defaults to "{:02X}".

        Returns:
            "Not Ok (Set: <set_value>, Actual: <actual_value>)" if the set_value
            differs from the actual_value. Otherwise "Ok".
    """
    if set_value == actual_value:
        return "Ok"

    return f"Not Ok (Set: {value_format.format(set_value)}, " \
              f"Actual: {value_format.format(actual_value)})"

def _u16_swap_bytes(u16_value):
    """Swap the bytes of unsigned 16-bit value.
        Used for conversion between little and big endian.

    Args:
        u16_value (int): Source

    Returns:
        int: Destination
    """
    result  = (u16_value & 0x00FF) << 8
    result |= (u16_value & 0xFF00) >> 8
    return result

def _u32_swap_bytes(u32_value):
    """Swap the bytes of unsigned 32-bit value.
        Used for conversion between little and big endian.

    Args:
        u32_value (int): Source

    Returns:
        int: Destination
    """
    result  = (u32_value & 0x000000FF) << 24
    result |= (u32_value & 0x0000FF00) << 8
    result |= (u32_value & 0x00FF0000) >> 8
    result |= (u32_value & 0xFF000000) >> 24
    return result

def _u32_swap_words(u32_value):
    """Swap the 16-bit words of unsigned 16-bit value.
        Used for conversion between little and middle endian.
        For big endian to middle endian conversion, convert it first to little endian
        and after it call this macro.

    Args:
        u32_value (int): Source

    Returns:
        int: Destination
    """
    result  = (u32_value & 0x0000FFFF) << 16
    result |= (u32_value & 0xFFFF0000) >> 16
    return result

def _read(addr, data_type):
    mem_access = mem_access_get_api_by_data_type(data_type)
    binary_data = globals()["BINARY_DATA"]
    mem_access.set_binary_data(binary_data)
    return mem_access.get_value(addr)

def _read_u8(addr):
    return _read(addr, "u8")

def _read_u16le(addr):
    return _read(addr, "u16le")

def _read_u16be(addr):
    return _read(addr, "u16be")

def _read_u32le(addr):
    return _read(addr, "u32le")

def _read_u32be(addr):
    return _read(addr, "u32be")

def _read_u64le(addr):
    return _read(addr, "u64le")

def _read_u64be(addr):
    return _read(addr, "u64be")

def _read_s8(addr):
    return _read(addr, "s8")

def _read_s16le(addr):
    return _read(addr, "s16le")

def _read_s16be(addr):
    return _read(addr, "s16be")

def _read_s32le(addr):
    return _read(addr, "s32le")

def _read_s32be(addr):
    return _read(addr, "s32be")

def _read_s64le(addr):
    return _read(addr, "s64le")

def _read_s64be(addr):
    return _read(addr, "s64be")

def _read_float32le(addr):
    return _read(addr, "float32le")

def _read_float32be(addr):
    return _read(addr, "float32be")

def _read_float64le(addr):
    return _read(addr, "float64le")

def _read_float64be(addr):
    return _read(addr, "float64be")

def _read_string(addr, encoding="utf-8"):
    value_list = []
    idx = 0
    while True:
        value = _read_u8(addr + idx)
        if value == 0:
            break
        value_list.append(value)
        idx += 1

    byte_values = bytearray(value_list)

    return byte_values.decode(encoding)

# pylint: disable-next=too-many-arguments
def _calc_checksum(binary_data_endianess, start_address, end_address, polynomial, bit_width, seed, \
    reverse_input, reverse_output, final_xor):

    binary_data = globals()["BINARY_DATA"]
    # pylint: disable-next=too-many-function-args
    checksum = calc_checksum(binary_data, binary_data_endianess, start_address, end_address, \
                             polynomial, bit_width, seed, reverse_input, reverse_output, \
                             final_xor)

    return checksum

def set_binary_data(binary_data):
    """Set the binary data to be used by all macros. This avoids to spawn the binary data
        access into the template.

    Args:
        binary_data (IntelHex): Binary data
    """
    globals()["BINARY_DATA"] = binary_data

def get_macro_dict():
    """Get the macro dictionary. The macros will be supported inside the template
        and can be used there.

    Returns:
        dict: Macro dictionary
    """
    macro_dict = {}

    macro_dict["macros_compare_values"] = _compare_values

    macro_dict["m_read_u8"] = _read_u8
    macro_dict["m_read_u16le"] = _read_u16le
    macro_dict["m_read_u16be"] = _read_u16be
    macro_dict["m_read_u32le"] = _read_u32le
    macro_dict["m_read_u32be"] = _read_u32be
    macro_dict["m_read_u64le"] = _read_u64le
    macro_dict["m_read_u64be"] = _read_u64be

    macro_dict["m_read_s8"] = _read_s8
    macro_dict["m_read_s16le"] = _read_s16le
    macro_dict["m_read_s16be"] = _read_s16be
    macro_dict["m_read_s32le"] = _read_s32le
    macro_dict["m_read_s32be"] = _read_s32be
    macro_dict["m_read_s64le"] = _read_s64le
    macro_dict["m_read_s64be"] = _read_s64be

    macro_dict["m_read_float32le"] = _read_float32le
    macro_dict["m_read_float32be"] = _read_float32be
    macro_dict["m_read_float64le"] = _read_float64le
    macro_dict["m_read_float64be"] = _read_float64be

    macro_dict["m_read_string"] = _read_string

    macro_dict["m_calc_checksum"] = _calc_checksum

    macro_dict["m_swap_bytes_u16"] = _u16_swap_bytes # Used for LE/BE conversion
    macro_dict["m_swap_bytes_u32"] = _u32_swap_bytes # Used for LE/BE conversion
    macro_dict["m_swap_words_u32"] = _u32_swap_words # Used for LE/ME conversion

    return macro_dict

################################################################################
# Main
################################################################################
