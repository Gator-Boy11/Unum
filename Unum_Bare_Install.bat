@echo off
reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT
if %OS%==64BIT powershell -command "start-bitstransfer -source https://www.python.org/ftp/python/3.6.4/python-3.6.4-amd64.exe -destination python-3.6.4.exe"
if %OS%==32BIT powershell -command "start-bitstransfer -source https://www.python.org/ftp/python/3.6.4/python-3.6.4.exe -destination python-3.6.4.exe"
python-3.6.4.exe /passive PrependPath=0 InstallAllUsers=0 InstallLauncherAllUsers=0 DefaultJustForMeTargetDir=%USERPROFILE%\Documents
if %OS%==64BIT del %cd%\python-3.6.4.exe