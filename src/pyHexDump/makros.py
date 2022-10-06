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
import ctypes
################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def makros_compare_values(set_value, actual_value, value_format="{:02X}"):
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
    else:
        return f"Not Ok (Set: {value_format.format(set_value)}, " \
              f"Actual: {value_format.format(actual_value)})"

def convert_middle_to_little_endian(value):
    """Converts the value from middle to little endian representation.
        The value 0xCCDDAABB should be represented as 0xAABBCCDD
    
        Args:
            value(int): Value in middle endian representation
            
        Retruns:
            Value in little endian representation
    """
    solution = ctypes.c_uint32(0)

    tmp = ctypes.c_uint32(0)
    # Shift CCDD to the right position
    tmp.value = value << 16
    solution.value = solution.value | tmp.value

    # Shift AABB to the right position
    tmp.value = 0
    tmp.value = value >> 16
    solution.value = solution.value | tmp.value

    return solution.value

################################################################################
# Main
################################################################################
