"""Command to calculate the checksum.
The algrotihm and the table are taken from https://github.com/Michaelangel007/crc32
or from http://ross.net/crc/download/crc_v3.txt."""

# MIT License
#
# Copyright (c) 2022 Tobias Stelze (tobias.stelzle@newtec.de)
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
from pyHexDump.common import common_load_binary_file, common_print_value
from pyHexDump.mem_access import mem_access_get_api_by_data_type

# pylint: disable=duplicate-code

################################################################################
# Variables
################################################################################

_CMD_NAME = "checksum"

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

# pylint: disable=too-many-arguments, too-many-locals, too-many-positional-arguments
def calc_checksum(binary_data, binary_data_endianess, start_address, end_address,\
    polynomial, bit_width, seed, reverse_input, reverse_output, final_xor):
    """Calcuate the checksum for the given address in the binary_data and the
    given number of bytes.

    Args:
        binary_data (IntelHex): Binary data
        binary_data_endianess (str): Binary data endianess and data bit width, e.g. uint32le.
        start_address (int): Address where to start the calculation
        end_address (int):  Address where to end the calculation (not included)
        polynomial(int): Generator polynomial to use in the CRC calculation.
                         The bits in this integer are to coefficients in the polynomial.
        bit_width(int): Number of bits for the CRC calculation. They have to match with
                        the generator polynomial
        seed (int): Seed value for the CRC calculation
        reverse_input(bool): Reflect each single input byte if True
        reverse_output(bool): Reflect the final CRC value if True
        final_xor(bool): Xor the final result with the value 0xff before returning the soulution

    Returns:
        checksum: Checksum
    """
    mem_access = mem_access_get_api_by_data_type(binary_data_endianess)
    mem_access.set_binary_data(binary_data)
    offset = 0
    count = (end_address - start_address) / mem_access.get_size()

    bit_width_mask = pow(2, bit_width) - 1
    msb_mask = 1 << bit_width
    crc = seed
    word = 0

    polynomial = (1 << bit_width) | polynomial

    while count > 0:
        count -= 1

        word = mem_access.get_value(start_address + offset)

        for idx in range(mem_access.get_size()):
            # MSB first
            byte = word >> (8 * (mem_access.get_size() - idx - 1)) & 0xFF

            if reverse_input is True:
                tmp = f"{byte:08b}"
                byte = int(tmp[::-1], 2)

            crc = crc ^ (byte << (bit_width - 8))

            for _ in range(8):
                crc = crc << 1

                if (crc & msb_mask) != 0:
                    crc = crc ^ polynomial

        offset += mem_access.get_size()

    crc &= bit_width_mask

    if reverse_output is True:
        tmp = f"{crc:0{bit_width}b}"
        crc = int(tmp[::-1], 2)

    if final_xor:
        crc = crc ^ bit_width_mask

    return crc

# pylint: disable=too-many-arguments, too-many-positional-arguments
def _cmd_checksum(binary_file, binary_data_endianess, start_address, end_address, \
    polynomial, bit_width, seed, reverse_input, reverse_output, final_xor):
    """Print the checksum for the given address and the given number of bytes
    to the console.

    Args:
        binary_file (str): File name of the binary file
        binary_data_endianess (str): Binary data endianess and data bit width, e.g. uint32le.
        start_address (int): Address where to start the calculation
        end_address (int):  Address where to end the calculation (not included)
        polynomial(int): Generator polynomial to use in the CRC calculation.
                         The bits in this integer are to coefficients in the polynomial.
        bit_width(int): Number of bits for the CRC calculation. They have to match with
                        the generator polynomial
        seed (int): Seed value for the CRC calculation
        reverse_input(bool): Reflect each single input byte if True
        reverse_output(bool): Reflect the final CRC value if True
        final_xor(bool): Xor the final result with the value 0xff before returning the soulution

    Returns:
        Ret: If successful it will return OK, otherwise a corresponding error code.
    """
    ret_status, intel_hex = common_load_binary_file(binary_file)

    if ret_status == Ret.OK:
        checksum = calc_checksum(intel_hex, binary_data_endianess,
                                 start_address, end_address, polynomial, \
                                 bit_width, seed, reverse_input, \
                                 reverse_output, final_xor)

        value_width = bit_width // 4
        value_format = "{:0" + str(value_width) + "X}"
        common_print_value(checksum, value_format)

    return ret_status

def _exec(args):
    """Determine the required parameters from the program arguments and execute the command.

    Args:
        args (obj): Program arguments

    Returns:
        Ret: If successful, it will return Ret.OK otherwise a corresponding error.
    """
    return _cmd_checksum(args.binaryFile[0], \
                         args.binaryDataEndianess, \
                         args.saddr, args.eaddr,\
                         args.polynomial, args.bitWidth, \
                         args.seed, args.reverseIn, \
                         args.reverseOut, args.finalXOR)

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
        help="Calculate the CRCx checksum for the specified data."
    )

    parser.add_argument(
        "binaryFile",
        metavar="BINARY_FILE",
        type=str,
        nargs=1,
        help="Binary file in intel hex format (.hex) or binary (.bin)."
    )
    parser.add_argument(
        "-bde",
        "--binaryDataEndianess",
        metavar="BINARY_DATA_ENDIANESS",
        choices=["uint8", "uint16le", "uint16be", "uint32le", "uint32be", "uint64le", "uint64be"],
        required=False,
        default="uint8",
        help="The binary data endianess.\n" \
            "(default: %(default)s)"
    )
    parser.add_argument(
        "-sa",
        "--saddr",
        metavar="SADDR",
        type=lambda x: int(x, 0), # Support "0x" notation
        required=True,
        help="The calculation starts at this address."
    )
    parser.add_argument(
        "-ea",
        "--eaddr",
        metavar="EADDR",
        type=lambda x: int(x, 0), # Support "0x" notation
        required=True,
        help="The calculation ends at this address. (not included)"
    )
    parser.add_argument(
        "-p",
        "--polynomial",
        metavar="POLYNOMIAL",
        type=lambda x: int(x, 0), # Support "0x" notation
        required=False,
        default=0x04C11DB7,
        help="The polynomial for the CRC calculation.\n" \
            "(default: 0x%(default)x)"
    )
    parser.add_argument(
        "-bw",
        "--bitWidth",
        metavar="BIT_WIDTH",
        type=lambda x: int(x, 0), # Support "0x" notation
        required=False,
        default=32,
        help="The bit width of the CRC calculation.\n" \
            "(default: %(default)s)"
    )
    parser.add_argument(
        "-s",
        "--seed",
        metavar="SEED",
        type=lambda x: int(x, 0), # Support "0x" notation
        required=False,
        default=0,
        help="The seed value for the CRC calculation.\n" \
            "(default: %(default)d)"
    )
    parser.add_argument(
        "-ri",
        "--reverseIn",
        action="store_true",
        required=False,
        default=False,
        help="Use reverse input.\n" \
            "(default: %(default)s)"
    )
    parser.add_argument(
        "-ro",
        "--reverseOut",
        action="store_true",
        required=False,
        default=False,
        help="Use reverse output.\n" \
            "(default: %(default)s)"
    )
    parser.add_argument(
        "-fx",
        "--finalXOR",
        action="store_true",
        required=False,
        default=False,
        help="Use a final XOR with all bits 1.\n" \
            "(default: %(default)s)"
    )

    return cmd_par_dict

################################################################################
# Main
################################################################################
