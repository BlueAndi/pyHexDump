"""Command to print information retrieved from a configuration.
    If no template for the report is given, it will list all elements in the
    configuration with its values.
    If a template is given, it will print the template and substitute the
    template variables with the corresponding configuration element value.
"""

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
from mako.template import Template
from mako.exceptions import SyntaxException, RichTraceback
from pyHexDump.constants import Ret
from pyHexDump.common import \
    common_load_binary_file, \
    common_load_template_file
from pyHexDump.macros import get_macro_dict, set_binary_data
from pyHexDump.bunch import dict_to_bunch
from pyHexDump.config_model import ConfigModel
from pyHexDump.tmpl_model import TmplModel

# pylint: disable=duplicate-code

################################################################################
# Variables
################################################################################

_CMD_NAME = "print"
_IS_VERBOSE = False

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def _print_config_elements(tmpl_element_dict, show_only_in_hex, namespace=""):
    """Print a single configuration element with its value, read from the
        binary data.

    Args:
        tmpl_element_dict (dict): Template element objects
        show_only_in_hex (bool): Show values only in hex format. Only applied without template.
        namespace (str, optional): Namespace which to use. Defaults to "".

    Returns:
        Ret: If successful, it will return Ret.OK otherwise a corresponding error.
    """
    ret_status = Ret.OK

    for key, tmpl_element in tmpl_element_dict.items():

        # The dictionary of elements may contain further dictionaries which
        # corresponds to a structure of elements.
        if isinstance(tmpl_element, dict):
            ret_status = _print_config_elements(tmpl_element, show_only_in_hex, namespace + key + ".") # pylint: disable=line-too-long
        else:
            if show_only_in_hex is True:
                print(f"{namespace}{key} @ {tmpl_element.addr():08X}: {tmpl_element.hex()}")
            else:
                print(f"{namespace}{key} @ {tmpl_element.addr():08X}: {tmpl_element}")

        if ret_status != Ret.OK:
            break

    return ret_status

def _print_template(tmpl_model, template, constants): # pylint: disable=too-many-locals
    """Print a generated report from template and configuration element dictionary.

    Args:
        tmpl_model (obj): The template element model
        template (str): The template content
        constants (dict): Dictionary of constants to be used in the template.

    Returns:
        Ret: If successul printed, it will return Ret.OK otherwise a corresponding error.
    """
    ret_status = Ret.OK
    tmpl_element_dict = tmpl_model.get()
    tmpl_element_list = tmpl_model.get_list()

    # Add a list of all config elements to be able to iterate in the template over all.
    tmpl_element_dict.update({
        "config_elements": tmpl_element_list
    })

    if _IS_VERBOSE is True:
        print("Configuration elements:")
        for element in tmpl_element_list:
            print(f"* {element.name()}")
        print("\n")

    # Add macro functions, so they are available in the template
    tmpl_element_dict.update(get_macro_dict())

    # Add constants to be available in the template
    tmpl_element_dict.update(constants)

    # Create the template
    tmpl_element_bunch = dict_to_bunch(tmpl_element_dict)

    try:
        tmpl = Template(template, strict_undefined=True)
        print(tmpl.render(**tmpl_element_bunch))
    except (ValueError, NameError) as error:
        print(f"{type(error).__name__} in template:\n")
        print(error)
        ret_status = Ret.ERROR_TEMPLATE
    except (TypeError, AttributeError, SyntaxException) as error:
        # Show only relevant part of trace
        traceback = RichTraceback()
        show = False
        print(f"{type(error).__name__} in template:\n")
        for (filename, lineno, function, line) in traceback.traceback:
            if show is False and function == "render_body":
                show = True

            if show is True:
                print(f"File {filename}, line {lineno}, in {function}")
                print(line, "\n")
                print(f"{str(traceback.error.__class__.__name__)}: {traceback}")

        ret_status = Ret.ERROR_TEMPLATE

    return ret_status

def _constants_to_dict(constants):
    """Convert list of constants in key:value format to a dictionary.

    Args:
        constants (list(str)): List of constants

    Returns:
        dict(str): Dictionary with constants
    """
    constants_dict = {}

    for constant in constants:
        key_value_pair = constant.split(":", 1)

        if key_value_pair is not None:
            constants_dict[key_value_pair[0]] = key_value_pair[1]

    return constants_dict

def _cmd_print(binary_file, config_file, template_file, show_only_in_hex, constants):
    """Print configuration element values. The configuration file contains the
        elements with its meta data. A template may be used to format the
        output. If no template is available, the configuration elements will
        be printed in the order they are defined in the configuration file.

    Args:
        binary_file (str): File name of the binary file
        config_file (str): File name of the configuration file
        template_file (str): File name of the template file
        show_only_in_hex (bool): Show values only in hex format. Only applied without template.
        constants (list): List of constants to be used in the template. Format "key:value".

    Returns:
        Ret: If successful, it will return Ret.OK otherwise a error code.
    """
    ret_status, binary_data = common_load_binary_file(binary_file)

    # Is binary file successful loaded?
    if ret_status == Ret.OK:
        config_model = ConfigModel()

        ret_status = config_model.load(config_file)

        # Is configuration file successful loaded?
        if ret_status == Ret.OK:
            tmpl_model = TmplModel()

            tmpl_model.load_from_config_elements(binary_data, config_model.get())

            # If there is no template file available, only the elements in the
            # configuration will be printed. Otherwise the template is used to
            # print a corresponding report.
            if template_file is None:
                ret_status = _print_config_elements(tmpl_model.get(), show_only_in_hex) # pylint: disable=line-too-long
            else:
                ret_status, template = common_load_template_file(template_file)

                # Is template file successful loaded?
                if ret_status == Ret.OK:

                    # Ensure that the macros can access the binary data
                    set_binary_data(binary_data)

                    constants_dict = {}
                    if constants is not None:
                        constants_dict = _constants_to_dict(constants)

                    ret_status = _print_template(tmpl_model, template, constants_dict)

    return ret_status

def _exec(args):
    """Determine the required parameters from the program arguments and execute the command.

    Args:
        args (obj): Program arguments

    Returns:
        Ret: If successful, it will return Ret.OK otherwise a corresponding error.
    """
    global _IS_VERBOSE # pylint: disable=global-statement
    _IS_VERBOSE = args.verbose

    # Constants are optional
    constants = getattr(args, 'constant', None)

    return _cmd_print(args.binaryFile[0], args.configFile[0], args.templateFile, args.onlyInHex, constants) # pylint: disable=line-too-long,too-many-function-args

def cmd_print_register(arg_sub_parsers):
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
        required=False,
        default=None,
        help="Template file in ASCII format."
    )

    parser.add_argument(
        "-oih",
        "--onlyInHex",
        action="store_true",
        required=False,
        default=False,
        help="Show values in hex format. Only applied valid without template."
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        required=False,
        default=False,
        help="Prints more additional information."
    )

    parser.add_argument(
        "-c",
        "--constant",
        action="append",
        required=False,
        help="Constant key/value pair to be used in the template. " \
                "Can be applied several times. Example --constant name:value"
    )

    return cmd_par_dict

################################################################################
# Main
################################################################################
