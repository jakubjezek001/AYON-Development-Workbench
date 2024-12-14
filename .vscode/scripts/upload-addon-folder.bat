@echo off
@REM %1 -> addon folder path

cd /d %cd%/.vscode/scripts/

@REM Upload addons
call .\.poetry\bin\poetry.exe run python upload-addon-folder.py --debug --addon %1
