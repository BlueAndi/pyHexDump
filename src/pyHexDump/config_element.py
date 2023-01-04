"""Configuration element
"""

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
from pyHexDump.mem_access import mem_access_get_api_by_data_type

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

class ConfigElement:
    """Represents a single element in the configuration.
    """
    def __init__(self, name, addr, data_type, count) -> None:
        self._name = name
        self._addr = addr
        self._mem_access = mem_access_get_api_by_data_type(data_type)
        self._count = count

    def get_name(self):
        """Get the configuration element name.

        Returns:
            str: Configuration element name
        """
        return self._name

    def get_addr(self):
        """Get the configuration element address.

        Returns:
            int: Configuration element address
        """
        return self._addr

    def get_count(self):
        """Get the configuration element count.
            A count of 1 means its just one value.
            Greater than 1 for a array of values.

        Returns:
            int: Configuration element count
        """
        return self._count

    def get_mem_access(self):
        """Get the memory access API.

        Returns:
            MemAccess: Memory access API
        """
        return self._mem_access

    def set_intel_hex(self, intel_hex):
        """Set the intel hex ...

        Args:
            intel_hex (_type_): _description_
        """
        if self._mem_access is not None:
            self._mem_access.set_binary_data(intel_hex)

    def get_value(self):
        """Get the configuration element value.
            If the count is 1, only a single value will be returned.
            If the count is greater than 1, a list of values will be returned.

        Returns:
            int, list: Configuration element value
        """
        value = 0

        if self._mem_access is None:
            return 0

        if self._count == 1:
            value = self._mem_access.get_value(self._addr)
        elif self._count > 1:
            value = []
            for idx in range(self._count):
                offset = idx * self._mem_access.get_size()
                value.append(self._mem_access.get_value(self._addr + offset))
        else:
            value = 0

        return value

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
