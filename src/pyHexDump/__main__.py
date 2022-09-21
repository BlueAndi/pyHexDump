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
from pyHexDump.commands import commands_handle_command

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def main():
    """The program entry point function.

    Returns:
        int: System exit status
    """
    ret_status      = Ret.OK
    prg_arg_parser  = PrgArgParser()

    # Uncomment for debugging purposes
    #print(prg_arg_parser.get_args())

    # If no program arguments are available, the help information shall be shown.
    if prg_arg_parser.get_args().cmd is None:
        prg_arg_parser.print_help()
    else:

        # Handle command received via program arguments
        ret_status = commands_handle_command(prg_arg_parser.get_args())

        # Any error?
        if ret_status != Ret.OK:

            # Print more detail about the kind of error
            if ret_status == Ret.ERROR_INPUT_FILE_NOT_FOUND:
                print(f"File {prg_arg_parser.get_args().binaryFile[0]} not found.")
            elif ret_status == Ret.ERROR_CONFIG_FILE_NOT_FOUND:
                print(f"File {prg_arg_parser.get_args().configFile[0]} not found.")
            elif ret_status == Ret.ERROR_TEMPLATE_FILE_NOT_FOUND:
                print(f"File {prg_arg_parser.get_args().templateFile} not found.")
            elif ret_status == Ret.ERROR_UNKNOWN_COMMAND:
                print(f"Unknown command {prg_arg_parser.get_args().cmd}.")
            elif ret_status == Ret.ERROR_TEMPLATE:
                print("Template error")
            else:
                print("Error")

    return ret_status

################################################################################
# Main
################################################################################

if __name__ == "__main__":
    sys.exit(main())
