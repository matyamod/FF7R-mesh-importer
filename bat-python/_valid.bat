#Drop .uexp onto this batch file.

@echo off

@if "%~1"=="" goto skip

@pushd %~dp0
python ..\src\main.py "%~1" valid --mode=valid --verbose
@popd

pause

:skip