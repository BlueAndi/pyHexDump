#!/bin/bash

if ! command -v parGen --version &> /dev/null
then
    echo Error: Please install https://github.com/nhjschulz/flashcontainer or set it to path.
    exit
fi

if ! command -v pyHexDump --version &> /dev/null
then
    echo Error: Please install https://github.com/BlueAndi/pyHexDump or set it to path.
    exit
fi

echo Generate intel hex file powered by https://github.com/nhjschulz/flashcontainer
parGen --ihex --dump example.xml
echo
echo Generate report in markdown
pyHexDump print example.hex example.pyhexdump --templateFile example.mao > example.md
echo
cat example.md
