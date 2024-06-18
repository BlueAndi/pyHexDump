"""This module provides version and author information."""

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
import importlib.metadata as meta
import os
import sys
import toml

################################################################################
# Variables
################################################################################

__version__ = "???"
__author__ = "???"
__email__ = "???"
__repository__ = "???"
__license__ = "???"

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # pylint: disable=protected-access
        # pylint: disable=no-member
        base_path = sys._MEIPASS
    except Exception:  # pylint: disable=broad-except
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def init_from_metadata():
    """Initialize dunders from importlib.metadata
    Requires that the package was installed.

    Returns:
        list: Tool related informations
    """

    my_metadata = meta.metadata('pyHexDump')

    return \
        my_metadata['Version'],\
        my_metadata['Author'],\
        my_metadata['Author-email'],\
        my_metadata['Project-URL'].replace("repository, ", ""),\
        my_metadata['License']

def init_from_toml():
    """Initialize dunders from pypackage.toml file

    Tried if package wasn't installed.

    Returns:
        list: Tool related informations
    """

    toml_file = resource_path("pyproject.toml")
    data = toml.load(toml_file)

    return \
        data["project"]["version"],\
        data["project"]["authors"][0]["name"],\
        data["project"]["authors"][0]["email"],\
        data["project"]["urls"]["repository"],\
        data["project"]["license"]["text"]

################################################################################
# Main
################################################################################

try:
    __version__, __author__, __email__, __repository__, __license__ = init_from_metadata()

except meta.PackageNotFoundError:
    __version__, __author__, __email__, __repository__, __license__ = init_from_toml()
