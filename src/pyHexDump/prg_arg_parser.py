"""This module contains the program argument parser and its configuration."""

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
import argparse
from pyHexDump.version import __version__

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

class PrgArgParser():
    """Parses all program arguments according to its configuration.
    """

    def __init__(self):
        """Configure parser and parse program arguments.
        """
        self._parser = self._create_parser()
        self._args = self._parser.parse_args()

    def _create_parser(self):
        main_parser = self._create_main_parser()

        # Every command has its own sub parser
        sub_parsers = main_parser.add_subparsers(dest="cmd")
        self._create_dump_sub_parser(sub_parsers)
        self._create_print_sub_parser(sub_parsers)
        self._create_checksum_sub_parser(sub_parsers)

        return main_parser

    def _create_main_parser(self):
        main_parser = argparse.ArgumentParser(description="Binary files in different \
            formats can be analyzed by specifying a memory map configuration.")
        main_parser.set_defaults(which="")

        main_parser.add_argument(
            "--version",
            action="version",
            version="%(prog)s " + __version__)

        return main_parser

    def _create_dump_sub_parser(self, sub_parsers):
        parser = sub_parsers.add_parser(
            "dump",
            help="Dump a range of data from a start address."
        )

        parser.add_argument(
            "binaryFile",
            metavar="BINARY_FILE",
            type=str,
            nargs=1,
            help="Binary file in intel hex format (.hex) or binary (.bin)."
        )
        parser.add_argument(
            "-a",
            "--addr",
            metavar="ADDR",
            type=lambda x: int(x, 0), # Support "0x" notation
            nargs="?", # Optional
            default=0,
            help="The dump starts at this address. Default: 0x00000000."
        )
        parser.add_argument(
            "-c",
            "--count",
            metavar="COUNT",
            type=lambda x: int(x, 0), # Support "0x" notation
            nargs="?", # Optional
            default=64,
            help="The number of elements in the dump.\nDefault: 16"
        )
        parser.add_argument(
            "-dt",
            "--dataType",
            metavar="DATA_TYPE",
            type=str,
            nargs="?", # Optional
            default="u8",
            help="The type of a single data element (u8, u16le, u16be, u32le, u32be). Default: u8"
        )

    def _create_print_sub_parser(self, sub_parsers):
        parser = sub_parsers.add_parser(
            "print",
            help="Retrieve the elements from configuration and print them."
        )

        parser.add_argument(
            "binaryFile",
            metavar="BINARY_FILE",
            type=str,
            nargs=1,
            help="Binary file in intel hex format (.hex) or binary (.bin)."
        )

        parser.add_argument(
            "configFile",
            metavar="CONFIG_FILE",
            type=str,
            nargs=1,
            help="Configuration file in JSON format (*.json)."
        )

        parser.add_argument(
            "-tf",
            "--templateFile",
            metavar="TEMPLATE_FILE",
            type=str,
            nargs="?",
            default=None,
            help="Template file in ASCII format."
        )


    def _create_checksum_sub_parser(self, sub_parsers):
        parser = sub_parsers.add_parser(
            "checksum",
            help="Calculate the CRC32 checksum for the specified data."
        )

        parser.add_argument(
            "binaryFile",
            metavar="BINARY_FILE",
            type=str,
            nargs=1,
            help="Binary file in intel hex format (.hex) or binary (.bin)."
        )
        parser.add_argument(
            "-sa",
            "--saddr",
            metavar="SADDR",
            type=lambda x: int(x, 0), # Support "0x" notation
            nargs=1,
            help="The calculation starts at this address."
        )
        parser.add_argument(
            "-ea",
            "--eaddr",
            metavar="EADDR",
            type=lambda x: int(x, 0), # Support "0x" notation
            nargs=1,
            help="The calculation ends at this address. (not included)"
        )       
        parser.add_argument(
            "-s",
            "--seed",
            metavar="SEED",
            type=lambda x: int(x, 0), # Support "0x" notation
            nargs="?", # Optional
            default=0,
            help="The seed value for the CRC calculation.\nDefault: 0"
        )

    def print_help(self):
        """Print the help information.
        """
        self._parser.print_help()

    def get_args(self):
        """Get parsed arguments.

        Returns:
            dict: Arguments
        """
        return self._args

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
