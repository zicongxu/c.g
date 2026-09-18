[CmdletBinding()]
param(
    [string]$AppPath = "",
    [string]$BinDir = (Join-Path $env:LOCALAPPDATA "Congguo\bin"),
    [switch]$NoPathUpdate
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Launcher = Join-Path $ProjectRoot "launcher\cgcli.cmd"
$WorkspaceTools = Split-Path -Parent (Split-Path -Parent $ProjectRoot)
$DefaultBuild = Join-Path $WorkspaceTools (
    "software\congguo-depth-studio\dist\CongGuoDepthStudio"
)

if (-not $AppPath) {
    $AppPath = $DefaultBuild
}
if (Test-Path -LiteralPath $AppPath -PathType Container) {
    $AppHost = Join-Path $AppPath "CongGuoCliHost.exe"
}
else {
    $AppHost = $AppPath
}
if (-not (Test-Path -LiteralPath $AppHost -PathType Leaf)) {
    throw "App CLI host was not found: $AppHost"
}

$HostVersion = & $AppHost --cgcli --version
if ($LASTEXITCODE -ne 0 -or $HostVersion -notmatch "^cgcli ") {
    throw "App CLI host failed its version check: $HostVersion"
}

New-Item -ItemType Directory -Force -Path $BinDir | Out-Null
$InstalledLauncher = Join-Path $BinDir "cgcli.cmd"
Copy-Item -Force -LiteralPath $Launcher -Destination $InstalledLauncher

$ConfigDir = Join-Path $env:LOCALAPPDATA "Congguo"
New-Item -ItemType Directory -Force -Path $ConfigDir | Out-Null
$ConfigPath = Join-Path $ConfigDir "cgcli-app-path.txt"
$Utf8WithoutBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($ConfigPath, $AppHost, $Utf8WithoutBom)

if (-not $NoPathUpdate) {
    $UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $PathEntries = @($UserPath -split ";" | Where-Object { $_ })
    if ($PathEntries -notcontains $BinDir) {
        $UpdatedPath = (@($PathEntries) + $BinDir) -join ";"
        [Environment]::SetEnvironmentVariable("Path", $UpdatedPath, "User")
        Write-Host "Added to user PATH: $BinDir"
    }
}

Write-Host "Installed cgcli launcher: $InstalledLauncher"
Write-Host "Using App CLI host: $AppHost"
Write-Host "Open a new terminal, then run: cgcli --version"
