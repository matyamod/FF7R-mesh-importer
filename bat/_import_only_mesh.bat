@echo off

set ff7r_file=PC0001_00_Barret_Standard\Model\PC0001_00.uexp
set ue4_18_file=MyUE4Barret\PC0001_00.uexp
set save_folder=test\PC0001_00\Model

python ..\src\main.py %ff7r_file% %ue4_18_file% %save_folder% --verbose --only_mesh

pause