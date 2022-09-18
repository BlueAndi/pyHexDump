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
from string import Template
from pyHexDump.constants import Ret
from pyHexDump.common import\
    common_load_binary_file,\
    common_load_json_file,\
    common_dump_intel_hex,\
    common_load_template_file
from pyHexDump.mem_access import mem_access_get_api_by_data_type

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

class ConfigElement:
    """Represents a single element in the configuration.
    """
    def __init__(self, name, addr, data_type, count) -> None:
        self._intel_hex = None
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
        self._intel_hex = intel_hex

    def get_value(self):
        """Get the configuration element value.
            If the count is 1, only a single value will be returned.
            If the count is greater than 1, a list of values will be returned.

        Returns:
            int, list: Configuration element value
        """
        value = 0

        if self._intel_hex is not None:
            if self._count == 1:
                value = self._mem_access.get_value(self._intel_hex, self._addr)
            elif self._count > 1:
                value = []
                for idx in range(self._count):
                    offset = idx * self._mem_access.get_size()
                    value.append(self._mem_access.get_value(self._intel_hex, self._addr + offset))
            else:
                value = 0

        return value

class MyTemplate(Template):
    """Template which supports additional a space as identifier, but not as first character.

    Args:
        Template (obj): Template base
    """
    braceidpattern="(?a:[_a-z][_a-z0-9 ]*)"

################################################################################
# Functions
################################################################################

def _get_config_elements(config_dict):
    cfg_elements = []

    for item in config_dict["elements"]:

        name = None
        if "name" in item:
            name = item["name"]

        addr = None
        if "addr" in item:
            if isinstance(item["addr"], str) is True:
                addr = int(item["addr"], 0)
            elif isinstance(item["addr"], int) is True:
                addr = item["addr"]

        data_type = None
        if "dataType" in item:
            data_type = item["dataType"]

        count = None
        if "count" in item:
            if isinstance(item["count"], str) is True:
                count = int(item["count", 0])
            elif isinstance(item["count"], int) is True:
                count = item["count"]

        if (name      is not None) and (addr  is not None) and \
           (data_type is not None) and (count is not None):
            cfg_elements.append(ConfigElement(name, addr, data_type, count))

    return cfg_elements

def _print_config_elements(intel_hex_file, cfg_elements):
    ret_status = Ret.OK

    for cfg_element in cfg_elements:
        cfg_element.set_intel_hex(intel_hex_file)

        print("{} @ ".format(cfg_element.get_name()), end="")
        common_dump_intel_hex(  intel_hex_file,
                                cfg_element.get_mem_access(),
                                cfg_element.get_addr(),
                                cfg_element.get_count(),
                                0)
        print("")

    return ret_status

def _print_template(intel_hex_file, cfg_elements, template):
    ret_status = Ret.OK
    element_dict = {}
    tmpl = MyTemplate(template)

    for cfg_element in cfg_elements:
        cfg_element.set_intel_hex(intel_hex_file)

        if cfg_element.get_count() == 1:
            width = cfg_element.get_mem_access().get_size() * 2
            out_str = "{:0{width}x}".format(cfg_element.get_value(), width=width)
            element_dict[cfg_element.get_name()] = out_str

        elif cfg_element.get_count() > 1:
            width = cfg_element.get_mem_access().get_size() * 2
            out_str = ""
            for idx in range(cfg_element.get_count()):
                if idx > 0:
                    out_str += " "
                out_str += "{:0{width}x}".format(cfg_element.get_value()[idx], width=width)
            element_dict[cfg_element.get_name()] = out_str

    try:
        print(tmpl.safe_substitute(element_dict))
    except ValueError:
        ret_status = Ret.ERROR_TEMPLATE

    return ret_status

def cmd_print(binary_file, config_file, template_file):
    """Print configuration element values. The configuration file contains the
        elements with its meta data. A template may be used to format the
        output. If no template is available, the configuration elements will
        be printed in the order they are defined in the configuration file.

    Args:
        binary_file (str): File name of the binary file
        config_file (str): File name of the configuration file
        template_file (str): File name of the template file

    Returns:
        Ret: If successful, it will return Ret.OK otherwise a error code.
    """
    ret_status, intel_hex_file = common_load_binary_file(binary_file)

    # Is binary file successful loaded?
    if ret_status == Ret.OK:
        ret_status, config_dict = common_load_json_file(config_file)

        # Is configuration file successful loaded?
        if ret_status == Ret.OK:
            cfg_elements = _get_config_elements(config_dict)

            # If there is no template file available, only the elements in the
            # configuration will be printed. Otherwise the template is used to
            # print a corresponding report.
            if template_file is None:
                ret_status = _print_config_elements(intel_hex_file, cfg_elements)
            else:
                ret_status, template = common_load_template_file(template_file)

                # Is template file successful loaded?
                if ret_status == Ret.OK:
                    ret_status = _print_template(intel_hex_file, cfg_elements, template)

    return ret_status

################################################################################
# Main
################################################################################
