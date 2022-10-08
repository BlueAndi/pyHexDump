"""The main module with the program entry point."""

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
import sys
from pyHexDump.constants import Ret
from pyHexDump.prg_arg_parser import PrgArgParser

from pyHexDump.cmd_dump import cmd_dump_register
from pyHexDump.cmd_print import cmd_print_register
from pyHexDump.cmd_print_checksum import cmd_checksum_register

################################################################################
# Variables
################################################################################

# Register a command here!
_COMMAND_REG_LIST = [
    cmd_dump_register,
    cmd_print_register,
    cmd_checksum_register
]

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def _get_cmd_exec_func(commands, cmd_name):
    exec_func = None

    for cmd in commands:
        if cmd["name"] == cmd_name:
            exec_func = cmd["execFunc"]

    return exec_func

def main():
    """The program entry point function.

    Returns:
        int: System exit status
    """
    ret_status          = Ret.OK
    prg_arg_parser      = PrgArgParser()
    prg_arg_sub_parsers = prg_arg_parser.get_sub_parsers()
    commands            = []

    # Register all command specific argument parsers
    for cmd_reg_func in _COMMAND_REG_LIST:
        cmd_par_dict = cmd_reg_func(prg_arg_sub_parsers)
        commands.append(cmd_par_dict)

    # Parse all program arguments now
    prg_arg_parser.parse_args()

    # Uncomment for debugging purposes
    print(prg_arg_parser.get_args())

    # If no program arguments are available, the help information shall be shown.
    if prg_arg_parser.get_args().cmd is None:
        prg_arg_parser.print_help()
    else:
        # Handle command received via program arguments
        cmd_exec_func = _get_cmd_exec_func(commands, prg_arg_parser.get_args().cmd)

        if cmd_exec_func is None:
            ret_status = Ret.ERROR_UNKNOWN_COMMAND
        else:
            ret_status = cmd_exec_func(prg_arg_parser.get_args())

    return ret_status

################################################################################
# Main
################################################################################

if __name__ == "__main__":
    sys.exit(main())
