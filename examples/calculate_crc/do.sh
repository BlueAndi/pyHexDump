#!/bin/bash

if ! command -v pyHexDump --version &> /dev/null
then
    echo Error: Please install https://github.com/BlueAndi/pyHexDump or set it to path.
    exit
fi

echo Calculate CRC checksum from 0x80000020 to 0x80000040
pyHexDump checksum ../data/aurix_tc397.hex -sa 0x80000020 -ea 0x80000040
echo
