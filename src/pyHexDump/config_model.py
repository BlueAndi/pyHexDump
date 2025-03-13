"""Configuration model
"""

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
from pyHexDump.common import common_load_json_file
from pyHexDump.mem_access import mem_access_get_api_by_data_type
from pyHexDump.config_element import ConfigElement, PaddingElement

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

class ConfigModel():
    """The configuration model holds a configuration elements.
    """
    def __init__(self):
        self._list = []

    def load(self, file_name):
        """Load configuration model from file.

        Args:
            file_name (str): Name of the configuration file.
        """
        ret_status, config_dict = common_load_json_file(file_name)

        if ret_status == Ret.OK:
            self._list = self._get_config_elements(config_dict)

        return ret_status

    def get(self):
        """Get list of configuration elements.

        Returns:
            list: Configuration elements
        """
        return self._list

    def _find_structure_definition(self, config_dict, structure_name):
        """Find a structure definition by its name.

        Args:
            config_dict (dict): Configuration items
            structure_name (str): Name of the structure

        Returns:
            dict: If structure found, it will return its definition otherwise None.
        """
        structure_pos = None

        if "structures" in config_dict:
            for idx, item in enumerate(config_dict["structures"]):
                if "name" in item:
                    name = item["name"]
                    if name == structure_name:
                        if "elements" in item:
                            structure_pos = item["elements"]
                        else:
                            print(f"Warning: \"elements\" is missing for {name} element.")
                        break

                else:
                    print(f"Warning: \"name\" is missing for {idx + 1}. structure element.")

        return structure_pos

    def _get_name_from_config_item(self, item):
        """Get the name from the configuration item.

        Args:
            item (dict): Configuration item

        Returns:
            str, optional: Name of the configuration item.
        """
        name = None

        if "name" in item:
            name = item["name"]

        return name

    def _get_count_from_config_item(self, item):
        count = None

        if "count" in item:
            if isinstance(item["count"], str) is True:
                count = int(item["count"], 0)
            elif isinstance(item["count"], int) is True:
                count = item["count"]

        return count

    def _get_addr_from_config_item(self, item):
        addr = None

        if "addr" in item:
            if isinstance(item["addr"], str) is True:
                addr = int(item["addr"], 0)
            elif isinstance(item["addr"], int) is True:
                addr = item["addr"]

        return addr

    def _get_offset_from_config_item(self, item):
        offset = None

        if "offset" in item:
            if isinstance(item["offset"], str) is True:
                offset = int(item["offset"], 0)
            elif isinstance(item["offset"], int) is True:
                offset = item["offset"]

        return offset

    def _get_data_type_from_config_item(self, item):
        data_type = None

        if "dataType" in item:
            # Built-in datatype or structure?
            if isinstance(item["dataType"], str) is True:
                data_type = item["dataType"]
            elif isinstance(item["dataType"], list) is True:
                data_type = item["dataType"]

        return data_type

    # pylint: disable=too-many-locals,too-many-branches
    def _get_config_structure(self, structure_name, structure_definition, config_dict, base_addr):
        """Get a configuration element object dictionary from the configuration
            item sub dictionary. If not all necessary parameters are available,
            it will be skipped.

        Args:
            structure_name (str): Structure name
            structure_definition (dict): Structure definition
            config_dict (dict): Configuration items
            base_addr (int): The base address of the sub dictionary

        Returns:
            dict: Configuration element objects.
        """
        cfg_elements_dict = {}
        addr = base_addr

        for idx, item in enumerate(structure_definition):

            # "name" is mandatory
            name = self._get_name_from_config_item(item)

            if name is None:
                print(f"Warning: \"name\" is missing for {idx + 1}. structure element.")
                break

            # "count" is mandatory
            count = self._get_count_from_config_item(item)

            if count is None:
                print(f"Warning: \"count\" is missing for {name} structure element.")
                break

            # "offset" is optional
            offset = self._get_offset_from_config_item(item)

            if offset is None:
                offset = 0

            # A offset is always relative to the given base address.
            elif offset > 0:
                # Padding between the elements?
                if addr < base_addr + offset:
                    # Add padding element to be able to calculate the size of structures correctly.
                    padding_key = name + "_padding"
                    cfg_elements_dict[padding_key] = PaddingElement(base_addr + offset - addr)

                addr = base_addr + offset

            else:
                print(f"Warning: \"offset\" is invalid for {name} structure element.")
                break

            # "data_type" is mandatory
            data_type = self._get_data_type_from_config_item(item)

            if data_type is None:
                print(f"Warning: \"dataType\" is missing for {name} structure element.")
                break

            name_full = structure_name + "." + name

            # Is it a builtin or custom datatype?
            if isinstance(data_type, str) is True:

                # Is it a custom datatype which is defined separately?
                mem_access = mem_access_get_api_by_data_type(data_type)
                if mem_access is None:
                    sub_structure_definition = self._find_structure_definition(config_dict, data_type)

                    if sub_structure_definition is None:
                        print(f"Warning: Data type {data_type} not found.")
                    else:
                        cfg_elements_dict_sub = self._get_config_structure(name_full,
                                                                            sub_structure_definition,
                                                                            config_dict,
                                                                            addr)

                        cfg_elements_dict[name] = ConfigElement(name_full,
                                                                addr,
                                                                data_type,
                                                                count,
                                                                cfg_elements_dict_sub)

                        addr += cfg_elements_dict[name].size

                # Builtin datatype
                else:
                    cfg_elements_dict[name] = ConfigElement(name_full, addr, data_type, count)
                    addr += cfg_elements_dict[name].size

            # Does the datatype contain the structure information in itself?
            elif isinstance(data_type, list) is True:
                cfg_elements_dict_sub = self._get_config_structure(name_full,
                                                                    item["dataType"],
                                                                    config_dict,
                                                                    addr)

                cfg_elements_dict[name] = ConfigElement(name_full,
                                                        addr,
                                                        "structure",
                                                        count,
                                                        cfg_elements_dict_sub)

                addr += cfg_elements_dict[name].size

            else:
                raise NotImplementedError

        return cfg_elements_dict

    # pylint: disable=too-many-branches
    def _get_config_elements(self, config_dict):
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
            print("Warning: No elements found.")
            return cfg_elements_dict

        for idx, item in enumerate(config_dict["elements"]):

            # "name" is mandatory
            name = self._get_name_from_config_item(item)

            if name is None:
                print(f"Warning: \"name\" is missing for {idx + 1}. element.")
                continue

            # "addr" is mandatory
            addr = self._get_addr_from_config_item(item)

            if addr is None:
                print(f"Warning: \"addr\" is missing for {name}.")
                continue

            # "count" is mandatory
            count = self._get_count_from_config_item(item)

            if count is None:
                print(f"Warning: \"count\" is missing for {name}.")
                continue

            # "data_type" is mandatory
            data_type = self._get_data_type_from_config_item(item)

            if data_type is None:
                print(f"Warning: \"dataType\" is missing for {name}.")
                continue

            # Is it a builtin or custom datatype?
            if isinstance(data_type, str) is True:

                # Is it a custom datatype which is defined separately?
                if mem_access_get_api_by_data_type(data_type) is None:
                    structure_definition = self._find_structure_definition(config_dict, data_type)

                    if structure_definition is None:
                        print(f"Warning: Data type {data_type} not found.")
                    else:
                        structure_elements_dict = self._get_config_structure(name,
                                                                            structure_definition,
                                                                            config_dict,
                                                                            addr)

                        if name not in cfg_elements_dict:
                            cfg_elements_dict[name] = ConfigElement(name,
                                                                    addr,
                                                                    data_type,
                                                                    count,
                                                                    structure_elements_dict)
                        else:
                            cfg_elements_dict[name].elements |= structure_elements_dict

                # Builtin datatype
                else:
                    cfg_elements_dict[name] = ConfigElement(name, addr, data_type, count)

            # Does the datatype contain the structure information in itself?
            elif isinstance(data_type, list) is True:
                structure_elements_dict = self._get_config_structure(name,
                                                                    item["dataType"],
                                                                    config_dict,
                                                                    addr)

                if name not in cfg_elements_dict:
                    cfg_elements_dict[name] = ConfigElement(name,
                                                            addr,
                                                            data_type,
                                                            count,
                                                            structure_elements_dict)
                else:
                    cfg_elements_dict[name].elements |= structure_elements_dict
            else:
                raise NotImplementedError

        return cfg_elements_dict

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
