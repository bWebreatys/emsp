@echo off
setlocal
cd /d "%~dp0"
title Installation du socle EMSP (hors-ligne)
set "RT=%~dp0runtime"

REM 1) Reperer le zip Python embeddable depose dans embeddable\
set "ZIP="
for %%f in ("embeddable\python-3.12*-embed-amd64.zip") do set "ZIP=%%f"
if "%ZIP%"=="" (
  echo [ERREUR] Le Python "embeddable" est introuvable.
  echo.
  echo Deposez le fichier   python-3.12.10-embed-amd64.zip   dans le dossier  embeddable\
  echo Lien officiel : https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip
  echo Cette etape se fait UNE seule fois, depuis une machine connectee.
  echo.
  pause & exit /b 1
)

echo [1/4] Decompression du runtime Python...
if exist "%RT%" rmdir /s /q "%RT%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Force '%ZIP%' '%RT%'"
if not exist "%RT%\python.exe" ( echo [ERREUR] Decompression echouee. & pause & exit /b 1 )

echo [2/4] Configuration du runtime...
set "PTH="
for %%v in ("%RT%\python3*._pth") do set "PTH=%%v"
> "%PTH%" echo python312.zip
>> "%PTH%" echo .
>> "%PTH%" echo .\Lib\site-packages
>> "%PTH%" echo .\Scripts
>> "%PTH%" echo import site

echo [3/4] Installation de pip (hors-ligne)...
"%RT%\python.exe" "wheels\get-pip.py" --no-index --find-links "wheels" --no-warn-script-location
if errorlevel 1 ( echo [ERREUR] pip non installe. & pause & exit /b 1 )

echo [4/4] Installation des dependances Flask + openpyxl (hors-ligne)...
"%RT%\python.exe" -m pip install --no-index --find-links "wheels" Flask openpyxl --no-warn-script-location
if errorlevel 1 ( echo [ERREUR] Dependances non installees. & pause & exit /b 1 )

echo.
echo  ====================================================
echo   Socle installe. Lancez maintenant  Demarrer_EMSP.bat
echo  ====================================================
echo.
pause
