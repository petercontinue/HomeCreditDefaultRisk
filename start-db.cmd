@echo off
cd /d "%~dp0"
echo Starting PostgreSQL (port 6436)...
docker compose up -d
docker compose ps
