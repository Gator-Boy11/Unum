@echo off
mkdir Unum
cd Unum
powershell -command "start-bitstransfer -source https://raw.githubusercontent.com/Gator-Boy11/Unum/master/unum_client.py -destination unum_client.py"
powershell -command "start-bitstransfer -source https://raw.githubusercontent.com/Gator-Boy11/Unum/master/unum_server.py-destination unum_server.py"
powershell -command "start-bitstransfer -source https://raw.githubusercontent.com/Gator-Boy11/Unum/master/LICENSE -destination LICENSE.txt"
powershell -command "start-bitstransfer -source https://raw.githubusercontent.com/Gator-Boy11/Unum/master/README.md -destination README.md"
reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT
if %OS%==64BIT powershell -command "start-bitstransfer -source https://www.python.org/ftp/python/3.6.4/python-3.6.4-amd64.exe -destination python-3.6.4.exe"
if %OS%==32BIT powershell -command "start-bitstransfer -source https://www.python.org/ftp/python/3.6.4/python-3.6.4.exe -destination python-3.6.4.exe"
python-3.6.4.exe /passive PrependPath=0 InstallAllUsers=0 InstallLauncherAllUsers=0 DefaultJustForMeTargetDir=%USERPROFILE%\Documents
del %cd%\python-3.6.4.exe