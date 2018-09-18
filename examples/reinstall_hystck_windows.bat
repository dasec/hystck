REM remove old installation
cd %HOMEPATH%\hystck
del /Q *

REM copy hystck from CD drive \E -> recursive, /Y suppress confirmations, /Q hide filenames while copying
XCOPY D:\* . /E /Y /Q

REM start installation
python setup.py install