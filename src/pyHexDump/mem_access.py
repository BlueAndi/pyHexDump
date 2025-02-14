"""This module provides the memory access API."""

# MIT License
#
# Copyright (c) 2022 - 2025 Andreas Merkle (web@blue-andi.de)
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
from abc import ABC, abstractmethod
import struct

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

class IMemAccess(ABC):
    """Abstract memory access

    Args:
        ABC (obj): Abstract base class
    """

    @abstractmethod
    def set_binary_data(self, binary_data):
        """Set binary data which to access.

        Args:
            binary_data (IntelHex): Binary data

        Raises:
            NotImplementedError: Subclass implementation is missing.
        """
        raise NotImplementedError("Subclass implementation missing.")

    @abstractmethod
    def _set_endianess(self, is_little_endian):
        """Set endianess of data which to access.

        Args:
            is_little_endian (bool): True for little endian, otherwise big endian.

        Raises:
            NotImplementedError: Subclass implementation is missing.
        """
        raise NotImplementedError("Subclass implementation missing.")

    @abstractmethod
    def get_value(self, addr):
        """Get value from the binary data at the given address.

        Args:
            addr (int): Address of the value

        Raises:
            NotImplementedError: Subclass implementation is missing.

        Returns:
            int: Value
        """
        raise NotImplementedError("Subclass implementation missing.")

    @abstractmethod
    def get_size(self):
        """Get the data type size in byte.

        Raises:
            NotImplementedError: Subclass implementation is missing.

        Returns:
            int: Data type size in byte
        """
        raise NotImplementedError("Subclass implementation missing.")

class MemAccessInteger(IMemAccess):
    """Base class which realizes the abstract memory access interfaces
        for integer values.

    Args:
        IMemAccess (obj): Abstract base class
    """
    def __init__(self, binary_data, bit_width, is_little_endian, is_unsigned):
        super().__init__()
        self._binary_data = binary_data
        self._size_byte = bit_width // 8
        self._is_little_endian = is_little_endian
        self._is_unsigned = is_unsigned

    def set_binary_data(self, binary_data):
        """Set binary data which to access.

        Args:
            binary_data (IntelHex): Binary data
        """
        self._binary_data = binary_data

    def _set_endianess(self, is_little_endian):
        """Set endianess of data which to access.

        Args:
            is_little_endian (bool): True for little endian, otherwise big endian.
        """
        self._is_little_endian = is_little_endian

    def get_value(self, addr):
        """Get value from the binary data at the given address.

        Args:
            addr (int): Address of the value

        Returns:
            int: Value
        """
        value = 0
        if self._is_little_endian is True:
            if self._is_unsigned is True:
                value = self._get_value_uxle(self._binary_data, addr, self._size_byte)
            else:
                value = self._get_value_sxle(self._binary_data, addr, self._size_byte)
        else:
            if self._is_unsigned is True:
                value = self._get_value_uxbe(self._binary_data, addr, self._size_byte)
            else:
                value = self._get_value_sxbe(self._binary_data, addr, self._size_byte)

        return value

    def get_size(self):
        """Get the data type size in byte.

        Returns:
            int: Data type size in byte
        """
        return self._size_byte

    def _get_value_uxle(self, intel_hex, addr, size):
        value = 0

        if intel_hex is not None:
            if size == 1:
                value = intel_hex[addr]
            elif size > 1:
                for offset in range(size - 1, -1, -1):
                    value <<= 8
                    value += intel_hex[addr + offset]

        return value

    def _get_value_uxbe(self, intel_hex, addr, size):
        value = 0

        if intel_hex is not None:
            if size == 1:
                value = intel_hex[addr]
            elif size > 1:
                for offset in range(0, size, 1):
                    value <<= 8
                    value += intel_hex[addr + offset]

        return value

    def _get_value_sxle(self, intel_hex, addr, size):
        value = self._get_value_uxle(intel_hex, addr, size)
        bit_width = size * 8
        if value & (1 << (bit_width - 1)):
            value -= 1 << bit_width

        return value

    def _get_value_sxbe(self, intel_hex, addr, size):
        value = self._get_value_uxbe(intel_hex, addr, size)
        bit_width = size * 8
        if value & (1 << (bit_width - 1)):
            value -= 1 << bit_width

        return value

class MemAccessFloat(IMemAccess):
    """Base class which realizes the abstract memory access interfaces
        for float values.

    Args:
        IMemAccess (obj): Abstract base class
    """
    def __init__(self, binary_data, bit_width, is_little_endian):
        super().__init__()
        self._binary_data = binary_data
        self._size_byte = bit_width // 8
        self._is_little_endian = is_little_endian

    def set_binary_data(self, binary_data):
        """Set binary data which to access.

        Args:
            binary_data (IntelHex): Binary data
        """
        self._binary_data = binary_data

    def _set_endianess(self, is_little_endian):
        """Set endianess of data which to access.

        Args:
            is_little_endian (bool): True for little endian, otherwise big endian.
        """
        self._is_little_endian = is_little_endian

    def get_value(self, addr):
        """Get value from the binary data at the given address.

        Args:
            addr (int): Address of the value

        Returns:
            int: Value
        """
        value = 0
        if self._is_little_endian is True:
            value = self._get_value_uxle(self._binary_data, addr, self._size_byte)
        else:
            value = self._get_value_uxbe(self._binary_data, addr, self._size_byte)

        if self._size_byte == 4:
            value = struct.unpack('!f', value.to_bytes(self._size_byte, byteorder="big"))[0]
        elif self._size_byte == 8:
            value = struct.unpack('!d', value.to_bytes(self._size_byte, byteorder="big"))[0]
        else:
            raise NotImplementedError(f"Unsupported bit width of {self._size_byte * 8} for float")

        return value

    def get_size(self):
        """Get the data type size in byte.

        Returns:
            int: Data type size in byte
        """
        return self._size_byte

    def _get_value_uxle(self, intel_hex, addr, size):
        value = 0

        if intel_hex is not None:
            if size == 1:
                value = intel_hex[addr]
            elif size > 1:
                for offset in range(size - 1, -1, -1):
                    value <<= 8
                    value += intel_hex[addr + offset]

        return value

    def _get_value_uxbe(self, intel_hex, addr, size):
        value = 0

        if intel_hex is not None:
            if size == 1:
                value = intel_hex[addr]
            elif size > 1:
                for offset in range(0, size, 1):
                    value <<= 8
                    value += intel_hex[addr + offset]

        return value

################################################################################
# Functions
################################################################################

def mem_access_get_api_by_data_type(data_type):
    """Get API to access a memory depended on the data type.

    Args:
        data_type (str): Data type

    Returns:
        MemAccess: Memory access API; may be None in case there is no available
    """
    mem_access_lookup = {
        "uint8": MemAccessInteger(None, 8, True, True),
        "int8": MemAccessInteger(None, 8, True, False),
        "uint16le": MemAccessInteger(None, 16, True, True),
        "uint16be": MemAccessInteger(None, 16, False, True),
        "int16le": MemAccessInteger(None, 16, True, False),
        "int16be": MemAccessInteger(None, 16, False, False),
        "uint32le": MemAccessInteger(None, 32, True, True),
        "uint32be": MemAccessInteger(None, 32, False, True),
        "int32le": MemAccessInteger(None, 32, True, False),
        "int32be": MemAccessInteger(None, 32, False, False),
        "uint64le": MemAccessInteger(None, 64, True, True),
        "uint64be": MemAccessInteger(None, 64, False, True),
        "int64le": MemAccessInteger(None, 64, True, False),
        "int64be": MemAccessInteger(None, 64, False, False),
        "float32le": MemAccessFloat(None, 32, True),
        "float32be": MemAccessFloat(None, 32, False),
        "float64le": MemAccessFloat(None, 64, True),
        "float64be": MemAccessFloat(None, 64, False),
        "utf8": MemAccessInteger(None, 8, True, True)
    }

    return mem_access_lookup.get(data_type, None)

################################################################################
# Main
################################################################################
