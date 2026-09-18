@echo off
setlocal EnableExtensions DisableDelayedExpansion

set "APP_HOST="
if defined CGCLI_APP_PATH set "APP_HOST=%CGCLI_APP_PATH%"

if not defined APP_HOST (
    set "CONFIG_PATH=%LOCALAPPDATA%\Congguo\cgcli-app-path.txt"
    if exist "%CONFIG_PATH%" set /p APP_HOST=<"%CONFIG_PATH%"
)

if not defined APP_HOST (
    echo cgcli: Congguo Depth Studio runtime was not found. 1>&2
    echo Run install-launcher-windows.ps1 or set CGCLI_APP_PATH. 1>&2
    exit /b 3
)

if exist "%APP_HOST%\CongGuoCliHost.exe" set "APP_HOST=%APP_HOST%\CongGuoCliHost.exe"
if not exist "%APP_HOST%" (
    echo cgcli: App CLI host is missing: %APP_HOST% 1>&2
    exit /b 3
)

"%APP_HOST%" --cgcli %*
exit /b %ERRORLEVEL%
