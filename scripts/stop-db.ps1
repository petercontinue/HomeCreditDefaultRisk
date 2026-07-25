$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
& "$Root\stop-db.cmd"
