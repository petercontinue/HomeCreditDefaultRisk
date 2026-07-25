$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
& "$Root\start-backend.cmd"
