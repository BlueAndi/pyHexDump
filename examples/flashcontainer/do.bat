@echo off

parGen --version 2>NUL
if errorlevel 1 goto parGen_not_found

pyHexDump --version 2>NUL
if errorlevel 1 goto pyHexDump_not_found

echo Generate intel hex file powered by https://github.com/nhjschulz/flashcontainer
parGen --ihex --dump example.xml 2>NUL
echo
echo Generate report in markdown
pyHexDump print example.hex example.pyhexdump --templateFile example.mao > example.md
echo
type example.md

goto :eof

:parGen_not_found
echo Error: Please install https://github.com/nhjschulz/flashcontainer or set it to path.
goto :eof

:pyHexDump_not_found
echo Error: Please install https://github.com/BlueAndi/pyHexDump or set it to path.
