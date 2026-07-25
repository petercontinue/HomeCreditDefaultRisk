@echo off
cd /d "%~dp0"
echo Stopping backend (port 8000)...
powershell -NoProfile -Command ^
  "$conns = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue;" ^
  "if (-not $conns) { Write-Host 'Backend is not running.'; exit 0 }" ^
  "$procIds = @($conns | Select-Object -ExpandProperty OwningProcess -Unique);" ^
  "foreach ($procId in $procIds) { try { Stop-Process -Id $procId -Force -ErrorAction Stop; Write-Host ('Stopped PID ' + $procId) } catch { Write-Host ('Could not stop PID ' + $procId) } }"
echo Done.
pause
