@echo off

pyHexDump --version 2>NUL
if errorlevel 1 goto pyHexDump_not_found

echo Dump data as 8-bit
pyHexDump dump ..\data\aurix_tc397.hex -a 0x80000020
echo.
echo Dump data as 32-bit little endian
pyHexDump dump ..\data\aurix_tc397.hex -a 0x80000020 -dt u32le
echo.
echo Dump data as 64-bit little endian
pyHexDump dump ..\data\aurix_tc397.hex -a 0x80000020 -dt u64le
echo.
goto :eof

:pyHexDump_not_found
echo Error: Please install https://github.com/BlueAndi/pyHexDump or set it to path.
