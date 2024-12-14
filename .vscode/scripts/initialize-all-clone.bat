@echo off
@REM %1 -> Current Directory

@REM This is hardcoded.
cd /d %1
for %%i in (
    ayon-applications,
    ayon-core,
    ayon-docker,
    ayon-circuit,
    ayon-deadline,
    ayon-dependencies-tool,
    ayon-documentation,
    ayon-launcher,
    ayon-nuke,
    ayon-flame,
    ayon-resolve,
    ayon-syncsketch,
    ayon-ocio,
    ayon-python-api,
    ayon-third-party,
    ayon-traypublisher,
    example-studio-addon,
    ayon-ftrack,
    ayon-shotgrid
) do (
    if exist %1/%%i (echo %1/%%i exists) else (git clone https://github.com/ynput/%%i.git)
)