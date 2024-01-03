"""Template element
"""

# MIT License
#
# Copyright (c) 2022 - 2024 Andreas Merkle (web@blue-andi.de)
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
import struct
import math

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

class BaseTemplateElement():
    """Base template element

    Args:
        ABC (obj): Abstract base class
    """
    def __init__(self, name, addr):
        super().__init__()
        self._name = name
        self._addr = addr

    def name(self):
        """Get name of the element.

        Returns:
            str: Element name
        """
        return self._name

    def addr(self):
        """Get the address of the element in the binary data.

        Returns:
            int: Address
        """
        return self._addr

class TmplElementInt(BaseTemplateElement):
    """Template element representing a single integer element with a address, value and bit width.
    """
    def __init__(self, name, addr, value, bit_width):
        super().__init__(name, addr)
        self._value = value
        self._bit_width = bit_width

    def __bool__(self):
        return bool(self._value)

    def __int__(self):
        return self._value

    def __float__(self):
        return float(self._value)

    def __str__(self):
        return str(self._value)

    def __add__(self, value):
        return self._value + value

    def __sub__(self, value):
        return self._value - value

    def __mul__(self, value):
        return self._value * value

    def __pow__(self, value):
        return self._value ** value

    def __truediv__(self, value):
        return self._value / value

    def __floordiv__(self, value):
        return self._value // value

    def __mod__(self, value):
        return self._value % value

    def __lshift__(self, value):
        return self._value << value

    def __rshift__(self, value):
        return self._value >> value

    def __and__(self, value):
        return self._value & value

    def __or__(self, value):
        return self._value | value

    def __xor__(self, value):
        return self._value ^ value

    def __divmod__(self, value):
        return (self._value // value, self._value % value)

    def __lt__(self, value):
        return self._value < value

    def __le__(self, value):
        return self._value <= value

    def __eq__(self, value):
        return self._value == value

    def __ne__(self, value):
        return self._value != value

    def __gt__(self, value):
        return self._value > value

    def __ge__(self, value):
        return self._value >= value

    def __abs__(self):
        return abs(self._value)

    def __invert__(self):
        return ~self._value

    def __ceil__(self):
        return math.ceil(self._value)

    def __floor__(self):
        return math.floor(self._value)

    def _value_to_hex(self, value, prefix):
        if value < 0:
            value &= (1 << self._bit_width) - 1

        return f"{prefix}{value:0{self._bit_width // 4}X}"

    def hex(self, prefix="0x"):
        """Get the value in hex format.

        Args:
            prefix (str, optional): Prefix. Defaults to "0x".

        Returns:
            str: Hex value
        """
        return self._value_to_hex(self._value, prefix)

class TmplElementIntList(BaseTemplateElement):
    """Template element representing a list of integer elements with a address, value and bit width.
    """
    def __init__(self, name, addr, value, bit_width):
        super().__init__(name, addr)
        self._value = value
        self._bit_width = bit_width

    def __str__(self):
        return str(self._value)

    def __add__(self, value):
        return self._value + value

    def __mul__(self, value):
        return self._value * value

    def __lt__(self, value):
        return self._value < value

    def __le__(self, value):
        return self._value <= value

    def __eq__(self, value):
        return self._value == value

    def __ne__(self, value):
        return self._value != value

    def __gt__(self, value):
        return self._value > value

    def __ge__(self, value):
        return self._value >= value

    def __getitem__(self, key):
        return self._value[key]

    def _value_to_hex(self, value, prefix):
        if value < 0:
            value &= (1 << self._bit_width) - 1

        return f"{prefix}{value:0{self._bit_width // 4}X}"

    def hex(self, prefix="0x"):
        """Get the value in hex format.

        Args:
            prefix (str, optional): Prefix. Defaults to "0x".

        Returns:
            str: Hex value
        """
        output = "["

        for idx, value in enumerate(self._value):

            if idx > 0:
                output += ", "

            output += self._value_to_hex(value, prefix)

        output += "]"

        return output

class TmplElementFloat(BaseTemplateElement):
    """Template element representing a single float element with a address, value and bit width.
    """
    def __init__(self, name, addr, value, bit_width):
        super().__init__(name, addr)
        self._value = value
        self._bit_width = bit_width

    def __bool__(self):
        return bool(self._value)

    def __int__(self):
        return int(self._value)

    def __float__(self):
        return self._value

    def __str__(self):
        return str(self._value)

    def __add__(self, value):
        return self._value + value

    def __sub__(self, value):
        return self._value - value

    def __mul__(self, value):
        return self._value * value

    def __pow__(self, value):
        return self._value ** value

    def __truediv__(self, value):
        return self._value / value

    def __floordiv__(self, value):
        return self._value // value

    def __mod__(self, value):
        return self._value % value

    def __divmod__(self, value):
        return (self._value // value, self._value % value)

    def __lt__(self, value):
        return self._value < value

    def __le__(self, value):
        return self._value <= value

    def __eq__(self, value):
        return self._value == value

    def __ne__(self, value):
        return self._value != value

    def __gt__(self, value):
        return self._value > value

    def __ge__(self, value):
        return self._value >= value

    def __abs__(self):
        return abs(self._value)

    def __ceil__(self):
        return math.ceil(self._value)

    def __floor__(self):
        return math.floor(self._value)

    def _value_to_hex(self, value, prefix):
        if self._bit_width == 32:
            value = struct.unpack('<I', struct.pack('<f', value))[0]
        elif self._bit_width == 64:
            value = struct.unpack('<Q', struct.pack('<d', value))[0]
        else:
            raise NotImplementedError(f"Unsupported bit width of {self._bit_width} for float")

        return f"{prefix}{value:0{self._bit_width // 4}X}"

    def hex(self, prefix="0x"):
        """Get the value in hex format.

        Args:
            prefix (str, optional): Prefix. Defaults to "0x".

        Returns:
            str: Hex value
        """
        return self._value_to_hex(self._value, prefix)

class TmplElementFloatList(BaseTemplateElement):
    """Template element representing a list of float elements with a address, value and bit width.
    """
    def __init__(self, name, addr, value, bit_width):
        super().__init__(name, addr)
        self._value = value
        self._bit_width = bit_width

    def __str__(self):
        return str(self._value)

    def __add__(self, value):
        return self._value + value

    def __mul__(self, value):
        return self._value * value

    def __lt__(self, value):
        return self._value < value

    def __le__(self, value):
        return self._value <= value

    def __eq__(self, value):
        return self._value == value

    def __ne__(self, value):
        return self._value != value

    def __gt__(self, value):
        return self._value > value

    def __ge__(self, value):
        return self._value >= value

    def __getitem__(self, key):
        return self._value[key]

    def _value_to_hex(self, value, prefix):
        if self._bit_width == 32:
            value = struct.unpack('<I', struct.pack('<f', value))[0]
        elif self._bit_width == 64:
            value = struct.unpack('<Q', struct.pack('<d', value))[0]
        else:
            raise NotImplementedError(f"Unsupported bit width of {self._bit_width} for float")

        return f"{prefix}{value:0{self._bit_width // 4}X}"

    def hex(self, prefix="0x"):
        """Get the value in hex format.

        Args:
            prefix (str, optional): Prefix. Defaults to "0x".

        Returns:
            str: Hex value
        """
        output = "["

        for idx, value in enumerate(self._value):

            if idx > 0:
                output += ", "

            output += self._value_to_hex(value, prefix)

        output += "]"

        return output

class TmplElementStr(BaseTemplateElement):
    """Template element representing a single integer element with a address, value and bit width.
    """
    def __init__(self, name, addr, value, bit_width):
        super().__init__(name, addr)
        self._value = value
        self._bit_width = bit_width

    def __int__(self):
        return int(self._value)

    def __str__(self):
        return self._value

    def __add__(self, value):
        return self._value + value

    def __mul__(self, value):
        return self._value * value

    def __mod__(self, value):
        return self._value % value

    def __lt__(self, value):
        return self._value < value

    def __le__(self, value):
        return self._value <= value

    def __eq__(self, value):
        return self._value == value

    def __ne__(self, value):
        return self._value != value

    def __gt__(self, value):
        return self._value > value

    def __ge__(self, value):
        return self._value >= value

    def __getitem__(self, key):
        return self._value[key]

    def _value_to_hex(self, value, prefix):
        if value < 0:
            value &= (1 << self._bit_width) - 1

        return f"{prefix}{value:0{self._bit_width // 4}X}"

    def hex(self, prefix="0x"):
        """Get the value in hex format.

        Args:
            prefix (str, optional): Prefix. Defaults to "0x".

        Returns:
            str: Hex value
        """
        output = "["

        for idx, value in enumerate(self._value):

            if idx > 0:
                output += ", "

            output += self._value_to_hex(ord(value), prefix)

        output += "]"

        return output

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
