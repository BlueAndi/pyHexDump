# pyHexDump <!-- omit in toc -->

# Examples
Before running any of the examples please ensure that Python is installed, as well as pyHexDump!

Open a command line terminal and enter:
```bash
$ python --version
```

You should see something like \
```bash
Python 3.9.4
```

In the same way check for pyHexDump.
```bash
$ pyHexDump --version
```

And you should see the version information.

## Calculate CRC
Calculates the CRC checksum from a start address to a end address.

Folder: [calculate_crc](./calculate_crc/)

## Dump Data
Dump data by using different datatypes.

Folder: [dump](./dump/)

## Generate A Flash Container
[ParGen (https://github.com/nhjschulz/flashcontainer)](https://github.com/nhjschulz/flashcontainer) is an embedded development tool for generation of parameters values that can be stored in flash memory and maintained independent from the application. It allows to alter/update parameter values without recompilations.

In this example it is used to generate such a flash container in intel hex format and with pyHexDump the generated flash container file is analyzed to generate a report in markdown format.

Folder: [flashcontainer](./flashcontainer/)

## Print Data From Configuration
Parameters are configured in a configuration file, which is used to determine its values and print them to the CLI.

Folder: [print_config](./print_config/)

## Generate A Report
Generate a report by using a configuration and a template file.

Folder: [print_config_and_template](./print_config_and_template/)

## Configure A Custom Datatype
Sometimes at given address there can be a structure of several elements with different datatypes. In this example the configuration contains the element and its datatype is just a list of further elements. Recommended is to define a structure and assign a dataype name, which can be reused several times. See in the next example.

Folder: [print_config_with_custom_datatype](./print_config_with_custom_datatype/)

## Configure A Structure As New Datatype
Sometimes at given address there can be a structure of several elements with different datatypes. In this example the configuration contains the definition of the structure as separate datatype.

Folder: [print_config_with_structure](./print_config_with_structure/)

# Issues, Ideas And Bugs
If you have further ideas or you found some bugs, great! Create a [issue](https://github.com/BlueAndi/pyHexDump/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

# License
The whole source code is published under the [MIT license](http://choosealicense.com/licenses/mit/).
Consider the different licenses of the used third party libraries too!

# Contribution
Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.
