[CmdletBinding()]
param(
    [switch]$SkipSetup,
    [switch]$SkipTests,
    [switch]$SkipArchive,
    [string]$PythonCommand = ""
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$CliRoot = Join-Path (Split-Path -Parent (Split-Path -Parent $ProjectRoot)) "cli\cgcli"
$VirtualPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$ModelPath = Join-Path $ProjectRoot (
    "src\congguo_depth_studio\resources\depth_anything_v2_vits.onnx"
)
$ExpectedSha256 = "d2b11a11c1d4a12b47608fa65a17ee9a4c605b55ee1730c8e3b526304f2562be"

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
    if (-not $SkipSetup) {
        $SetupArguments = @()
        if ($PythonCommand) {
            $SetupArguments += @("-PythonCommand", $PythonCommand)
        }
        & (Join-Path $PSScriptRoot "setup-windows.ps1") @SetupArguments
        if ($LASTEXITCODE -ne 0) {
            throw "Windows setup failed with exit code $LASTEXITCODE"
        }
    }

    if (-not (Test-Path -LiteralPath $VirtualPython)) {
        throw "Missing .venv. Run scripts\setup-windows.ps1 first."
    }
    if (-not (Test-Path -LiteralPath $ModelPath)) {
        throw "Missing model. Run scripts\download-model.ps1 first."
    }
    $ModelSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $ModelPath).Hash.ToLower()
    if ($ModelSha256 -ne $ExpectedSha256) {
        throw "Model SHA-256 mismatch; refusing to build."
    }

    if (-not $SkipTests) {
        Write-Host "Running App and CLI lint/tests..."
        Invoke-Checked -Executable $VirtualPython -ArgumentList @(
            "-m", "ruff", "check", "src", "tests",
            (Join-Path $CliRoot "src"), (Join-Path $CliRoot "tests")
        )
        Invoke-Checked -Executable $VirtualPython -ArgumentList @(
            "-m", "pytest", "-q", "tests", (Join-Path $CliRoot "tests")
        )
    }

    Write-Host "Building Windows portable package with PyInstaller..."
    Invoke-Checked -Executable $VirtualPython -ArgumentList @(
        "-m", "PyInstaller", "--noconfirm", "--clean",
        "packaging\windows\DepthMotionStudio.spec"
    )

    $DistRoot = Join-Path $ProjectRoot "dist\CongGuoDepthStudio"
    $GuiExecutable = Join-Path $DistRoot "CongGuoDepthStudio.exe"
    $CliExecutable = Join-Path $DistRoot "CongGuoCliHost.exe"
    if (-not (Test-Path -LiteralPath $GuiExecutable)) {
        throw "Packaged GUI executable is missing: $GuiExecutable"
    }
    if (-not (Test-Path -LiteralPath $CliExecutable)) {
        throw "Packaged CLI host is missing: $CliExecutable"
    }

    $CliVersion = & $CliExecutable --cgcli --version
    if ($LASTEXITCODE -ne 0 -or $CliVersion -notmatch "^cgcli ") {
        throw "Packaged cgcli smoke test failed: $CliVersion"
    }

    Write-Host "Packaged CLI host passed: $CliVersion"
    $PreviousPlatform = $env:QT_QPA_PLATFORM
    $PreviousSmoke = $env:DEPTH_STUDIO_SMOKE_TEST
    try {
        $env:QT_QPA_PLATFORM = "minimal"
        $env:DEPTH_STUDIO_SMOKE_TEST = "1"
        $SmokeOutput = & $CliExecutable 2>&1
        $SmokeExitCode = $LASTEXITCODE
        $SmokeText = ($SmokeOutput | ForEach-Object { "$_" }) -join " | "
        if ($SmokeExitCode -ne 0) {
            throw "Packaged App smoke test exited ${SmokeExitCode}: $SmokeText"
        }
        if ($SmokeText -notmatch "ready=True") {
            throw "Packaged App smoke test returned unexpected output: $SmokeText"
        }
    }
    finally {
        $env:QT_QPA_PLATFORM = $PreviousPlatform
        $env:DEPTH_STUDIO_SMOKE_TEST = $PreviousSmoke
    }

    Write-Host "Packaged GUI runtime and model discovery passed."
    Write-Host "Built and verified: $DistRoot"
    if (-not $SkipArchive) {
        $ArchivePath = Join-Path $ProjectRoot "dist\congguo-depth-studio-v2.4.0-windows-x64.zip"
        if (Test-Path -LiteralPath $ArchivePath) {
            Remove-Item -Force -LiteralPath $ArchivePath
        }
        Compress-Archive -Path $DistRoot -DestinationPath $ArchivePath
        $ArchiveHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $ArchivePath).Hash.ToLower()
        Write-Host "Archive: $ArchivePath"
        Write-Host "SHA-256: $ArchiveHash"
    }
}
finally {
    Pop-Location
}
