#!/bin/bash

if ! command -v pyHexDump --version &> /dev/null
then
    echo Error: Please install https://github.com/BlueAndi/pyHexDump or set it to path.
    exit
fi

echo Print configuration with custom datatype
pyHexDump print ../data/aurix_tc397.hex config.json --onlyInHex
echo
