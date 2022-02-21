@echo off

set ff7r_file=NP0030_00.uexp
set ue4_18_file=test\NP0030_00.uexp
set save_folder=test\OnlyMesh\

python ..\src\main.py %ff7r_file% %ue4_18_file% %save_folder% --verbose --only_mesh

pause