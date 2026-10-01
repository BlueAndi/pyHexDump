"""This module contains functions used for generating the report."""

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
from typing import Callable
from intelhex import IntelHex

from pyHexDump.mem_access import mem_access_get_api_by_data_type
from pyHexDump.cmd_checksum import calc_checksum

################################################################################
# Variables
################################################################################

BINARY_DATA: IntelHex | None = None

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def _compare_values(set_value: int | float, actual_value: int | float,
                    value_format: str = "{:02X}") -> str:
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

def _u16_swap_bytes(u16_value: int) -> int:
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

def _u32_swap_bytes(u32_value: int) -> int:
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

def _u32_swap_words(u32_value: int) -> int:
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

def _read(addr: int, data_type: str) -> int | float:
    """Read a typed value from the current binary data.

    Args:
        addr: Address of the value.
        data_type: Supported memory data type name.

    Returns:
        Decoded integer or floating-point value.
    """
    mem_access = mem_access_get_api_by_data_type(data_type)
    binary_data = globals()["BINARY_DATA"]
    mem_access.set_binary_data(binary_data)
    return mem_access.get_value(addr)

def _read_u8(addr: int) -> int:
    """Read an unsigned 8-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded unsigned integer.
    """
    return _read(addr, "uint8")

def _read_u16le(addr: int) -> int:
    """Read an unsigned little-endian 16-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded unsigned integer.
    """
    return _read(addr, "uint16le")

def _read_u16be(addr: int) -> int:
    """Read an unsigned big-endian 16-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded unsigned integer.
    """
    return _read(addr, "uint16be")

def _read_u32le(addr: int) -> int:
    """Read an unsigned little-endian 32-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded unsigned integer.
    """
    return _read(addr, "uint32le")

def _read_u32be(addr: int) -> int:
    """Read an unsigned big-endian 32-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded unsigned integer.
    """
    return _read(addr, "uint32be")

def _read_u64le(addr: int) -> int:
    """Read an unsigned little-endian 64-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded unsigned integer.
    """
    return _read(addr, "uint64le")

def _read_u64be(addr: int) -> int:
    """Read an unsigned big-endian 64-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded unsigned integer.
    """
    return _read(addr, "uint64be")

def _read_s8(addr: int) -> int:
    """Read a signed 8-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded signed integer.
    """
    return _read(addr, "int8")

def _read_s16le(addr: int) -> int:
    """Read a signed little-endian 16-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded signed integer.
    """
    return _read(addr, "int16le")

def _read_s16be(addr: int) -> int:
    """Read a signed big-endian 16-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded signed integer.
    """
    return _read(addr, "int16be")

def _read_s32le(addr: int) -> int:
    """Read a signed little-endian 32-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded signed integer.
    """
    return _read(addr, "int32le")

def _read_s32be(addr: int) -> int:
    """Read a signed big-endian 32-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded signed integer.
    """
    return _read(addr, "int32be")

def _read_s64le(addr: int) -> int:
    """Read a signed little-endian 64-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded signed integer.
    """
    return _read(addr, "int64le")

def _read_s64be(addr: int) -> int:
    """Read a signed big-endian 64-bit value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded signed integer.
    """
    return _read(addr, "int64be")

def _read_float32le(addr: int) -> float:
    """Read a little-endian 32-bit floating-point value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded floating-point value.
    """
    return _read(addr, "float32le")

def _read_float32be(addr: int) -> float:
    """Read a big-endian 32-bit floating-point value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded floating-point value.
    """
    return _read(addr, "float32be")

def _read_float64le(addr: int) -> float:
    """Read a little-endian 64-bit floating-point value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded floating-point value.
    """
    return _read(addr, "float64le")

def _read_float64be(addr: int) -> float:
    """Read a big-endian 64-bit floating-point value.

    Args:
        addr: Address of the value.

    Returns:
        Decoded floating-point value.
    """
    return _read(addr, "float64be")

def _read_string(addr: int, encoding: str = "utf-8", max_length: int = 256) -> str:
    """Read and decode a NUL-terminated byte string.

    Args:
        addr: Address of the first byte.
        encoding: Codec used to decode the bytes.
        max_length: Maximum number of bytes to inspect.

    Returns:
        Decoded string ending at the first NUL byte.
    """
    value_list = []
    for idx in range(max_length):
        value = _read_u8(addr + idx)
        if value == 0:
            byte_values = bytearray(value_list)
            return byte_values.decode(encoding)
        value_list.append(value)

    raise ValueError(f"String at address {addr:#x} is not terminated within {max_length} bytes.")

# pylint: disable=too-many-arguments
def _calc_checksum(
    binary_data_endianess: str,
    start_address: int,
    end_address: int,
    polynomial: int,
    bit_width: int,
    seed: int,
    reverse_input: bool,
    reverse_output: bool,
    final_xor: bool,
) -> int:
    """Calculate a checksum over the current binary data.

    Args:
        binary_data_endianess: Data type and byte order used to read input.
        start_address: First address included in the checksum.
        end_address: End address excluded from the checksum.
        polynomial: CRC generator polynomial.
        bit_width: Number of bits in the CRC value.
        seed: Initial CRC value.
        reverse_input: Whether to reflect input bytes.
        reverse_output: Whether to reflect the final CRC value.
        final_xor: Whether to XOR the result with the width mask.

    Returns:
        Calculated checksum value.
    """

    binary_data = globals()["BINARY_DATA"]
    # pylint: disable=too-many-function-args
    checksum = calc_checksum(binary_data, binary_data_endianess, start_address, end_address, \
                             polynomial, bit_width, seed, reverse_input, reverse_output, \
                             final_xor)

    return checksum

def set_binary_data(binary_data: IntelHex | None) -> None:
    """Set the binary data to be used by all macros. This avoids to spawn the binary data
        access into the template.

    Args:
        binary_data (IntelHex): Binary data

    Returns:
        None: Sets the data read by the template macros.
    """
    globals()["BINARY_DATA"] = binary_data

def get_macro_dict() -> dict[str, Callable[..., object]]:
    """Get the macro dictionary. The macros will be supported inside the template
        and can be used there.

    Returns:
        dict[str, Callable[..., object]]: Names mapped to template macro functions.
    """
    macro_dict = {}

    macro_dict["macros_compare_values"] = _compare_values

    macro_dict["m_read_uint8"] = _read_u8
    macro_dict["m_read_uint16le"] = _read_u16le
    macro_dict["m_read_uint16be"] = _read_u16be
    macro_dict["m_read_uint32le"] = _read_u32le
    macro_dict["m_read_uint32be"] = _read_u32be
    macro_dict["m_read_uint64le"] = _read_u64le
    macro_dict["m_read_uint64be"] = _read_u64be

    macro_dict["m_read_int8"] = _read_s8
    macro_dict["m_read_int16le"] = _read_s16le
    macro_dict["m_read_int16be"] = _read_s16be
    macro_dict["m_read_int32le"] = _read_s32le
    macro_dict["m_read_int32be"] = _read_s32be
    macro_dict["m_read_int64le"] = _read_s64le
    macro_dict["m_read_int64be"] = _read_s64be

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
