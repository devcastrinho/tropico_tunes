@echo off
title TROPICO - Servidor local
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo.
  echo Ambiente virtual nao encontrado.
  echo Siga a primeira instalacao descrita no arquivo COMO_USAR.md.
  echo.
  pause
  exit /b 1
)

echo.
echo ==============================================
echo   TROPICO iniciado em http://127.0.0.1:5000
echo ==============================================
echo.
echo Mantenha esta janela aberta.
echo Pressione Ctrl+C para encerrar o sistema.
echo.

set "DATABASE_URL=sqlite:///tropico.db"
".venv\Scripts\python.exe" -m flask --app run.py seed
if errorlevel 1 (
  echo.
  echo Nao foi possivel preparar o banco local.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" -m flask --app run.py run
pause
