@echo off

REM Drug and drop .uexp into this batch file.
REM It will generate a .gltf file in the 'exported' folder.

@if "%~1"=="" goto skip

@pushd %~dp0
python ..\src\main.py "%~1" exported --mode=export --verbose
@popd

pause

:skip