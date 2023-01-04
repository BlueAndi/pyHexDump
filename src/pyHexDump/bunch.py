"""Bunch
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

class Bunch(dict):
    """Bunch is a dictionary that supports attribute-style access, a la JavaScript.
        A dictionary must be accessed via myDict["test"].
        A bunch can access the same with myDict.test.
    """
    def __init__(self, dict_of_items):
        dict.__init__(self, dict_of_items)
        self.__dict__.update(dict_of_items)

################################################################################
# Functions
################################################################################

def dict_to_bunch(dict_of_items):
    """Convert a dictionary to a bunch.

    Args:
        dict_of_items (dict): Dictionary of items

    Returns:
        Bunch: Bunch of items
    """
    bunch_of_items = {}

    for key, value in dict_of_items.items():
        if isinstance(value, dict):
            value = dict_to_bunch(value)

        bunch_of_items[key] = value

    return Bunch(bunch_of_items)

################################################################################
# Main
################################################################################
