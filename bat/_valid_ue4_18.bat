@echo off

@if "%~1"=="" goto skip

@pushd %~dp0
python src\main.py "%~1" valid --mode=valid_ue4_18 --verbose
@popd

pause

:skip