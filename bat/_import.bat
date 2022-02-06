@echo off

set ff7r_file=WE0005_00_Yuffie_Shuriken\Model\WE0005_00.uexp
set ue4_18_file=foo\bar.uexp
set save_folder=test\Weapon\WE0005_00_Yuffie_Shuriken\Model

python ..\src\main.py %ff7r_file% %ue4_18_file% %save_folder%

pause