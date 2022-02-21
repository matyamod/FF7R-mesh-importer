@echo off

REM Drop .uexp onto this batch file.

@if "%~1"=="" goto skip

@pushd %~dp0
src\main.exe "%~1" valid --mode=valid --verbose
@popd

pause

:skip