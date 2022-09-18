# pyHexDump
A CLI tool written in Python to dump binary files and files in intel hex format. It can generate a report for any file based on report template. This is useful for images which contain specific data always on the same address, e.g. a CRC, signature, etc.

There are a lot of hex viewers already, but I was not able to find one which I could configure in a way to generate something like a report.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://choosealicense.com/licenses/mit/)
[![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

# Installation
```cmd
$ git clone https://github.com/BlueAndi/pyHexDump.git
$ cd pyHexDump
$ python setup.py install
```

# Usage

Show help information:
```cmd
$ pyHexDump --help
```

# Examples

## Dump data as 8-bit

```$ pyHexDump dump ./test/aurix_tc397.hex -a 0x80000020```

Result:
```
80000020: 02 58 da 01 9b 1f 00 f0 0f 4f 10 f0 6c 41 c5 ff
80000030: 00 01 bc f1 82 04 6d 00 2f 04 91 30 00 ff 39 ff
80000040: 30 06 16 0f 4b 0f 41 f1 4b f2 51 f0 3c 01 3c 01
80000050: 4b 0f 31 f1 3b 80 3e 00 4b 0f 01 02 e2 08 3c 01
```

## Dump data as 32-bit little endian

```$ pyHexDump dump ./test/aurix_tc397.hex -a 0x80000020 -dt u32le```

Result:
```
80000020: 01da5802 f0001f9b f0104f0f ffc5416c
80000030: f1bc0100 006d0482 3091042f ff39ff00
80000040: 0f160630 f1410f4b f051f24b 013c013c
80000050: f1310f4b 003e803b 02010f4b 013c08e2
80000060: 4800800b 00ce006d 4f409000 80da4802
80000070: 5008003b f440f5a6 006d8402 01da028b
80000080: f0108f0f 9000f16c ffffffff 7fffffff
80000090: f0248160 00873802 ffffffff f0248164
800000a0: 0000d066 ffffffff f0248168 00073802
800000b0: ffffffff f024816c 00009826 ffffffff
800000c0: f0248124 000000c9 ffffffff f0248108
800000d0: 30360001 ffffffff f024810c 0b690708
800000e0: ffffffff f0248128 0121048e ffffffff
800000f0: 00000000 ffffffff ffffffff ffffffff
80000100: f8000091 3048ffd9 0200000d 0fdcf402
80000110: 00000000 00000000 00000000 00000000
```

## Print configuration

```$ pyHexDump print ./test/aurix_tc397.hex ./test/config.json```

with ```config.json``` like
```json
{
    "elements": [{
        "name": "UCB00_BMI_BMHDID",
        "addr": "0xAF400000",
        "dataType": "u32le",
        "count": 1
    }, {
        "name": "UCB00_STAD",
        "addr": "0xAF400004",
        "dataType": "u32le",
        "count": 1
    }, {
        "name": "UCB00_CRCBMHD",
        "addr": "0xAF400008",
        "dataType": "u32le",
        "count": 1
    }, {
        "name": "UCB00_CRCBMHD_N",
        "addr": "0xAF40000C",
        "dataType": "u32le",
        "count": 1
    }, {
        "name": "UCB00_PWx",
        "addr": "0xAF400104",
        "dataType": "u32le",
        "count": 8
    }, {
        "name": "UCB00_CONFIRMATION",
        "addr": "0xAF4001F0",
        "dataType": "u32le",
        "count": 1
    }]
}
```

Result:
```
UCB00_BMI_BMHDID @ af400000: b35900fe
UCB00_STAD @ af400004: a0000000
UCB00_CRCBMHD @ af400008: 31795570
UCB00_CRCBMHD_N @ af40000c: ce86aa8f
UCB00_PWx @ af400104: 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
UCB00_CONFIRMATION @ af4001f0: 43211234
```

## Print report with template

```$ pyHexDump print ./test/aurix_tc397.hex ./test/config.json --template ./test/template.md```

with ```config.json``` like
```json
{
    "elements": [{
        "name": "UCB00_BMI_BMHDID",
        "addr": "0xAF400000",
        "dataType": "u32le",
        "count": 1
    }, {
        "name": "UCB00_STAD",
        "addr": "0xAF400004",
        "dataType": "u32le",
        "count": 1
    }, {
        "name": "UCB00_CRCBMHD",
        "addr": "0xAF400008",
        "dataType": "u32le",
        "count": 1
    }, {
        "name": "UCB00_CRCBMHD_N",
        "addr": "0xAF40000C",
        "dataType": "u32le",
        "count": 1
    }, {
        "name": "UCB00_PWx",
        "addr": "0xAF400104",
        "dataType": "u32le",
        "count": 8
    }, {
        "name": "UCB00_CONFIRMATION",
        "addr": "0xAF4001F0",
        "dataType": "u32le",
        "count": 1
    }]
}
```

with ```template.md``` like
```md
# Aurix TC397 - Blinky Example

## User Control Block 00

|Short Name|Value|
|----------|-----|
| BMI_BMHDID | ${UCB00_BMI_BMHDID} |
| STAD | ${UCB00_STAD} |
| CRCBMHD | ${UCB00_CRCBMHD} |
| CRCBMHD_N | ${UCB00_CRCBMHD_N} |
| PWx | ${UCB00_PWx} |
| CONFIRMATION | ${UCB00_CONFIRMATION} |
```

# Issues, Ideas And Bugs
If you have further ideas or you found some bugs, great! Create a [issue](https://github.com/BlueAndi/pyHexDump/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

# License
The whole source code is published under the [MIT license](http://choosealicense.com/licenses/mit/).
Consider the different licenses of the used third party libraries too!

# Contribution
Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.
