"""Tests
"""

from pyHexDump.constants import Ret
from pyHexDump.prg_arg_parser import PrgArgParser
from pyHexDump.cmd_print import cmd_print_register, _exec
from pyHexDump.bunch import dict_to_bunch

def test_cmd_registration():
    """Test the command registration.
    """
    main_prg_arg_parser = PrgArgParser()
    cmd = cmd_print_register(main_prg_arg_parser.get_sub_parsers())

    assert cmd["name"] == "print"
    assert hasattr(cmd["execFunc"], "__call__") is True

def test_config(capsys):
    """Test the call via command line args."""
    args = {
        "binaryFile": [ "tests/data/data.txt" ],
        "configFile": [ "tests/data/config.json" ],
        "templateFile": None,
        "onlyInHex": False,
        "verbose": False
    }

    ret_status = _exec(dict_to_bunch(args))

    captured = capsys.readouterr()
    captured_lines = captured.out.split("\n")

    assert ret_status == Ret.OK
    assert captured_lines[0] == "uint8_single @ 00000000: 49"
    assert captured_lines[1] == "uint8_array @ 00000001: [50, 51, 52]"
    assert captured_lines[2] == "utf8 @ 00000004: 567"
    assert captured_lines[3] == ""

def test_config_structure(capsys):
    """Test the call via command line args."""
    args = {
        "binaryFile": [ "tests/data/data.txt" ],
        "configFile": [ "tests/data/config_structure.json" ],
        "templateFile": None,
        "onlyInHex": False,
        "verbose": False
    }

    ret_status = _exec(dict_to_bunch(args))

    captured = capsys.readouterr()
    captured_lines = captured.out.split("\n")

    assert ret_status == Ret.OK
    assert captured_lines[0] == "uint8_single_custom.element @ 00000000: 49"
    assert captured_lines[1] == "uint8_list_custom.element @ 00000000: [49, 50, 51, 52, 53, 54, 55, 56]" #pylint: disable=line-too-long
    assert captured_lines[2] == ""

def test_config_structure_nested(capsys):
    """Test the call via command line args."""
    args = {
        "binaryFile": [ "tests/data/data.txt" ],
        "configFile": [ "tests/data/config_structure_nested.json" ],
        "templateFile": None,
        "onlyInHex": False,
        "verbose": False
    }

    ret_status = _exec(dict_to_bunch(args))

    captured = capsys.readouterr()
    captured_lines = captured.out.split("\n")

    assert ret_status == Ret.OK
    assert captured_lines[0] == "ubyte_list.element.a @ 00000000: 49" #pylint: disable=line-too-long
    assert captured_lines[1] == "ubyte_list.element.b @ 00000001: 50" #pylint: disable=line-too-long
    assert captured_lines[2] == ""
