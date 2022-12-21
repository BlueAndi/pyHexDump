@echo off

pyHexDump --version 2>NUL
if errorlevel 1 goto pyHexDump_not_found

echo Print configuration with custom datatype
pyHexDump print ..\data\aurix_tc397.hex config.json --onlyInHex
echo.
goto :eof

:pyHexDump_not_found
echo Error: Please install https://github.com/BlueAndi/pyHexDump or set it to path.
