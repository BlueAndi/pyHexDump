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

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

class ConfigElement:
    """Represents a single element in the configuration.
    """
    def __init__(self, name, addr, data_type, count):
        self._name = name
        self._addr = addr
        self._data_type = data_type
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

    def get_datatype(self):
        """Get the configuration element datatype.

        Returns:
            str: Data type
        """
        return self._data_type

    def get_count(self):
        """Get the configuration element count.
            A count of 1 means its just one value.
            Greater than 1 for a array of values.

        Returns:
            int: Configuration element count
        """
        return self._count

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
