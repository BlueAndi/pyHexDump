"""Template model
"""

# MIT License
#
# Copyright (c) 2022 - 2023 Andreas Merkle (web@blue-andi.de)
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
from pyHexDump.tmpl_element import TmplElementInt, \
                                    TmplElementIntList, \
                                    TmplElementFloat, \
                                    TmplElementFloatList, \
                                    TmplElementStr
from pyHexDump.mem_access import mem_access_get_api_by_data_type

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

class TmplModel():
    """The template model holds the template elements, which are provided to the
        template engine.
    """
    def __init__(self):
        self._tmpl_element_dict = {}

        # List of all config elements to be able to iterate in the template over all.
        self._tmpl_element_list = []

    def load_from_config_elements(self, binary_data, cfg_elements_dict):
        """Load the template element model from configuration elements.

        Args:
            binary_data (IntelHex): The binary data used to retrieve the value.
            cfg_elements_dict (dict): Configuration element objects
        """
        self._tmpl_element_dict = self._get_tmpl_element_dict(binary_data, cfg_elements_dict)
        self._tmpl_element_list = self._flatten_tmpl_dict(self._tmpl_element_dict)

    def get(self):
        """Get dictionary of configuration elements.

        Returns:
            dict: Configuration elements
        """
        return self._tmpl_element_dict

    def get_list(self):
        """Get list of configuration elements.

        Returns:
            list: Configuration elements
        """
        return self._tmpl_element_list

    def _is_integer(self, data_type):
        data_types = ["int8", "uint8", "int16le", "int16be", "uint16le", "uint16be", \
            "int32le", "int32be", "uint32le", "uint32be", "int64le", "int64be", "uint64le", \
            "uint64be"]

        return data_type in data_types

    def _is_float(self, data_type):
        data_types = ["float32le", "float32be", "float64le", "float64be"]

        return data_type in data_types

    def _is_str(self, data_type):
        data_types = ["utf8"]

        return data_type in data_types

    def _create_template_element_single(self, cfg_element, mem_access):
        value = mem_access.get_value(cfg_element.get_addr())
        bit_width = mem_access.get_size() * 8

        if self._is_integer(cfg_element.get_datatype()) is True:
            tmpl_element = TmplElementInt(cfg_element.get_name(), cfg_element.get_addr(), value, bit_width)     # pylint: disable=line-too-long
        elif self._is_float(cfg_element.get_datatype()) is True:
            tmpl_element = TmplElementFloat(cfg_element.get_name(), cfg_element.get_addr(), value, bit_width)   # pylint: disable=line-too-long
        elif self._is_str(cfg_element.get_datatype()) is True:
            tmpl_element = TmplElementStr(cfg_element.get_name(), cfg_element.get_addr(), chr(value), bit_width)     # pylint: disable=line-too-long
        else:
            raise NotImplementedError(f"Datatype {cfg_element.get_datatype()} is not supported.")

        return tmpl_element

    def _read_string_(self, mem_access, addr, max_length = 256, encoding="utf-8"):
        value_list = []
        idx = 0
        while max_length > idx:
            value = mem_access.get_value(addr + idx)
            if value == 0:
                break
            value_list.append(value)
            idx += 1

        byte_values = bytearray(value_list)

        return byte_values.decode(encoding)

    def _create_template_element_list(self, cfg_element, mem_access):
        bit_width = mem_access.get_size() * 8

        if self._is_str(cfg_element.get_datatype()) is True:
            max_length = cfg_element.get_count() * mem_access.get_size()
            str_utf8 = self._read_string_(mem_access, cfg_element.get_addr(), max_length, "utf-8")
            tmpl_element = TmplElementStr(cfg_element.get_name(), cfg_element.get_addr(), str_utf8, bit_width)              # pylint: disable=line-too-long

        else:

            value_list = []
            for idx in range(cfg_element.get_count()):
                value_list.append(mem_access.get_value(cfg_element.get_addr() + idx * mem_access.get_size()))               # pylint: disable=line-too-long

            if self._is_integer(cfg_element.get_datatype()) is True:
                tmpl_element = TmplElementIntList(cfg_element.get_name(), cfg_element.get_addr(), value_list, bit_width)    # pylint: disable=line-too-long
            elif self._is_float(cfg_element.get_datatype()) is True:
                tmpl_element = TmplElementFloatList(cfg_element.get_name(), cfg_element.get_addr(), value_list, bit_width)  # pylint: disable=line-too-long
            else:
                raise NotImplementedError(f"Datatype {cfg_element.get_datatype()} is not supported.")                       # pylint: disable=line-too-long

        return tmpl_element

    def _create_template_element(self, cfg_element, mem_access):
        if cfg_element.get_count() == 1:
            tmpl_element = self._create_template_element_single(cfg_element, mem_access)

        elif cfg_element.get_count() > 1:
            tmpl_element = self._create_template_element_list(cfg_element, mem_access)

        else:
            raise TypeError(f"Count of {cfg_element.get_count()} is invalid.")

        return tmpl_element

    def _get_tmpl_element_dict(self, binary_data, cfg_elements_dict):
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
                tmpl_element_dict[key] = self._get_tmpl_element_dict(binary_data, cfg_element)
            else:
                mem_access = mem_access_get_api_by_data_type(cfg_element.get_datatype())

                if mem_access is not None:
                    mem_access.set_binary_data(binary_data)
                    tmpl_element_dict[key] = self._create_template_element(cfg_element, mem_access)

        return tmpl_element_dict

    def _flatten_tmpl_dict(self, tmpl_element_dict):
        """Flattens a template element dictionary and provides it as a list.

        Args:
            tmpl_element_dict (dict): Template elements dictionary

        Returns:
            list: List of template elements
        """
        tmpl_element_list = []

        for key in tmpl_element_dict.keys():
            if isinstance(tmpl_element_dict[key], dict):
                tmpl_element_list.extend(self._flatten_tmpl_dict(tmpl_element_dict[key]))
            else:
                tmpl_element_list.append(tmpl_element_dict[key])

        return tmpl_element_list

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
