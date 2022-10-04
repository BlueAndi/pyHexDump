"""This module provides the memory access API."""

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
from abc import ABC, abstractmethod

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

class MemAccess(ABC):
    """Abstract memory access

    Args:
        ABC (obj): Abstract base class
    """

    @abstractmethod
    def get_value(self, intel_hex, addr):
        """Get value from the intel hex object at the given address.

        Args:
            intel_hex (obj): Intel hex object
            addr (int): Address of the value

        Returns:
            int: Value
        """
        raise NotImplementedError("Subclass implementation missing.")

    @abstractmethod
    def get_size(self):
        """Get the data type size in byte.

        Returns:
            int: Data type size in byte
        """
        raise NotImplementedError("Subclass implementation missing.")

    def _get_value_uxle(self, intel_hex, addr, size):
        value = 0

        if size == 1:
            value = intel_hex[addr]
        elif size > 1:
            for offset in range(size - 1, -1, -1):
                value <<= 8
                value += intel_hex[addr + offset]

        return value

    def _get_value_uxbe(self, intel_hex, addr, size):
        value = 0

        if size == 1:
            value = intel_hex[addr]
        elif size > 1:
            for offset in range(0, size, 1):
                value <<= 8
                value += intel_hex[addr + offset]

        return value

class MemAccessU8(MemAccess):
    """Unsigned 8 bit element.

    Args:
        MemAccess (obj): Parent class
    """

    def get_value(self, intel_hex, addr):
        """Get value from the intel hex object at the given address.

        Args:
            intel_hex (obj): Intel hex object
            addr (int): Address of the value

        Returns:
            int: Value
        """
        return self._get_value_uxle(intel_hex, addr, self.get_size())

    def get_size(self):
        """Get the data type size in byte.

        Returns:
            int: Data type size in byte
        """
        return 1

class MemAccessU16LE(MemAccess):
    """Unsigned 16 bit little endian element.

    Args:
        MemAccess (obj): Parent class
    """

    def get_value(self, intel_hex, addr):
        """Get value from the intel hex object at the given address.

        Args:
            intel_hex (obj): Intel hex object
            address (int): Address of the value

        Returns:
            int: Value
        """
        return self._get_value_uxle(intel_hex, addr, self.get_size())

    def get_size(self):
        """Get the data type size in byte.

        Returns:
            int: Data type size in byte
        """
        return 2

class MemAccessU16BE(MemAccess):
    """Unsigned 16 bit big endian element.

    Args:
        MemAccess (obj): Parent class
    """

    def get_value(self, intel_hex, addr):
        """Get value from the intel hex object at the given address.

        Args:
            intel_hex (obj): Intel hex object
            address (int): Address of the value

        Returns:
            int: Value
        """
        return self._get_value_uxbe(intel_hex, addr, self.get_size())

    def get_size(self):
        """Get the data type size in byte.

        Returns:
            int: Data type size in byte
        """
        return 2

class MemAccessU32LE(MemAccess):
    """Unsigned 32 bit little endian element.

    Args:
        MemAccess (obj): Parent class
    """

    def get_value(self, intel_hex, addr):
        """Get value from the intel hex object at the given address.

        Args:
            intel_hex (obj): Intel hex object
            address (int): Address of the value

        Returns:
            int: Value
        """
        return self._get_value_uxle(intel_hex, addr, self.get_size())

    def get_size(self):
        """Get the data type size in byte.

        Returns:
            int: Data type size in byte
        """
        return 4

class MemAccessU32BE(MemAccess):
    """Unsigned 32 bit big endian element.

    Args:
        MemAccess (obj): Parent class
    """

    def get_value(self, intel_hex, addr):
        """Get value from the intel hex object at the given address.

        Args:
            intel_hex (obj): Intel hex object
            address (int): Address of the value

        Returns:
            int: Value
        """
        return self._get_value_uxbe(intel_hex, addr, self.get_size())

    def get_size(self):
        """Get the data type size in byte.

        Returns:
            int: Data type size in byte
        """
        return 4

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
    mem_access = None

    if data_type == "u8":
        mem_access = MemAccessU8()
    elif data_type == "u16le":
        mem_access = MemAccessU16LE()
    elif data_type == "u16be":
        mem_access = MemAccessU16BE()
    elif data_type == "u32le":
        mem_access = MemAccessU32LE()
    elif data_type == "u32be":
        mem_access = MemAccessU32BE()

    return mem_access

################################################################################
# Main
################################################################################
