@echo off
goto :check_Permissions
goto :check_Prerequisites check

IF %check% DO (
    REM call install functions
    python %~dp0pre_setup.py
)

echo "Installation finished"
pause > nul
exit
goto :eof

:check_Permissions
    echo Administrative permissions required. Detecting permissions...

    net session >nul 2>&1
    if %errorLevel% == 0 (
        echo Success: Administrative permissions confirmed.
    ) else (
        echo Failure: Current permissions inadequate.
    )

    pause >nul

:check_Prerequisites
    FOR /F "tokens=2*" %%A IN (REG Query HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall /s /v DisplayName 2^>nul ^| find /I "for python 2.7"') DO (
        set vcc=OK
    )

    FOR /F "tokens=2*" %%A IN (REG Query HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall /s /v DisplayName 2^>nul ^| find /I "python 2.7."') DO (
        set pyt=OK
    )

    IF NOT %pyt%==OK echo "Python is not installed".&GOTO:eof
    IF NOT %vcc%==OK echo "Visual C++ for Python is not installed".&GOTO:eof


    REM return true
    set %1=True


cmd /k