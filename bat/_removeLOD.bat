REM Drug and drop .uexp into this batch file.
REM A new asset will be generated in the 'LODremoved' folder.

@echo off

@if "%~1"=="" goto skip

@pushd %~dp0
python ..\src\main.py "%~1" LODremoved --mode=removeLOD --verbose
@popd

pause

:skip