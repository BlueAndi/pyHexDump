"""Command to print information retrieved from a configuration.
    If no template for the report is given, it will list all elements in the
    configuration with its values.
    If a template is given, it will print the template and substitute the
    template variables with the corresponding configuration element value.
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
import struct
from mako.template import Template
from mako.exceptions import SyntaxException, RichTraceback
from pyHexDump.constants import Ret
from pyHexDump.common import \
    common_load_binary_file, \
    common_load_json_file, \
    common_load_template_file
from pyHexDump.mem_access import mem_access_get_api_by_data_type
from pyHexDump.macros import get_macro_dict, set_binary_data

# pylint: disable=duplicate-code

################################################################################
# Variables
################################################################################

_CMD_NAME = "print"

################################################################################
# Classes
################################################################################

class ConfigElement:
    """Represents a single element in the configuration.
    """
    def __init__(self, name, addr, data_type, count) -> None:
        self._name = name
        self._addr = addr
        self._mem_access = mem_access_get_api_by_data_type(data_type)
        self._count = count

    def get_name(self):
        """Get the configuration element name.

        Returns:
            str: Configuration element name
        """
        return self._name

    def get_addr(self):
        """Get the configuration element address.

        Returns:
            int: Configuration element address
        """
        return self._addr

    def get_count(self):
        """Get the configuration element count.
            A count of 1 means its just one value.
            Greater than 1 for a array of values.

        Returns:
            int: Configuration element count
        """
        return self._count

    def get_mem_access(self):
        """Get the memory access API.

        Returns:
            MemAccess: Memory access API
        """
        return self._mem_access

    def set_intel_hex(self, intel_hex):
        """Set the intel hex ...

        Args:
            intel_hex (_type_): _description_
        """
        if self._mem_access is not None:
            self._mem_access.set_binary_data(intel_hex)

    def get_value(self):
        """Get the configuration element value.
            If the count is 1, only a single value will be returned.
            If the count is greater than 1, a list of values will be returned.

        Returns:
            int, list: Configuration element value
        """
        value = 0

        if self._mem_access is None:
            return 0

        if self._count == 1:
            value = self._mem_access.get_value(self._addr)
        elif self._count > 1:
            value = []
            for idx in range(self._count):
                offset = idx * self._mem_access.get_size()
                value.append(self._mem_access.get_value(self._addr + offset))
        else:
            value = 0

        return value

class Bunch(dict):
    """Bunch is a dictionary that supports attribute-style access, a la JavaScript.
        A dictionary must be accessed via myDict["test"].
        A bunch can access the same with myDict.test.
    """
    def __init__(self, dict_of_items):
        dict.__init__(self, dict_of_items)
        self.__dict__.update(dict_of_items)

class TmplElement():
    """Template element representing a element with a address, value and bit width.
    """
    def __init__(self, name, addr, value, bit_width) -> None:
        self._name = name
        self._addr = addr
        self._value = value
        self._bit_width = bit_width

    def __int__(self):
        if isinstance(self._value, int) is False:
            raise TypeError("Template element is not a int.")
        return self._value

    def __str__(self):
        return str(self._value)

    def __add__(self, value):
        return self._value + value

    def __sub__(self, value):
        return self._value - value

    def __mul__(self, value):
        return self._value * value

    def __pow__(self, value):
        return self._value ** value

    def __truediv__(self, value):
        return self._value / value

    def __floordiv__(self, value):
        return self._value // value

    def __mod__(self, value):
        return self._value % value

    def __lshift__(self, value):
        return self._value << value

    def __rshift__(self, value):
        return self._value >> value

    def __and__(self, value):
        return self._value & value

    def __or__(self, value):
        return self._value | value

    def __xor__(self, value):
        return self._value ^ value

    def __invert__(self):
        return ~self._value

    def __lt__(self, value):
        return self._value < value

    def __le__(self, value):
        return self._value <= value

    def __eq__(self, value):
        return self._value == value

    def __ne__(self, value):
        return self._value != value

    def __gt__(self, value):
        return self._value > value

    def __ge__(self, value):
        return self._value >= value

    def __getitem__(self, idx):
        if isinstance(self._value, list) is False:
            raise TypeError("Template element is not a list.")
        return self._value[idx]

    def _value_to_hex(self, value, prefix):

        if isinstance(value, int) is True:
            if value < 0:
                value &= (1 << self._bit_width) - 1

        elif isinstance(value, float) is True:
            if self._bit_width == 32:
                value = struct.unpack('<I', struct.pack('<f', value))[0]
            elif self._bit_width == 64:
                value = struct.unpack('<Q', struct.pack('<d', value))[0]
            else:
                raise NotImplementedError(f"Unsupported bit width of {self._bit_width} for float")

        return f"{prefix}{value:0{self._bit_width // 4}X}"

    def hex(self, prefix="0x"):
        """Get the value in hex format.

        Args:
            prefix (str, optional): Prefix. Defaults to "0x".

        Returns:
            str: Hex value
        """
        output = ""

        if isinstance(self._value, int) is True:
            output = self._value_to_hex(self._value, prefix)

        elif isinstance(self._value, float) is True:
            output = self._value_to_hex(self._value, prefix)

        elif isinstance(self._value, list) is True:
            output = "["

            for idx, value in enumerate(self._value):

                if idx > 0:
                    output += ", "

                output += self._value_to_hex(value, prefix)

            output += "]"

        else:
            raise NotImplementedError(f"{type(self._value)} is not supported.")

        return output

    def name(self):
        """Get name of the element.

        Returns:
            str: Element name
        """
        return self._name

    def addr(self):
        """Get the address of the element in the binary data.

        Returns:
            int: Address
        """
        return self._addr

################################################################################
# Functions
################################################################################

def _dict_to_bunch(dict_of_items):
    """Convert a dictionary to a bunch.

    Args:
        dict_of_items (dict): Dictionary of items

    Returns:
        Bunch: Bunch of items
    """
    bunch_of_items = {}

    for key, value in dict_of_items.items():
        if isinstance(value, dict):
            value = _dict_to_bunch(value)

        bunch_of_items[key] = value

    return Bunch(bunch_of_items)

def _find_structure_definition(config_dict, structure_name):
    """Find a structure definition by its name.

    Args:
        config_dict (dict): Configuration items
        structure_name (str): Name of the structure

    Returns:
        dict: If structure found, it will return its definition otherwise None.
    """
    structure_pos = None

    if "structures" in config_dict:
        for item in config_dict["structures"]:
            if "name" in item:
                if item["name"] == structure_name:
                    if "elements" in item:
                        structure_pos = item["elements"]

                    break

    return structure_pos

def _get_name_from_config_item(item):
    name = None

    if "name" in item:
        name = item["name"]

    return name

def _get_count_from_config_item(item):
    count = None

    if "count" in item:
        if isinstance(item["count"], str) is True:
            count = int(item["count"], 0)
        elif isinstance(item["count"], int) is True:
            count = item["count"]

    return count

def _get_addr_from_config_item(item):
    addr = None

    if "addr" in item:
        if isinstance(item["addr"], str) is True:
            addr = int(item["addr"], 0)
        elif isinstance(item["addr"], int) is True:
            addr = item["addr"]

    return addr

def _get_offset_from_config_item(item):
    offset = None

    if "offset" in item:
        if isinstance(item["offset"], str) is True:
            offset = int(item["offset"], 0)
        elif isinstance(item["offset"], int) is True:
            offset = item["offset"]

    return offset

def _get_data_type_from_config_item(item):
    data_type = None

    if "dataType" in item:
        # Built-in datatype or structure?
        if isinstance(item["dataType"], str) is True:
            data_type = item["dataType"]
        elif isinstance(item["dataType"], list) is True:
            data_type = item["dataType"]

    return data_type

def _get_config_structure(config_dict, base_addr):
    """Get a configuration element object dictionary from the configuration
        item sub dictionary. If not all necessary parameters are available,
        it will be skipped.

        Nested structures are not supported!

    Args:
        config_dict (dict): Configuration items
        base_addr (int): The base address of the sub dictionary

    Returns:
        dict: Configuration element objects
    """
    cfg_elements_dict = {}
    addr = base_addr

    for item in config_dict:

        # "name" is mandatory
        name = _get_name_from_config_item(item)

        if name is None:
            break

        # "count" is mandatory
        count = _get_count_from_config_item(item)

        if count is None:
            break

        # "offset" is optional
        offset = _get_offset_from_config_item(item)

        if offset is None:
            offset = 0

        # "data_type" is mandatory
        data_type = _get_data_type_from_config_item(item)

        # Nested structures not supported yet!
        if isinstance(data_type, list) is True:
            break

        if data_type is None:
            break

        # A offset is always relative to the given base address.
        if offset > 0:
            addr = base_addr + offset

        cfg_elements_dict[name] = ConfigElement(name, addr, data_type, count)

        addr += count * mem_access_get_api_by_data_type(data_type).get_size()

    return cfg_elements_dict

#pylint: disable-next=too-many-branches
def _get_config_elements(config_dict):
    """Get a configuration element object dictionary from the configuration
        item dictionary. If a configuration item doesn't contain all
        necessary parameters, it will be skipped.

    Args:
        config_dict (dict): Configuration items

    Returns:
        dict: Configuration element objects
    """
    cfg_elements_dict = {}

    if "elements" not in config_dict:
        return cfg_elements_dict

    for item in config_dict["elements"]:

        # "name" is mandatory
        name = _get_name_from_config_item(item)

        if name is None:
            continue

        # "addr" is mandatory
        addr = _get_addr_from_config_item(item)

        if addr is None:
            continue

        # "count" is mandatory
        count = _get_count_from_config_item(item)

        if count is None:
            continue

        # "data_type" is mandatory
        data_type = _get_data_type_from_config_item(item)

        if data_type is None:
            continue

        if isinstance(data_type, str) is True:
            # If a memory access API is available, its a built-in type otherwise a structure.
            mem_access = mem_access_get_api_by_data_type(data_type)
            if mem_access is None:
                structure_definition = _find_structure_definition(config_dict, data_type)

                if structure_definition is not None:
                    if name not in cfg_elements_dict:
                        cfg_elements_dict[name] = _get_config_structure(structure_definition, addr)
                    else:
                        cfg_elements_dict[name] |= _get_config_structure(structure_definition, addr)

            else:
                cfg_elements_dict[name] = ConfigElement(name, addr, data_type, count)

        elif isinstance(data_type, list) is True:
            if name not in cfg_elements_dict:
                cfg_elements_dict[name] = _get_config_structure(item["dataType"], addr)
            else:
                cfg_elements_dict[name] |= _get_config_structure(item["dataType"], addr)

    return cfg_elements_dict

def _print_config_elements(binary_data, tmpl_element_dict, show_only_in_hex, namespace=""):
    """Print a single configuration element with its value, read from the
        binary data.

    Args:
        binary_data (IntelHex): Binary data
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
            _print_config_elements(binary_data, tmpl_element, show_only_in_hex, namespace + key + ".") # pylint: disable=line-too-long
        else:
            if show_only_in_hex is True:
                print(f"{namespace}{key} @ {tmpl_element.addr():08X}: {tmpl_element.hex()}")
            else:
                print(f"{namespace}{key} @ {tmpl_element.addr():08X}: {tmpl_element}")

    return ret_status

def _get_tmpl_element_dict(binary_data, cfg_elements_dict):
    """Get a dictionary of elements and its value.

    Args:
        binary_data (IntelHex): The binary data used to retrieve the value.
        cfg_elements_dict (dict): Configuration element objects

    Returns:
        dict: Dictionary of elements and its value.
    """
    tmpl_element_dict = {}

    for key, cfg_element in cfg_elements_dict.items():

        if isinstance(cfg_element, dict):
            tmpl_element_dict[key] = _get_tmpl_element_dict(binary_data, cfg_element)
        else:
            cfg_element.set_intel_hex(binary_data)

            if cfg_element.get_count() == 1:
                bit_width = cfg_element.get_mem_access().get_size() * 8
                tmpl_element_dict[key] = TmplElement(key, cfg_element.get_addr(), cfg_element.get_value(), bit_width) # pylint: disable=line-too-long

            elif cfg_element.get_count() > 1:
                bit_width = cfg_element.get_mem_access().get_size() * 8
                value_list = []
                for idx in range(cfg_element.get_count()):
                    value_list.append(cfg_element.get_value()[idx])

                tmpl_element_dict[key] = TmplElement(key, cfg_element.get_addr(), value_list, bit_width) # pylint: disable=line-too-long

    return tmpl_element_dict

def _print_template(binary_data, tmpl_element_dict, template):
    """Print a generated report from template and configuration element dictionary.

    Args:
        binary_data (IntelHex): The binary data to retrieve the element values.
        tmpl_element_dict (dict): The template element objects.
        template (str): The template content

    Returns:
        Ret: If successul printed, it will return Ret.OK otherwise a corresponding error.
    """
    ret_status = Ret.OK

    # Add a list of all config elements to be able to iterate in the template over all.
    tmpl_element_list = []
    for tmpl_element_name in tmpl_element_dict.keys():
        tmpl_element_list.append(tmpl_element_dict[tmpl_element_name])

    tmpl_element_dict.update({
        "config_elements": tmpl_element_list
    })

    # Add macro functions, so they are available in the template
    tmpl_element_dict.update(get_macro_dict())
    # Ensure that the macros can access the binary data
    set_binary_data(binary_data)

    # Create the template
    tmpl_element_bunch = _dict_to_bunch(tmpl_element_dict)

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

def _cmd_print(binary_file, config_file, template_file, show_only_in_hex):
    """Print configuration element values. The configuration file contains the
        elements with its meta data. A template may be used to format the
        output. If no template is available, the configuration elements will
        be printed in the order they are defined in the configuration file.

    Args:
        binary_file (str): File name of the binary file
        config_file (str): File name of the configuration file
        template_file (str): File name of the template file
        show_only_in_hex (bool): Show values only in hex format. Only applied without template.

    Returns:
        Ret: If successful, it will return Ret.OK otherwise a error code.
    """
    ret_status, binary_data = common_load_binary_file(binary_file)

    # Is binary file successful loaded?
    if ret_status == Ret.OK:
        ret_status, config_dict = common_load_json_file(config_file)

        # Is configuration file successful loaded?
        if ret_status == Ret.OK:
            cfg_elements_dict = _get_config_elements(config_dict)
            tmpl_element_dict = _get_tmpl_element_dict(binary_data, cfg_elements_dict)

            # If there is no template file available, only the elements in the
            # configuration will be printed. Otherwise the template is used to
            # print a corresponding report.
            if template_file is None:
                ret_status = _print_config_elements(binary_data, tmpl_element_dict, show_only_in_hex) # pylint: disable=line-too-long
            else:
                ret_status, template = common_load_template_file(template_file)

                # Is template file successful loaded?
                if ret_status == Ret.OK:
                    ret_status = _print_template(binary_data, tmpl_element_dict, template)

    return ret_status

def _exec(args):
    """Determine the required parameters from the program arguments and execute the command.

    Args:
        args (obj): Program arguments

    Returns:
        Ret: If successful, it will return Ret.OK otherwise a corresponding error.
    """
    return _cmd_print(args.binaryFile[0], args.configFile[0], args.templateFile, args.onlyInHex)

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

    return cmd_par_dict

################################################################################
# Main
################################################################################
