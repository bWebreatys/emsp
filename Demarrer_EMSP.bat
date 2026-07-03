@echo off
setlocal
cd /d "%~dp0"
title EMSP - Interface de gestion
set "RT=%~dp0socle\runtime"
if not exist "%RT%\python.exe" (
  echo [ERREUR] Le socle n'est pas installe.
  echo Lancez d'abord :  socle\1_Installer_le_socle.bat
  pause & exit /b 1
)
echo Demarrage de l'interface EMSP...
echo Le navigateur s'ouvrira automatiquement sur  http://127.0.0.1:5000
echo (Patientez quelques secondes. Fermez cette fenetre pour arreter le serveur.)
"%RT%\python.exe" "%~dp0_lancer_emsp.py"
if errorlevel 1 pause
