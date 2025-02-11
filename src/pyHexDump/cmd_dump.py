"""Command to show a hex dump."""

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
from pyHexDump.constants import Ret
from pyHexDump.common import common_load_binary_file, common_dump_intel_hex
from pyHexDump.mem_access import mem_access_get_api_by_data_type

################################################################################
# Variables
################################################################################

_CMD_NAME = "dump"

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def _cmd_dump(binary_file, addr, count, data_type):
    """Dump binary file to the console at the given address. It will contain a
        number of elements (count) depended on the data type (data_type).

    Args:
        binary_file (str): File name of the binary file
        addr (int): Address where to start the dump
        count (int): Number of elements which to dump
        data_type (str): Data type of a element (uint8, uint16le, uint16be, uint32le, uint32be)

    Returns:
        Ret: If successful it will return OK, otherwise a corresponding error code.
    """
    ret_status, intel_hex = common_load_binary_file(binary_file)

    if ret_status == Ret.OK:
        mem_access = mem_access_get_api_by_data_type(data_type)
        mem_access.set_binary_data(intel_hex)
        ret_status = common_dump_intel_hex(mem_access, addr, count)
        print("")

    return ret_status

def _exec(args):
    """Determine the required parameters from the program arguments and execute the command.

    Args:
        args (obj): Program arguments

    Returns:
        Ret: If successful, it will return Ret.OK otherwise a corresponding error.
    """
    return _cmd_dump(args.binaryFile[0], args.addr, args.count, args.dataType)

def cmd_register(arg_sub_parsers):
    """Register the command specific CLI argument parser and get command
        specific paramters.

    Args:
        arg_sub_parsers (obj): Register the parser here

    Returns:
        obj: Command parameters
    """
    cmd_par_dict = {}
    cmd_par_dict["name"] = _CMD_NAME
    cmd_par_dict["execFunc"] = _exec

    parser = arg_sub_parsers.add_parser(
        _CMD_NAME,
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
        required=False,
        default=0,
        help="The dump starts at this address.\n" \
            "(default: %(default)d)."
    )
    parser.add_argument(
        "-c",
        "--count",
        metavar="COUNT",
        type=lambda x: int(x, 0), # Support "0x" notation
        required=False,
        default=64,
        help="The number of elements (choosen by datatype) in the dump.\n" \
            "(default: %(default)d)"
    )
    parser.add_argument(
        "-dt",
        "--dataType",
        metavar="DATA_TYPE",
        choices=["uint8", "uint16le", "uint16be", "uint32le", "uint32be", "uint64le", "uint64be"],
        type=str,
        required=False,
        default="uint8",
        help="The type of a single data element.\n" \
            "(default: %(default)s)"
    )

    return cmd_par_dict

################################################################################
# Main
################################################################################
