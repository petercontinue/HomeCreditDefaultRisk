@echo off
cd /d "%~dp0"
echo Stopping frontend (port 5173)...
powershell -NoProfile -Command ^
  "$conns = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue;" ^
  "if (-not $conns) { Write-Host 'Frontend is not running.'; exit 0 }" ^
  "$procIds = @($conns | Select-Object -ExpandProperty OwningProcess -Unique);" ^
  "foreach ($procId in $procIds) { try { Stop-Process -Id $procId -Force -ErrorAction Stop; Write-Host ('Stopped PID ' + $procId) } catch { Write-Host ('Could not stop PID ' + $procId) } }"
echo Done.
pause
