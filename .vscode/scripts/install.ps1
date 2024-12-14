$script_dir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$repo_root = (Get-Item $script_dir).FullName


function Default-Func {
    Write-Host ""
    Write-Host "venv desktop application tool"
    Write-Host ""
    Write-Host "Usage: ", "./install.ps1 ", "[target]"
    Write-Host ""
    Write-Host "Runtime targets:"
    Write-Host "  install  ", "Install runtime dependencies"
    Write-Host ""
}


function Install-Poetry() {
    Write-Host ">>> ", "Installing Poetry ... "
    $python = "python"
    if (Get-Command "pyenv" -ErrorAction SilentlyContinue) {
        if (-not (Test-Path -PathType Leaf -Path "$($repo_root)\.python-version")) {
            $result = & pyenv global
            if ($result -eq "no global version configured") {
                Write-Color -Text "!!! ", "Using pyenv but having no local or global version of Python set." -Color Red, Yellow
                Exit-WithCode 1
            }
        }
        $python = & pyenv which python

    }

    $env:POETRY_HOME="$repo_root\.poetry"
    (Invoke-WebRequest -Uri https://install.python-poetry.org/ -UseBasicParsing).Content | & $($python) -
}




function Main {
    if ($FunctionName -eq $null) {
        Install-Poetry
        Default-Func
        return
    }

    if ($FunctionName -eq "install") {
        Write-Host "Installation complete."
        Install-Poetry
    } else {
        Default-Func
    }
}

if (-not (Test-Path 'env:POETRY_HOME')) {
    $env:POETRY_HOME = "$repo_root\.poetry"
}

Main