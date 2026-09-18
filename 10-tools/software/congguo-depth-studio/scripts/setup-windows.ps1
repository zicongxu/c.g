[CmdletBinding()]
param(
    [string]$PythonCommand = "",
    [switch]$SkipModel
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$CliRoot = Join-Path (Split-Path -Parent (Split-Path -Parent $ProjectRoot)) "cli\cgcli"
$VirtualPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)][string]$Executable,
        [Parameter(Mandatory = $true)][string[]]$ArgumentList
    )
    & $Executable @ArgumentList
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $Executable $ArgumentList"
    }
}

Push-Location $ProjectRoot
try {
    if (-not (Test-Path -LiteralPath $VirtualPython)) {
        if ($PythonCommand) {
            Invoke-Checked -Executable $PythonCommand -ArgumentList @("-m", "venv", ".venv")
        }
        elseif (Get-Command py -ErrorAction SilentlyContinue) {
            Invoke-Checked -Executable "py" -ArgumentList @("-3.12", "-m", "venv", ".venv")
        }
        elseif (Get-Command python -ErrorAction SilentlyContinue) {
            Invoke-Checked -Executable "python" -ArgumentList @("-m", "venv", ".venv")
        }
        else {
            throw "Python 3.9-3.13 was not found. Install Python 3.12 x64 and rerun."
        }
    }

    Invoke-Checked -Executable $VirtualPython -ArgumentList @(
        "-c",
        (
            "import sys; assert (3, 9) <= sys.version_info[:2] < (3, 14), " +
            "'Python 3.9-3.13 is required'"
        )
    )
    Invoke-Checked -Executable $VirtualPython `
        -ArgumentList @("-m", "pip", "install", "--upgrade", "pip>=23,<27")
    Invoke-Checked -Executable $VirtualPython `
        -ArgumentList @("-m", "pip", "install", "-e", ".[dev,build]")
    Invoke-Checked -Executable $VirtualPython `
        -ArgumentList @("-m", "pip", "install", "-e", "${CliRoot}[dev]")

    if (-not $SkipModel) {
        & (Join-Path $PSScriptRoot "download-model.ps1")
        if ($LASTEXITCODE -ne 0) {
            throw "Model download failed with exit code $LASTEXITCODE"
        }
    }

    Write-Host "Windows development environment is ready."
    Write-Host "Run App: .\.venv\Scripts\python.exe -m congguo_depth_studio"
    Write-Host "Run CLI: .\.venv\Scripts\cgcli.exe --version"
}
finally {
    Pop-Location
}
