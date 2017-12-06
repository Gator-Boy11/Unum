@echo off
mkdir Unum
cd Unum
bitsadmin.exe /transfer "Download" /Download https://raw.githubusercontent.com/Gator-Boy11/Unum/master/unum_client.py %cd%\unum_client.py
bitsadmin.exe /transfer "Download" /Download https://raw.githubusercontent.com/Gator-Boy11/Unum/master/unum_server.py %cd%\unum_server.py
bitsadmin.exe /transfer "Download" /Download https://raw.githubusercontent.com/Gator-Boy11/Unum/master/LICENSE %cd%\LICENSE.txt
bitsadmin.exe /transfer "Download" /Download https://raw.githubusercontent.com/Gator-Boy11/Unum/master/README.md %cd%\README.md
bitsadmin.exe /transfer "Download" /Download https://www.python.org/ftp/python/3.6.3/python-3.6.3-amd64.exe %cd%\python-3.6.3-amd64.exe
python-3.6.3-amd64.exe /passive PrependPath=0 InstallAllUsers=0 InstallLauncherAllUsers=0 DefaultJustForMeTargetDir=%USERPROFILE%\Documents
del %cd%\python-3.6.3-amd64.exe
