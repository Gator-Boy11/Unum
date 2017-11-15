bitsadmin.exe /transfer "Download" /Download https://www.python.org/ftp/python/3.6.3/python-3.6.3-amd64.exe %cd%\python-3.6.3-amd64.exe
python-3.6.3-amd64.exe /passive PrependPath=1 InstallAllUsers=0 InstallLauncherAllUsers=0
del %cd%\python-3.6.3-amd64.exe