@echo off

REM Drug and drop .uexp into this batch file.
REM It will dump the buffers in the 'buffers' folder.

@if "%~1"=="" goto skip

@pushd %~dp0
src\main.exe "%~1" buffers --mode=dumpBuffers --verbose
@popd

pause

:skip