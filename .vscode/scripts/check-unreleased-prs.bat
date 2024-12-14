@echo off
@REM %1 -> Current Directory

@REM This is hardcoded.
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
    echo Checking unreleased PRs for ynput/%%i
    gh pr list --repo ynput/%%i --state merged --search "merged:>=$(gh release view --json publishedAt --jq '.publishedAt' --repo=ynput/%%i)"
)