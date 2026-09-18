[CmdletBinding()]
param(
    [string]$ModelUrl = (
        "https://huggingface.co/CyberTimon/RapidRAW-Models/resolve/" +
        "daec18e762798acb835d3cda7542d9ecee0dc16b/" +
        "depth_anything_v2_vits.onnx?download=true"
    )
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$TargetModel = Join-Path $ProjectRoot (
    "src\congguo_depth_studio\resources\depth_anything_v2_vits.onnx"
)
$ExpectedSha256 = "d2b11a11c1d4a12b47608fa65a17ee9a4c605b55ee1730c8e3b526304f2562be"

if (Test-Path -LiteralPath $TargetModel) {
    $InstalledSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $TargetModel).Hash.ToLower()
    if ($InstalledSha256 -eq $ExpectedSha256) {
        Write-Host "Model already installed and verified: $TargetModel"
        exit 0
    }
}

$TemporaryModel = "$TargetModel.download.$PID"
try {
    Write-Host "Downloading the pinned Depth Anything V2 Small ONNX artifact..."
    Invoke-WebRequest -Uri $ModelUrl -OutFile $TemporaryModel
    $ActualSha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $TemporaryModel).Hash.ToLower()
    if ($ActualSha256 -ne $ExpectedSha256) {
        throw "Model SHA-256 mismatch. Expected $ExpectedSha256; actual $ActualSha256"
    }
    Move-Item -Force -LiteralPath $TemporaryModel -Destination $TargetModel
    Write-Host "Downloaded and verified model: $TargetModel"
}
finally {
    if (Test-Path -LiteralPath $TemporaryModel) {
        Remove-Item -Force -LiteralPath $TemporaryModel
    }
}
