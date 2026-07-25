@echo off
cd /d "%~dp0"
echo Stopping PostgreSQL container...
docker compose down
if errorlevel 1 (
  echo [ERROR] Failed to stop database. Is Docker running?
) else (
  echo Database stopped.
)
pause
