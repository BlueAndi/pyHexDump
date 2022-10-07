"""This module contains the commands switch.
    It determines the command and the command specific arguments and
    execute it.
"""

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
from pyHexDump.constants import Ret
from pyHexDump.cmd_dump import cmd_dump
from pyHexDump.cmd_print import cmd_print
from pyHexDump.cmd_print_checksum import cmd_print_checksum

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def commands_handle_command(args):
    """Handle the command in the program arguments.

    Args:
        args (obj): Program arguments

    Returns:
        int: Function return status
    """
    ret_status = Ret.OK

    # Determine command and execute it
    if args.cmd == "dump":
        ret_status = cmd_dump(args.binaryFile[0], args.addr, args.count, args.dataType)
    elif args.cmd == "print":
        ret_status = cmd_print(args.binaryFile[0], args.configFile[0], args.templateFile)
    elif args.cmd ==  "checksum":
        ret_status = cmd_print_checksum(args.binaryFile[0], args.saddr, args.eaddr,\
                        args.polynomial, args.bitWidth, args.seed, args.reverseIn, \
                        args.reverseOut, args.finalXOR)
    else:
        ret_status = Ret.ERROR_UNKNOWN_COMMAND

    return ret_status

################################################################################
# Main
################################################################################
