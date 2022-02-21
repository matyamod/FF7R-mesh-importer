REM Drug and drop .uexp into this batch file.
REM It will dump the buffers in the 'buffers' folder.

@echo off

@if "%~1"=="" goto skip

@pushd %~dp0
python ..\src\main.py "%~1" buffers --mode=dumpBuffers --verbose
@popd

pause

:skip