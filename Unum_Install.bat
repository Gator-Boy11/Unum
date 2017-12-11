@echo off
mkdir Unum
cd Unum
bitsadmin.exe /transfer "Download" /Download https://raw.githubusercontent.com/Gator-Boy11/Unum/master/unum_client.py %cd%\unum_client.py
bitsadmin.exe /transfer "Download" /Download https://raw.githubusercontent.com/Gator-Boy11/Unum/master/unum_server.py %cd%\unum_server.py
bitsadmin.exe /transfer "Download" /Download https://raw.githubusercontent.com/Gator-Boy11/Unum/master/LICENSE %cd%\LICENSE.txt
bitsadmin.exe /transfer "Download" /Download https://raw.githubusercontent.com/Gator-Boy11/Unum/master/README.md %cd%\README.md
reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT
if %OS%==64BIT bitsadmin.exe /transfer "Download" /Download https://www.python.org/ftp/python/3.6.3/python-3.6.3-amd64.exe %cd%\python-3.6.3.exe
if %OS%==32BIT bitsadmin.exe /transfer "Download" /Download https://www.python.org/ftp/python/3.6.3/python-3.6.3.exe %cd%\python-3.6.3.exe
python-3.6.3.exe /passive PrependPath=0 InstallAllUsers=0 InstallLauncherAllUsers=0 DefaultJustForMeTargetDir=%USERPROFILE%\Documents
del %cd%\python-3.6.3-amd64.exe
