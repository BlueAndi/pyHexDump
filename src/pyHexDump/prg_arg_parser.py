"""This module contains the program argument parser and its configuration."""

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
import argparse
from pyHexDump.version import __version__, __author__, __email__, __repository__, __license__

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

class PrgArgParser():
    """Parses all program arguments according to its configuration.
    """

    def __init__(self) -> None:
        """Configure parser and parse program arguments.

        Returns:
            None: Initializes the parser state.
        """
        self._parser = self._create_main_parser()
        self._sub_parsers =  self._parser.add_subparsers(dest="cmd")
        self._args = None

    def _create_main_parser(self) -> argparse.ArgumentParser:
        """Create the parser shared by all CLI commands.

        Returns:
            argparse.ArgumentParser: Configured top-level parser.
        """
        main_parser = argparse.ArgumentParser( \
            description="Binary files in different formats can be analyzed by\
            specifying a memory map configuration or just dump some data to\
            the console.",
            epilog="Copyright (c) 2022 - 2026 " + __author__ + " - " + __license__ + \
            " - Find the project on github: " + __repository__)
        main_parser.set_defaults(which="")

        main_parser.add_argument(
            "--version",
            action="version",
            version="%(prog)s " + __version__)

        main_parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            required=False,
            default=False,
            help="Prints more additional information."
        )

        return main_parser

    def parse_args(self) -> None:
        """Parse the program arguments.

        Returns:
            None: Stores parsed arguments on this parser instance.
        """
        self._args = self._parser.parse_args()

    def get_sub_parsers(self) -> argparse._SubParsersAction:
        """Get the sub parsers to be able to add additional command specific parsers.

        Returns:
            obj: Argument sub parsers
        """
        return self._sub_parsers

    def print_help(self) -> None:
        """Print the help information.

        Returns:
            None: Writes help text to stdout.
        """
        self._parser.print_help()

    def get_args(self) -> argparse.Namespace | None:
        """Get parsed arguments.

        Returns:
            argparse.Namespace or None: Parsed arguments, if parsing has run.
        """
        return self._args

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
