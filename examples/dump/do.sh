#!/bin/bash

if ! command -v pyHexDump --version &> /dev/null
then
    echo Error: Please install https://github.com/BlueAndi/pyHexDump or set it to path.
    exit
fi

echo Dump data as 8-bit
pyHexDump dump ../data/aurix_tc397.hex -a 0x80000020
echo
echo Dump data as 32-bit little endian
pyHexDump dump ../data/aurix_tc397.hex -a 0x80000020 -dt uint32le
echo
echo Dump data as 64-bit little endian
pyHexDump dump ../data/aurix_tc397.hex -a 0x80000020 -dt uint64le
echo
