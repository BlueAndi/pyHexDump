"""Configuration element
"""

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
from pyHexDump.mem_access import mem_access_get_api_by_data_type

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

# pylint: disable=too-few-public-methods
class ConfigElement:
    """Represents a single element in the configuration.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, name, addr, data_type, count, elements = None):
        """
        Initialize the configuration element.

        Args:
            name (str): _description_
            addr (int): _description_
            data_type (str): _description_
            count (int): _description_
            elements (list, optional): List of configuration elements. Defaults to None.
        """
        self.name = name
        self.addr = addr
        self.data_type = data_type
        self.count = count
        self.elements = elements

    @property
    def size(self):
        """Get the size of the configuration element.

        Returns:
            int: Size of the configuration element in bytes.
        """
        size = 0

        if self.elements is None:
            mem_access = mem_access_get_api_by_data_type(self.data_type)
            assert mem_access is not None, f"Unsupported data type: {self.data_type}"

            size = mem_access.get_size()

        else:
            for _, config_element in self.elements.items():
                size += config_element.size

        size *= self.count

        return size

class PaddingElement(ConfigElement):
    """
    Padding element. Its used to fill up the gap between two other elements.
    A gap can be necessary in case of a specific alignment is required.
    """

    def __init__(self, size):
        """
        Initialize the padding element.

        Args:
            size (int): Size of the padding element in bytes.
        """
        super().__init__("padding", 0, "uint8", 0)
        self._size = size

    @property
    def size(self):
        """Get the size of the padding element.

        Returns:
            int: Size of the padding element in bytes.
        """
        return self._size

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
