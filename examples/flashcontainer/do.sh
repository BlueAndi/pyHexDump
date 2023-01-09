#!/bin/bash

if ! command -v pargen -h > /dev/null 2>&1
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
pargen --static --ihex --pyhexdump --destdir . example.xml
echo
echo Generate report in markdown
CWD=`pwd`
pushd ../..
pyHexDump print $CWD/example.hex $CWD/example.pyhexdump --templateFile $CWD/example.mao > $CWD/example.md
popd
echo
cat example.md
